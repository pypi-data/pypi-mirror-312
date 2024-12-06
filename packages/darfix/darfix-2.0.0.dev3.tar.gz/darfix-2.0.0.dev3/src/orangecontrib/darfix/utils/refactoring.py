"""module used to make ease refactoring"""

from typing import Union

from ewoksorange.bindings.owwidgets import OWEwoksWidgetOneThread, ow_build_opts
from ewokscore.variable import Variable
from darfix import dtypes


def fromOWSendDatasetToDataset(
    dataset: Union[dtypes.OWDataset, dtypes.OWSendDataset, dtypes.Dataset]
) -> dtypes.Dataset:
    """
    util function to handle compatibility between widgets
    """
    # Temp fix until https://gitlab.esrf.fr/workflow/ewoks/ewoksorange/-/merge_requests/169 is merged
    if isinstance(dataset, Variable):
        dataset = dataset.value

    if isinstance(dataset, dtypes.OWSendDataset):
        dataset, _ = dataset

    return dataset


def fromDatasetToOWSendDataset(
    dataset: Union[dtypes.OWDataset, dtypes.OWSendDataset, dtypes.Dataset], parent=None
) -> dtypes.OWSendDataset:
    """
    util function to handle compatibility between widgets
    """
    if isinstance(dataset, dtypes.Dataset):
        dataset = dtypes.OWDataset(
            dataset=dataset.dataset,
            indices=dataset.indices,
            bg_dataset=dataset.bg_dataset,
            bg_indices=dataset.bg_indices,
            parent=parent,
        )
    if isinstance(dataset, dtypes.OWDataset):
        dataset = dtypes.OWSendDataset(
            dataset=dataset,
            update=None,
        )
    return dataset


class OWDarfixWidgetOneThread(OWEwoksWidgetOneThread, **ow_build_opts):
    """A compatibility widget that takes care of converting Dataset (used in Ewoks) to OWSendDataset (used in Orange widgets) and vice-versa."""

    def get_task_inputs(self):
        # get task inputs handled directly by ewoksorange
        task_inputs = super().get_task_inputs()

        # compatibility with dataset type
        if "dataset" in task_inputs:
            task_inputs["dataset"] = fromOWSendDatasetToDataset(
                dataset=task_inputs.get("dataset")
            )
        return task_inputs

    def get_task_outputs(self):
        # backward compatibility.
        # for now widget expected to return instances of dtypes.OWSendDataset
        outputs = super().get_task_outputs()
        if "dataset" in outputs:
            outputs["dataset"].value = fromDatasetToOWSendDataset(
                dataset=outputs["dataset"].value
            )
        return outputs
