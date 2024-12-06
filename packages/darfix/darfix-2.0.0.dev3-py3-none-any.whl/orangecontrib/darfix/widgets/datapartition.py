__authors__ = ["J. Garriga"]
__license__ = "MIT"
__date__ = "28/09/2020"

from typing import Optional

from ewoksorange.gui.orange_imports import Setting, Input, Output
from ewoksorange.bindings.owwidgets import OWWidget

from darfix.gui.dataPartitionWidget import DataPartitionWidget
from darfix.core.process import DataPartition
from darfix import dtypes


class DataPartitionWidgetOW(OWWidget):
    """
    Widget that computes the background substraction from a dataset
    """

    name = "partition data"
    icon = "icons/filter.png"
    want_main_area = False
    ewokstaskclass = DataPartition

    # Inputs
    class Inputs:
        dataset = Input("dataset", dtypes.OWSendDataset)

    # Outputs
    class Outputs:
        dataset = Output("dataset", dtypes.OWSendDataset)

    bins = Setting(str(), schema_only=True)
    bottom_bins = Setting(str(), schema_only=True)
    top_bins = Setting(str(), schema_only=True)

    def __init__(self):
        super().__init__()

        self._widget = DataPartitionWidget(parent=self)
        self._widget.sigComputed.connect(self._sendSignal)
        self.controlArea.layout().addWidget(self._widget)

    @Inputs.dataset
    def setDataset(self, _input: Optional[dtypes.OWSendDataset]):
        if _input is not None:
            dataset, update = _input
            self._widget.setDataset(dataset)
            if update is None:
                self.open()
            if self.bins:
                self._widget.bins.setText(self.bins)
            if self.bottom_bins:
                self._widget.bottomBinsNumber.setText(self.bottom_bins)
            if self.top_bins:
                self._widget.topBinsNumber.setText(self.top_bins)

    def _sendSignal(self):
        owdataset = self._widget.getDataset(self)
        senddataset = dtypes.OWSendDataset(owdataset)
        self.Outputs.dataset.send(senddataset)
        self.bins = self._widget.bins.text()
        self.bottom_bins = self._widget.bottomBinsNumber.text()
        self.top_bins = self._widget.topBinsNumber.text()
        self.close()

    def _updateDataset(self, widget, dataset):
        self._widget._updateDataset(widget, dataset)
