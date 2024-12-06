__authors__ = ["J. Garriga"]
__license__ = "MIT"
__date__ = "11/05/2020"

import numpy

from silx.gui import qt
from silx.gui.plot import Plot1D

from .operationThread import OperationThread
from darfix.core.dataset import Operation
from darfix import dtypes
from darfix.gui.utils.message import missing_dataset_msg


class DataPartitionWidget(qt.QMainWindow):
    sigComputed = qt.Signal()

    def __init__(self, parent=None):
        qt.QMainWindow.__init__(self, parent)
        self._dataset = None

        self._plot = Plot1D()

        binsLabel = qt.QLabel("Number of histogram bins:")
        filterRangeLabel = qt.QLabel("Filter range:")
        self.bins = qt.QLineEdit("")
        self.bins.setToolTip(
            "Defines the number of equal-width bins in the given range for the histogram"
        )
        self.bins.setValidator(qt.QIntValidator())
        self.bottomBinsNumber = qt.QLineEdit("")
        self.bottomBinsNumber.setPlaceholderText("First bin")
        self.bottomBinsNumber.setToolTip(
            "Minimum bin to use. It is 0 if nothing is entered."
        )
        self.topBinsNumber = qt.QLineEdit("")
        self.topBinsNumber.setPlaceholderText("Last bin")
        self.topBinsNumber.setToolTip(
            "Maximum bin to use. It is the number of bins if nothing is entered"
        )
        self.bottomBinsNumber.setValidator(qt.QIntValidator())
        self.topBinsNumber.setValidator(qt.QIntValidator())
        self.computeHistogram = qt.QPushButton("Compute histogram")
        self.computePartition = qt.QPushButton("Filter")
        self.abortB = qt.QPushButton("Abort")
        self.abortB.hide()
        self.computeHistogram.pressed.connect(self._computeHistogram)
        self.computePartition.pressed.connect(self._computePartition)
        self.abortB.pressed.connect(self.abort)
        widget = qt.QWidget(parent=self)
        layout = qt.QGridLayout()
        layout.addWidget(binsLabel, 0, 0, 1, 1)
        layout.addWidget(self.bins, 0, 1, 1, 1)
        layout.addWidget(filterRangeLabel, 1, 0, 1, 1)
        layout.addWidget(self.bottomBinsNumber, 1, 1)
        layout.addWidget(self.topBinsNumber, 1, 2)
        layout.addWidget(self.computeHistogram, 0, 2, 1, 1)
        layout.addWidget(self.computePartition, 2, 2, 1, 1)
        layout.addWidget(self.abortB, 3, 2, 1, 1)
        layout.addWidget(self._plot, 3, 0, 1, 3)
        widget.setLayout(layout)
        widget.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
        self.setCentralWidget(widget)
        self._plot.hide()

    def _computeHistogram(self):
        if self._dataset is None:
            missing_dataset_msg()
            return
        self.computeHistogram.setEnabled(False)
        self.computePartition.setEnabled(False)
        self.abortB.show()
        try:
            self._thread = OperationThread(self, self._dataset.compute_frames_intensity)
            self._thread.finished.connect(self._showHistogram)
            self._thread.start()
        except Exception as e:
            self.computeHistogram.setEnabled(True)
            raise e

    def _computePartition(self):
        if self._dataset is None:
            missing_dataset_msg()
            return
        self.computeHistogram.setEnabled(False)
        self.computePartition.setEnabled(False)
        self.abortB.show()
        try:
            self._thread = OperationThread(self, self._dataset.partition_by_intensity)
            self._thread.setArgs(
                bins=int(self.bins.text()),
                bottom_bin=(
                    int(self.bottomBinsNumber.text())
                    if self.bottomBinsNumber.text() != ""
                    else None
                ),
                top_bin=(
                    int(self.topBinsNumber.text())
                    if self.topBinsNumber.text() != ""
                    else None
                ),
            )
            self._thread.finished.connect(self._filterData)
            self._thread.start()
        except Exception as e:
            self.computePartition.setEnabled(True)
            raise e

    def abort(self):
        self.abortB.setEnabled(False)
        self._dataset.stop_operation(Operation.PARTITION)

    def setDataset(self, owdataset: dtypes.OWDataset):
        self.parent = owdataset.parent
        self._dataset = owdataset.dataset
        self.indices = owdataset.indices
        self.bg_indices = owdataset.bg_indices
        self.bg_dataset = owdataset.bg_dataset
        self.bins.setText(str(self._dataset.nframes))

    def _updateDataset(self, widget, dataset):
        del self._dataset
        self._dataset = dataset
        self._update_dataset = dataset
        self.parent._updateDataset(widget, dataset)

    def _showHistogram(self):
        """
        Plots the eigenvalues.
        """
        self._thread.finished.disconnect(self._showHistogram)
        self.abortB.hide()
        self.abortB.setEnabled(True)
        self.computePartition.setEnabled(True)
        self.computeHistogram.setEnabled(True)
        if self._thread.data is not None:
            frames_intensity = self._thread.data
            self._plot.remove()
            self._plot.show()
            values, bins = numpy.histogram(
                frames_intensity, numpy.arange(int(self.bins.text()))
            )
            self._plot.addHistogram(values, bins, fill=True)
        else:
            print("\nComputation aborted")

    def _filterData(self):
        """
        Plots the eigenvalues.
        """
        self._thread.finished.disconnect(self._filterData)
        self.abortB.hide()
        self.abortB.setEnabled(True)
        self.computeHistogram.setEnabled(True)
        self.computePartition.setEnabled(True)
        if self._thread.data is not None:
            self.indices, self.bg_indices = self._thread.data
            self.sigComputed.emit()
        else:
            print("\nComputation aborted")

    def getDataset(self, parent) -> dtypes.OWDataset:
        return dtypes.OWDataset(
            parent=parent,
            dataset=self._dataset,
            indices=self.indices,
            bg_indices=self.bg_indices,
            bg_dataset=self.bg_dataset,
        )
