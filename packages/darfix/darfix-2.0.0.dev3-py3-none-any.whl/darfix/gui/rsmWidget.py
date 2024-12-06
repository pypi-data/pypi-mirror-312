__authors__ = ["J. Garriga"]
__license__ = "MIT"
__date__ = "16/07/2021"


from silx.gui import qt
from silx.utils.enum import Enum as _Enum

from darfix import dtypes


class PixelSize(_Enum):
    """
    Different pixel sizes
    """

    Basler = 0.051
    PcoEdge_2x = 0.00375
    PcoEdge_10x = 0.00075


class RSMWidget(qt.QMainWindow):
    """
    Widget to transform axes of RSM data
    """

    sigComputed = qt.Signal()

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)

        self._rotate = False
        self._moments = None
        self._pixelSize = None
        self.dataset = None

        widget = qt.QWidget()
        layout = qt.QGridLayout()

        pixelSizeLabel = qt.QLabel("Pixel size: ")
        self._pixelSizeCB = qt.QComboBox()
        self._pixelSizeCB.addItems(PixelSize.names())
        self._rotateCB = qt.QCheckBox("Rotate RSM", self)
        self._okButton = qt.QPushButton("Ok")
        self._okButton.setEnabled(False)
        self._okButton.pressed.connect(self._saveRSM)
        layout.addWidget(pixelSizeLabel, 0, 0)
        layout.addWidget(self._pixelSizeCB, 0, 1)
        layout.addWidget(self._rotateCB, 1, 1)
        layout.addWidget(self._okButton, 2, 0, 1, 2)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def setDataset(self, owdataset: dtypes.OWDataset):
        self.parent = owdataset.parent
        self.dataset = owdataset.dataset
        self.indices = owdataset.indices
        self.bg_indices = owdataset.bg_indices
        self.bg_dataset = owdataset.bg_dataset
        self._okButton.setEnabled(True)

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

    @property
    def pixelSize(self):
        return self._pixelSize

    @pixelSize.setter
    def pixelSize(self, pixelSize):
        self._pixelSize = pixelSize
        self._pixelSizeCB.setCurrentText(str(pixelSize))

    @property
    def rotate(self):
        return self._rotate

    @rotate.setter
    def rotate(self, rotate):
        self._rotate = rotate
        self._rotateCB.setChecked(rotate)

    def _saveRSM(self):
        self._pixelSize = self._pixelSizeCB.currentText()
        self._rotate = self._rotateCB.isChecked()
        self.dataset.compute_transformation(
            PixelSize[self._pixelSize].value, kind="rsm", rotate=self._rotate
        )
        self.sigComputed.emit()
