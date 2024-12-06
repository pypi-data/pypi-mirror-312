from __future__ import annotations

from ewokscore.missing_data import is_missing_data

from darfix.gui.grainPlotWidget import GrainPlotWidget
from darfix.tasks.grainplot import GrainPlot
from darfix import dtypes
from ..utils.refactoring import (
    OWDarfixWidgetOneThread,
    fromOWSendDatasetToDataset,
)


class GrainPlotWidgetOW(OWDarfixWidgetOneThread, ewokstaskclass=GrainPlot):
    """
    Computes moments (Center of mass, FWHM, Kurtosis, SKEWNESS) and displays them.

    Also computes mosaicity and orientation distribution for multi-dimensional datasets.
    """

    _ewoks_inputs_to_hide_from_orange = ("filename", "dimensions", "save_maps")

    name = "grain plot"
    icon = "icons/grainplot.png"
    description = "Computes Center of mass, FWHM, Kurtosis, Skewness, mosaicity (nD), orientation (nD) maps and displays them"
    want_main_area = True
    want_control_area = False

    def __init__(self):
        super().__init__()

        self._widget = GrainPlotWidget(parent=self)
        self.mainArea.layout().addWidget(self._widget)

    def get_task_inputs(self):
        task_inputs = super().get_task_inputs()

        # Saving is handled by the widget
        task_inputs["save_maps"] = False

        return task_inputs

    def handleNewSignals(self) -> None:
        dataset = self.get_task_input_value("dataset")
        self.setDataset(dataset, pop_up=True)
        # avoid calling 'handleNewSignals' execution is already called by 'setDataset'
        # super().handleNewSignals()

    def setDataset(self, owdataset: dtypes.OWDataset | None, pop_up=False):
        if owdataset is None or is_missing_data(owdataset):
            return

        dataset = owdataset

        if not isinstance(dataset, dtypes.OWDataset):
            raise TypeError(
                f"dataset is expected to be an instance of OWDataset. Got {type(owdataset)}."
            )

        self._widget.setDataset(dataset)
        self.execute_ewoks_task()
        if pop_up:
            self.open()

    def task_output_changed(self):
        dataset = self.get_task_output_value("dataset", None)

        if dataset is None:
            return

        if isinstance(dataset, dtypes.OWSendDataset):
            dataset = fromOWSendDatasetToDataset(dataset)
        if not isinstance(dataset, dtypes.Dataset):
            raise TypeError(
                f"dataset is expected to be an instance of {dtypes.Dataset}. Got {type(dataset)}."
            )
        self._widget.set_moments(dataset.dataset.moments_dims)

    def _updateDataset(self, widget, dataset):
        self._widget._updateDataset(widget, dataset)
