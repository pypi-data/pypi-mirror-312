from __future__ import annotations
import logging

import numpy
from silx.gui import qt
from silx.gui.colors import Colormap
from silx.gui.plot.StackView import StackViewMainWindow

from darfix import config, dtypes
from darfix.core.dataset import ImageDataset, Operation
from darfix.core.imageOperations import Method
from darfix.core.noiseremoval import (
    BackgroundType,
    NoiseRemovalOperation,
    apply_noise_removal_operation,
)

from ..operationThread import OperationThread
from .parametersDock import ParametersDock

_logger = logging.getLogger(__file__)


class NoiseRemovalDialog(qt.QDialog):
    """
    Dialog with `NoiseRemovalWidget` as main window and standard buttons.
    """

    okSignal = qt.Signal()

    def __init__(self, parent=None):
        qt.QDialog.__init__(self, parent)
        self.setWindowFlags(qt.Qt.WindowType.Widget)
        self._buttons = qt.QDialogButtonBox(parent=self)
        self._buttons.setStandardButtons(
            qt.QDialogButtonBox.Ok | qt.QDialogButtonBox.Abort
        )
        self._buttons.setEnabled(False)
        resetB = self._buttons.addButton(qt.QDialogButtonBox.Reset)
        self.mainWindow = _NoiseRemovalWidget(parent=self)
        self.mainWindow.setAttribute(qt.Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setLayout(qt.QVBoxLayout())
        self.layout().addWidget(self.mainWindow)
        self.layout().addWidget(self._buttons)

        self._buttons.accepted.connect(self.okSignal.emit)
        resetB.clicked.connect(self.mainWindow.resetStack)
        self._buttons.rejected.connect(self.mainWindow.abortCurrentComputation)
        self._buttons.button(qt.QDialogButtonBox.Abort).hide()

        self.mainWindow.computingSignal.connect(self._toggleButton)

    def setDataset(self, owdataset: dtypes.OWDataset):
        if owdataset.dataset is not None:
            self._buttons.setEnabled(True)
            self.mainWindow.setDataset(owdataset)

    def getDataset(self, parent) -> dtypes.OWDataset:
        return self.mainWindow.getDataset(parent)

    def getOperationHistory(self):
        return self.mainWindow._operationHistory

    def _toggleButton(self, isComputing: bool):
        self._buttons.button(qt.QDialogButtonBox.Ok).setDisabled(isComputing)
        self._buttons.button(qt.QDialogButtonBox.Abort).setVisible(isComputing)


class _NoiseRemovalWidget(qt.QMainWindow):
    """
    Widget to apply noise removal from a dataset.
    For now it can apply both background subtraction and hot pixel removal.
    For background subtraction the user can choose the background to use:
    dark frames, low intensity data or all the data. From these background
    frames, an image is computed either using the mean or the median.
    """

    computingSignal = qt.Signal(bool)

    def __init__(self, parent=None):
        qt.QMainWindow.__init__(self, parent)

        self._input_dataset: ImageDataset | None = None
        self._output_dataset: ImageDataset | None = None
        self.indices: numpy.ndarray | None = None
        self.bg_indices: numpy.ndarray | None = None
        self.bg_dataset: ImageDataset | None = None
        self.setWindowFlags(qt.Qt.WindowType.Widget)

        self._parametersDock = ParametersDock()
        self._parametersDock.setFeatures(qt.QDockWidget.DockWidgetMovable)
        self._sv = StackViewMainWindow()
        self._sv.setColormap(
            Colormap(
                name=config.DEFAULT_COLORMAP_NAME,
                normalization=config.DEFAULT_COLORMAP_NORM,
            )
        )

        self._size = None
        self._method = None
        self._background = self._parametersDock.bsBackgroundCB.currentText()
        self._bottom_threshold = self._parametersDock.bottomLE.text()
        self._top_threshold = self._parametersDock.topLE.text()
        self._step = self._parametersDock.step.text()
        self._chunks = [
            int(self._parametersDock.verticalChunkSize.text()),
            int(self._parametersDock.horizontalChunkSize.text()),
        ]
        self.setCentralWidget(self._sv)
        self.addDockWidget(
            qt.Qt.DockWidgetArea.BottomDockWidgetArea, self._parametersDock
        )

        # Add connections
        self._parametersDock.computeBS.clicked.connect(
            self._launchBackgroundSubtraction
        )
        self._parametersDock.computeHP.clicked.connect(self._launchHotPixelRemoval)
        self._parametersDock.computeTP.clicked.connect(self._launchThresholdRemoval)
        self._parametersDock.computeMR.clicked.connect(self._launchMaskRemoval)
        self._parametersDock.bsMethodsCB.currentTextChanged.connect(self._toggleMethod)
        self._parametersDock.bsBackgroundCB.currentIndexChanged.connect(
            self._toggleOnDiskWidget
        )
        self._operationHistory: list[NoiseRemovalOperation] = []

    def setDataset(self, owdataset: dtypes.OWDataset):
        """Saves the dataset and updates the stack with the dataset data."""
        self._parent = owdataset.parent
        self._dataset = owdataset.dataset
        self._output_dataset = owdataset.dataset
        self.indices = owdataset.indices
        if self._dataset.title != "":
            self._sv.setTitleCallback(lambda idx: self._dataset.title)
        self.setStack()
        self.bg_indices = owdataset.bg_indices
        self.bg_dataset = owdataset.bg_dataset

        self._parametersDock.computeBS.show()
        self._parametersDock.computeHP.show()
        self._parametersDock.computeTP.show()
        self._parametersDock.computeMR.show()

        """
        Sets the available background for the user to choose.
        """
        self._parametersDock.bsBackgroundCB.clear()
        if owdataset.bg_dataset is not None:
            self._parametersDock.bsBackgroundCB.addItem(BackgroundType.DARK_DATA.value)
        if owdataset.bg_indices is not None:
            self._parametersDock.bsBackgroundCB.addItem(
                BackgroundType.UNUSED_DATA.value
            )
        self._parametersDock.bsBackgroundCB.addItem(BackgroundType.DATA.value)

        # TODO: This fails when using a dataset with `in_memory=False`
        # self._parametersDock.topLE.setText(str(int(self._dataset.get_data().max()) + 1))

        self._operationHistory.clear()

    def _launchBackgroundSubtraction(self):
        self._background = self._parametersDock.bsBackgroundCB.currentText()

        if self._parametersDock.onDiskWidget.isVisible():
            if self._parametersDock.onDiskCheckbox.isChecked():
                self._step = None
                self._chunks = [
                    int(self._parametersDock.verticalChunkSize.text()),
                    int(self._parametersDock.horizontalChunkSize.text()),
                ]
            else:
                self._chunks = None
                self._step = int(self._parametersDock.step.text())
        else:
            self._step = None
            self._chunks = None

        self._method = self._parametersDock.bsMethodsCB.currentText()

        operation = NoiseRemovalOperation(
            type=Operation.BS,
            parameters={
                "method": self.method,
                "step": self._step,
                "chunks": self._chunks,
                "background_type": self._background,
            },
        )
        self._launchOperationInThread(operation)

    def _launchHotPixelRemoval(self):
        self._size = self._parametersDock.hpSizeCB.currentText()

        operation = NoiseRemovalOperation(
            type=Operation.HP,
            parameters={
                "kernel_size": int(self._size),
            },
        )
        self._launchOperationInThread(operation)

    def _launchThresholdRemoval(self):
        self._bottom_threshold = self._parametersDock.bottomLE.text()
        self._top_threshold = self._parametersDock.topLE.text()

        operation = NoiseRemovalOperation(
            type=Operation.THRESHOLD,
            parameters={
                "bottom": int(self._bottom_threshold),
                "top": int(self._top_threshold),
            },
        )
        self._launchOperationInThread(operation)

    def _launchMaskRemoval(self):
        if self._output_dataset is None:
            return
        mask = self.mask
        if mask is None:
            return
        operation = NoiseRemovalOperation(
            type=Operation.MASK,
            parameters={"mask": mask},
        )
        self._launchOperationInThread(operation)

    def _launchOperationInThread(self, operation: NoiseRemovalOperation):
        self._operationHistory.append(operation)
        if self._output_dataset is None:
            return
        self._thread = OperationThread(self, apply_noise_removal_operation)
        self._thread.setArgs(self.getDataset(self), operation)
        self._thread.finished.connect(self._updateData)
        self._thread.start()
        self._setComputingState(operation.type)

    def abortCurrentComputation(self):
        if self._current_operation is None or self._output_dataset is None:
            return
        self._output_dataset.stop_operation(self._current_operation)
        self._operationHistory.pop()

    def _setComputingState(self, operation: Operation | None):
        isComputing = bool(operation)
        self._parametersDock.computeBS.setDisabled(isComputing)
        self._parametersDock.computeHP.setDisabled(isComputing)
        self._parametersDock.computeTP.setDisabled(isComputing)
        self._parametersDock.computeMR.setDisabled(isComputing)

        self._current_operation = operation

        self.computingSignal.emit(isComputing)

    def _updateData(self):
        """
        Updates the stack with the data computed in the thread
        """
        try:
            self._thread.finished.disconnect(self._updateData)
        except TypeError as e:
            _logger.warning(e)
        self._setComputingState(None)
        if self._thread.data is not None:
            self.clearStack()
            self._output_dataset = self._thread.data
            self._thread.func = None
            self._thread.data = None
            self.setStack(self._output_dataset)
        else:
            print("\nComputation aborted")

    def _toggleMethod(self, text):
        if text == Method.mean.value:
            self._parametersDock.onDiskWidget.hide()
        elif text == Method.median.value:
            self._toggleOnDiskWidget(self._parametersDock.bsBackgroundCB.currentIndex())

    def _toggleOnDiskWidget(self, index):
        if self._dataset is None:
            return
        if self._parametersDock.bsMethodsCB.currentText() == Method.median.value:
            if self.bg_dataset is None:
                (
                    self._parametersDock.onDiskWidget.hide()
                    if self._dataset.in_memory
                    else self._parametersDock.onDiskWidget.show()
                )
            elif not (index or self.bg_dataset.in_memory) or (
                index and not self._dataset.in_memory
            ):
                self._parametersDock.onDiskWidget.show()
            else:
                self._parametersDock.onDiskWidget.hide()
        else:
            self._parametersDock.onDiskWidget.hide()

    def getDataset(self, parent) -> dtypes.OWDataset:
        if self._output_dataset is None:
            raise ValueError("Load a dataset before trying to get a new one !")
        return dtypes.OWDataset(
            parent=parent,
            dataset=self._output_dataset,
            indices=self.indices,
            bg_indices=self.bg_indices,
            bg_dataset=self.bg_dataset,
        )

    def _updateDataset(self, widget, dataset):
        self._dataset = dataset
        self._output_dataset = dataset
        if self._parent:
            self._parent._updateDataset(widget, dataset)

    def resetStack(self):
        self._operationHistory.clear()
        self._output_dataset = self._dataset
        self.setStack()

    def clearStack(self):
        self._sv.setStack(None)

    def getStack(self):
        stack = self._sv.getStack(copy=False, returnNumpyArray=True)
        if stack is None:
            return None
        return stack[0]

    def setStack(self, dataset=None):
        """
        Sets new data to the stack.
        Mantains the current frame showed in the view.

        :param Dataset dataset: if not None, data set to the stack will be from the given dataset.
        """
        new_dataset = dataset if dataset is not None else self._dataset
        if new_dataset is None:
            return
        old_nframe = self._sv.getFrameNumber()
        self._sv.setStack(new_dataset.get_data(self.indices))
        self._sv.setFrameNumber(old_nframe)

    def getStackViewColormap(self):
        """
        Returns the colormap from the stackView

        :rtype: silx.gui.colors.Colormap
        """
        return self._sv.getColormap()

    def setStackViewColormap(self, colormap):
        """
        Sets the stackView colormap

        :param colormap: Colormap to set
        :type colormap: silx.gui.colors.Colormap
        """
        self._sv.setColormap(colormap)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = size
        self._parametersDock.hpSizeCB.setCurrentText(size)

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, method):
        self._method = method
        self._parametersDock.bsMethodsCB.setCurrentText(method)

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, step):
        self._step = step
        if step is not None:
            self._parametersDock.step.setText(str(step))

    @property
    def chunks(self):
        return self._chunks

    @chunks.setter
    def chunks(self, chunks):
        self._chunks = chunks
        if chunks is not None:
            self._parametersDock.verticalChunkSize.setText(str(chunks[0]))
            self._parametersDock.horizontalChunkSize.setText(str(chunks[1]))

    @property
    def background(self):
        return self._background

    @background.setter
    def background(self, background):
        if self._parametersDock.bsBackgroundCB.findText(background) >= 0:
            self._background = background
            self._parametersDock.bsBackgroundCB.setCurrentText(background)

    @property
    def bottom_threshold(self):
        return self._bottom_threshold

    @bottom_threshold.setter
    def bottom_threshold(self, bottom):
        self._bottom_threshold = bottom
        self._parametersDock.bottomLE.setText(bottom)

    @property
    def top_threshold(self):
        return self._top_threshold

    @top_threshold.setter
    def top_threshold(self, top):
        self._top_threshold = top
        self._parametersDock.topLE.setText(top)

    @property
    def _dataset(self):
        return self._input_dataset

    @_dataset.setter
    def _dataset(self, dataset):
        self._input_dataset = dataset
        self.__clearMaskWithWrongShape()

    @property
    def mask(self):
        return self._svPlotWidget.getSelectionMask()

    @mask.setter
    def mask(self, mask):
        self.__storeMask(mask)
        self.__clearMaskWithWrongShape()

    def __storeMask(self, mask):
        if mask is None:
            self._svPlotWidget.clearMask()
        else:
            self._svPlotWidget.setSelectionMask(mask)

    @property
    def _svPlotWidget(self):
        return self._sv.getPlotWidget()

    def __clearMaskWithWrongShape(self):
        mask = self.mask
        if mask is None:
            return
        if self._dataset is None or self._dataset.data is None:
            return
        stack_shape = self._dataset.data.shape[-2:]
        mask_shape = mask.shape
        if stack_shape == mask_shape:
            return
        self.__storeMask(mask)
