from __future__ import annotations

from ewokscore.missing_data import MISSING_DATA
from ewokscore.missing_data import is_missing_data
from ewoksorange.bindings.owwidgets import OWEwoksWidgetOneThread


from darfix.dtypes import Dataset
from darfix.gui.PCAWidget import PCAPlot
from darfix.tasks.pca import PCA
from orangecontrib.darfix.utils.refactoring import fromOWSendDatasetToDataset


class PCAWidgetOW(OWEwoksWidgetOneThread, ewokstaskclass=PCA):
    name = "PCA"
    description = "A widget to perform principal component analysis"
    icon = "icons/pca.png"
    want_main_area = True
    want_control_area = False

    _ewoks_inputs_to_hide_from_orange = ("chunk_size", "num_components")

    def __init__(self):
        super().__init__()

        self._plot = PCAPlot(parent=self)
        self.mainArea.layout().addWidget(self._plot)

    def get_task_inputs(self):
        task_inputs = super().get_task_inputs()

        if "dataset" in task_inputs:
            task_inputs["dataset"] = fromOWSendDatasetToDataset(
                dataset=task_inputs.get("dataset", MISSING_DATA)
            )

        return task_inputs

    def task_output_changed(self) -> None:
        vals = self.get_task_output_value("vals")
        dataset: Dataset | None = self.get_task_output_value("dataset", None)

        if is_missing_data(vals):
            self._plot.clear()
        else:
            self._plot.setData(vals, dataset.dataset.title if dataset else None)
        return super().task_output_changed()

    def handleNewSignals(self) -> None:
        super().handleNewSignals()
        self.open()
