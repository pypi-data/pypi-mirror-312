from __future__ import annotations

from silx.gui import qt
from silx.utils.enum import Enum as _Enum
from ewoksorange.gui.parameterform import block_signals

from darfix import dtypes


class Value(_Enum):
    """"""

    PIXEL_2X = 3.25
    PIXEL_10X = 0.65


class Orientation(_Enum):
    VERTICAL = "Vertical"
    HORIZONTAL = "Horizontal"


class MagnificationWidget(qt.QMainWindow):
    """
    Widget to apply magnification transformation to the data axes.
    """

    sigComputed = qt.Signal()

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)

        widget = qt.QWidget()
        layout = qt.QVBoxLayout()
        self._magnificationFactorWidget = _MagnificationFactorWidget(parent=self)
        layout.addWidget(self._magnificationFactorWidget)

        self._topographyCheckbox = qt.QCheckBox("Topography (obpitch)")
        self._centerAxesCheckbox = qt.QCheckBox("Center axes")
        self._centerAxesCheckbox.setChecked(True)
        self._orientationCB = qt.QComboBox()
        self._orientationCB.addItems(Orientation.values())
        topographyAxis = qt.QLabel("Topography axis: ")

        self._okButton = qt.QPushButton("Ok")
        self._okButton.setEnabled(False)
        self._okButton.pressed.connect(self._saveMagnification)
        layout.addWidget(self._topographyCheckbox, alignment=qt.Qt.AlignRight)
        self._topographyWidget = qt.QWidget()
        topographyLayout = qt.QHBoxLayout()
        topographyLayout.addWidget(topographyAxis)
        topographyLayout.addWidget(self._orientationCB)
        self._topographyWidget.setLayout(topographyLayout)
        self._topographyWidget.hide()
        self._topographyWidget.setMaximumHeight(40)
        layout.addWidget(self._topographyWidget, alignment=qt.Qt.AlignRight)
        layout.addWidget(self._okButton)
        layout.addWidget(self._centerAxesCheckbox)

        spacer = qt.QWidget(parent=self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        layout.addWidget(spacer)

        # self._okButton.pressed.connect(self._saveMagnification)
        self._topographyCheckbox.toggled.connect(self._checkTopography)

        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def setDataset(self, owdataset: dtypes.OWDataset):
        self.parent = owdataset.parent
        self.dataset = owdataset.dataset
        self.indices = owdataset.indices
        self.bg_indices = owdataset.bg_indices
        self.bg_dataset = owdataset.bg_dataset

        if not self.dataset.dims:
            msg = qt.QMessageBox()
            msg.setIcon(qt.QMessageBox.Warning)
            msg.setText(
                "This widget has to be used before selecting any region of \
                         interest and after selecting the dimensions"
            )
            msg.exec_()
        else:
            self._okButton.setEnabled(True)

    @property
    def magnification(self):
        return self._magnificationFactorWidget.getMagnification()

    @property
    def orientation(self):
        if self._topographyCheckbox.isChecked():
            return self._orientationCB.currentIndex()
        else:
            return -1

    @orientation.setter
    def orientation(self, orientation):
        if orientation != -1:
            self._topographyCheckbox.setChecked(True)
            self._orientationCB.setCurrentIndex(orientation)

    @magnification.setter
    def magnification(self, magnification: float):
        self._magnificationFactorWidget.setMagnification(magnification=magnification)

    def getDataset(self, parent) -> dtypes.OWDataset:
        return dtypes.OWDataset(
            parent=parent,
            dataset=self.dataset,
            indices=self.indices,
            bg_indices=self.bg_indices,
            bg_dataset=self.bg_dataset,
        )

    def _updateDataset(self, widget, dataset):
        self.parent._updateDataset(widget, dataset)
        self.dataset = dataset

    def _checkTopography(self, checked: bool):
        if checked:
            self._topographyWidget.show()
        else:
            self._topographyWidget.hide()

    def _saveMagnification(self):
        print("save magnification", self.magnification)
        self.dataset.compute_transformation(
            self.magnification,
            topography=[
                self._topographyCheckbox.isChecked(),
                self._orientationCB.currentIndex(),
            ],
            center=self._centerAxesCheckbox.isChecked(),
        )

        self.sigComputed.emit()


class _MagnificationFactorWidget(qt.QWidget):
    """
    Widget to define a magnification
    """

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        layout = qt.QGridLayout()

        self.setLayout(layout)
        layout.addWidget(qt.QLabel("magnification: ", self), 0, 0, 2, 1)

        self._magnificationQSB = qt.QDoubleSpinBox(parent=self)
        self._magnificationQSB.setMinimum(0)
        self._magnificationQSB.setSingleStep(0.1)
        self._magnificationQSB.setDecimals(2)
        layout.addWidget(self._magnificationQSB, 0, 1, 2, 1)

        buttons_font = self.font()
        buttons_font.setPixelSize(10)

        self._2xMagnificationRB = qt.QPushButton("2x magnification")
        layout.addWidget(
            self._2xMagnificationRB,
            0,
            2,
            1,
            1,
        )
        self._2xMagnificationRB.setCheckable(True)
        self._2xMagnificationRB.setFont(buttons_font)
        self._2xMagnificationRB.setFocusPolicy(qt.Qt.NoFocus)

        self._10xMagnificationRB = qt.QPushButton("10x magnification")
        layout.addWidget(
            self._10xMagnificationRB,
            1,
            2,
            1,
            1,
        )
        self._10xMagnificationRB.setCheckable(True)
        self._10xMagnificationRB.setFont(buttons_font)
        self._10xMagnificationRB.setFocusPolicy(qt.Qt.NoFocus)

        # connect signal / slot
        self._2xMagnificationRB.released.connect(
            lambda: self.setMagnification(Value.PIXEL_2X.value)
        )

        self._10xMagnificationRB.released.connect(
            lambda: self.setMagnification(Value.PIXEL_10X.value)
        )
        self._magnificationQSB.editingFinished.connect(self._updateCheckedButton)

        # set up
        self.setMagnification(Value.PIXEL_2X.value)

    def getMagnification(self) -> float:
        return self._magnificationQSB.value()

    def setMagnification(self, magnification: float | str):
        magnification = float(magnification)
        self._magnificationQSB.setValue(magnification)
        self._updateCheckedButton()

    def _updateCheckedButton(self):
        magnification = self.getMagnification()
        with block_signals(self._2xMagnificationRB):
            self._2xMagnificationRB.setChecked(magnification == Value.PIXEL_2X.value)

        with block_signals(self._10xMagnificationRB):
            self._10xMagnificationRB.setChecked(magnification == Value.PIXEL_10X.value)
