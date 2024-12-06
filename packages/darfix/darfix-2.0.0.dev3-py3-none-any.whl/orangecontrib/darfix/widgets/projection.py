__authors__ = ["J. Garriga"]
__license__ = "MIT"
__date__ = "09/12/2021"

from typing import Optional

from ewoksorange.bindings.owwidgets import OWWidget
from ewoksorange.gui.orange_imports import Setting, Input, Output

from darfix.gui.projectionWidget import ProjectionWidget
from darfix.core.process import Projection
from darfix import dtypes


class ProjectionWidgetOW(OWWidget):
    """
    Widget that computes the background substraction from a dataset
    """

    name = "projection"
    # icon = "icons/projection.png"
    want_main_area = False
    ewokstaskclass = Projection

    # Inputs
    class Inputs:
        dataset = Input("dataset", dtypes.OWSendDataset)

    # Outputs
    class Outputs:
        dataset = Output("dataset", dtypes.OWSendDataset)

    dimension = Setting(int)

    def __init__(self):
        super().__init__()

        self._widget = ProjectionWidget(parent=self)
        self._widget.sigComputed.connect(self._sendSignal)
        self.controlArea.layout().addWidget(self._widget)

    @Inputs.dataset
    def setDataset(self, _input: Optional[dtypes.OWSendDataset]):
        if _input is not None:
            dataset, update = _input
            self._widget.setDataset(dataset)

            if update is None:
                self.open()
            elif update != self:
                owdataset = self._widget.getDataset(self)
                senddataset = dtypes.OWSendDataset(owdataset, update)
                self.Outputs.dataset.send(senddataset)

            if self.dimension:
                self._widget.dimension = self.dimension

    def _updateDataset(self, widget, dataset):
        self._widget._updateDataset(widget, dataset)

    def _sendSignal(self):
        """
        Function to emit the new dataset.
        """
        self.dimension = self._widget.dimension
        owdataset = self._widget.getDataset(self)
        senddataset = dtypes.OWSendDataset(owdataset)
        self.Outputs.dataset.send(senddataset)
        self.close()
