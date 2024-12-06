from __future__ import annotations

from darfix.gui.metadataWidget import MetadataWidget
from darfix.tasks.metadata import MetadataTask
from darfix import dtypes
from ewoksorange.bindings.owwidgets import OWEwoksWidgetNoThread
from ewokscore.missing_data import MISSING_DATA
from orangecontrib.darfix.utils.refactoring import fromOWSendDatasetToDataset


class MetadataWidgetOW(
    OWEwoksWidgetNoThread,
    ewokstaskclass=MetadataTask,
):
    """
    Widget to select the data to be used in the dataset.
    """

    name = "metadata"
    icon = "icons/metadata.svg"
    want_control_area = False
    want_main_area = True

    def __init__(self):
        super().__init__()

        self._widget = MetadataWidget()
        self.mainArea.layout().addWidget(self._widget)

    def setDataset(self, dataset: None | dtypes.OWSendDataset | dtypes.OWDataset):
        if dataset:
            if isinstance(dataset, dtypes.OWSendDataset):
                dataset, _ = dataset
            if dataset is None:
                self._widget.clearTable()
            else:
                self._widget.setDataset(dataset)

    def handleNewSignals(self) -> None:
        dataset = self.get_task_input_value("dataset", MISSING_DATA)
        if dataset is MISSING_DATA:
            return
        # handle compatibility between OWSendDataset, OWDataset...
        dataset = fromOWSendDatasetToDataset(dataset)
        self.setDataset(dataset)
        # this is a task only displaying metadata. there is no real processing.
        # return super().handleNewSignals()
