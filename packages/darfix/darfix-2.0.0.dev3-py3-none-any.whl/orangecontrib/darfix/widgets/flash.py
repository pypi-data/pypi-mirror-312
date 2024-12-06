__authors__ = ["J. Garriga"]
__license__ = "MIT"
__date__ = "12/08/2019"

from typing import Optional

from ewoksorange.bindings.owwidgets import OWWidget
from ewoksorange.gui.orange_imports import Input, Output

from darfix.core.process import FlashTask
from darfix import dtypes


class FlashWidgetOW(OWWidget):
    """
    Widget that creates a new dataset from a given one, and copies its data.
    """

    name = "flash"
    icon = "icons/flash.svg"
    want_main_area = False
    ewokstaskclass = FlashTask

    # Inputs
    class Inputs:
        dataset = Input("dataset", dtypes.OWSendDataset)

    # Outputs
    class Outputs:
        dataset = Output("dataset", dtypes.OWSendDataset)

    def __init__(self):
        super().__init__()

    @Inputs.dataset
    def setDataset(self, _input: Optional[dtypes.OWSendDataset]):
        if _input is not None:
            if not isinstance(_input, dtypes.OWSendDataset):
                raise TypeError(
                    f"_input is expected to be an instance of {dtypes.OWSendDataset}. Got {type(_input)} instead."
                )
            # Copy and send new dataset
            self.dataset, _ = _input
            darfix_dataset = self.dataset.dataset
            widget = self.dataset.parent

            widget._updateDataset(
                widget=widget,
                dataset=darfix_dataset,
            )
            owdataset = dtypes.OWDataset(
                parent=self,
                dataset=self.dataset.dataset,
                indices=self.dataset.indices,
                bg_dataset=self.dataset.bg_dataset,
                bg_indices=self.dataset.bg_indices,
            )
            senddataset = dtypes.OWSendDataset(owdataset)
            self.Outputs.dataset.send(senddataset)

    def _updateDataset(self, widget, dataset):
        owdataset = dtypes.OWDataset(
            parent=self,
            dataset=dataset,
            indices=self.dataset.indices,
            bg_dataset=self.dataset.bg_dataset,
            bg_indices=self.dataset.bg_indices,
        )
        senddataset = dtypes.OWSendDataset(owdataset, widget)
        self.Outputs.dataset.send(senddataset)
