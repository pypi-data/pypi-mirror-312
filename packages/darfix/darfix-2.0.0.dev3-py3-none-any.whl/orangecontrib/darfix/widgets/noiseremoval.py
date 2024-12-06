from __future__ import annotations


from ewoksorange.gui.orange_imports import Input, Output
from silx.gui.colors import Colormap


from darfix.gui.noiseremoval.noiseRemovalWidget import NoiseRemovalDialog
from darfix.tasks.noiseremoval import NoiseRemoval
from darfix import dtypes
from ..utils.refactoring import OWDarfixWidgetOneThread


class NoiseRemovalWidgetOW(OWDarfixWidgetOneThread, ewokstaskclass=NoiseRemoval):
    name = "noise removal"
    description = "A widget to perform various noise removal operations"
    icon = "icons/noise_removal.png"
    want_main_area = True
    want_control_area = False

    _ewoks_inputs_to_hide_from_orange = ("operations",)

    # Inputs
    class Inputs:
        colormap = Input("colormap", Colormap)

    # Outputs
    class Outputs:
        colormap = Output("colormap", Colormap)

    def __init__(self):
        super().__init__()

        self._widget = NoiseRemovalDialog(parent=self)
        self.mainArea.layout().addWidget(self._widget)
        self._widget.okSignal.connect(self.execute_noise_removal_operations)

    def handleNewSignals(self) -> None:
        dataset = self.get_task_input_value("dataset")
        self.setDataset(dataset, pop_up=True)

        # Do not call super().handleNewSignals() to prevent propagation

    def setDataset(self, dataset: dtypes.Dataset | None, pop_up=True):
        if dataset is None:
            return
        self._widget.setDataset(dataset)
        if pop_up:
            self.open()

    @Inputs.colormap
    def setColormap(self, colormap):
        self._widget.mainWindow.setStackViewColormap(colormap)

    def task_output_changed(self) -> None:
        self.Outputs.colormap.send(self._widget.mainWindow.getStackViewColormap())
        self.close()

    def execute_noise_removal_operations(self) -> None:
        self.set_default_input("operations", self._widget.getOperationHistory())
        self.execute_ewoks_task()
