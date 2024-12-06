"""
Module for defining processes to be used by the library `ewoks`. Each of
the processes defined here can be used (its corresponding widgets) within an
Orange workflow and later be converted to an Ewoks workflow without the GUI part needed.
"""

import os
from typing import Any, List, Dict

import numpy
import string
import h5py

from silx.gui import qt

from ewokscore import Task
from ewoksutils.import_utils import qualname

from darfix.gui.rsmHistogramWidget import RSMHistogramWidget
from darfix.gui.rsmWidget import PixelSize
from darfix import dtypes


def generate_ewoks_task_inputs(task_class, **kwargs) -> List[Dict[str, Any]]:
    task_identifier = qualname(task_class)

    return [
        {"task_identifier": task_identifier, "name": name, "value": value}
        for name, value in kwargs.items()
    ]


class FlashTask(
    Task,
    input_names=["dataset"],
    output_names=["dataset"],
):
    def run(self):
        self.outputs.dataset = self.inputs.dataset


class DataPartition(
    Task,
    input_names=["dataset"],
    optional_input_names=["bins", "n_bins"],
    output_names=["dataset"],
):
    def run(self):
        dataset = self.inputs.dataset.dataset

        bins = self.inputs.bins if self.inputs.bins else None
        nbins = self.inputs.n_bins if self.inputs.n_bins else 1
        indices, bg_indices = dataset.partition_by_intensity(bins, nbins)
        self.outputs.dataset = dtypes.Dataset(
            dataset=dataset,
            indices=indices,
            bg_indices=bg_indices,
            bg_dataset=self.inputs.dataset.bg_dataset,
        )


class Transformation(
    Task,
    input_names=["dataset"],
    optional_input_names=[
        "magnification",
        "pixelSize",
        "kind",
        "rotate",
        "orientation",
    ],
    output_names=["dataset"],
):
    def run(self):
        dataset = self.inputs.dataset.dataset

        magnification = self.inputs.magnification if self.inputs.magnification else None
        orientation = self.inputs.orientation if self.inputs.orientation else None
        pixelSize = self.inputs.pixelSize if self.inputs.pixelSize else None
        kind = self.inputs.kind if self.inputs.kind else None
        rotate = self.inputs.rotate if self.inputs.rotate else None
        if dataset and dataset.dims.ndim:
            if dataset.dims.ndim == 1 and kind:
                dataset.compute_transformation(
                    PixelSize[pixelSize].value, kind="rsm", rotate=rotate
                )
            else:
                if orientation == -1 or orientation is None:
                    dataset.compute_transformation(magnification, topography=[False, 0])
                else:
                    dataset.compute_transformation(
                        magnification, topography=[True, orientation]
                    )
        self.outputs.dataset = dtypes.Dataset(
            dataset=dataset,
            indices=self.inputs.dataset.indices,
            bg_indices=self.inputs.dataset.bg_indices,
            bg_dataset=self.inputs.dataset.bg_dataset,
        )


class Projection(
    Task,
    input_names=["dataset"],
    optional_input_names=["dimension"],
    output_names=["dataset"],
):
    def run(self):
        dataset = self.inputs.dataset.dataset
        indices = self.inputs.dataset.indices

        dimension = self.inputs.dimension
        if dimension:
            dataset = dataset.project_data(dimension=dimension, indices=indices)
        self.outputs.dataset = dtypes.Dataset(
            dataset=dataset,
            indices=indices,
            bg_indices=self.inputs.dataset.bg_indices,
            bg_dataset=self.inputs.dataset.bg_dataset,
        )


class RSMHistogram(
    Task,
    input_names=["dataset"],
    optional_input_names=[
        "q",
        "a",
        "map_range",
        "detector",
        "units",
        "n",
        "map_shape",
        "energy",
    ],
    output_names=["dataset"],
):
    def run(self):
        # FIXME: no any QApplication should be defined in a task class
        app = qt.QApplication.instance() or qt.QApplication([])
        widget = RSMHistogramWidget()
        if self.inputs.dataset:
            owdataset = dtypes.OWDataset(None, *self.inputs.dataset)
            widget.setDataset(owdataset)
        widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        # TODO: Only show computed maps?
        if self.inputs.q:
            widget.q = self.inputs.q
        if self.inputs.a:
            widget.a = self.inputs.a
        if self.inputs.map_range:
            widget.map_range = self.inputs.map_range
        if self.inputs.detector:
            widget.detector = self.inputs.detector
        if self.inputs.units:
            widget.units = self.inputs.units
        if self.inputs.n:
            widget.n = self.inputs.n
        if self.inputs.map_shape:
            widget.map_shape = self.inputs.map_shape
        if self.inputs.energy:
            widget.energy = self.inputs.energy
        # FIXME: this a processing relative to GUI. This shouldn't appear here
        widget.show()
        app.exec_()
        self.outputs.dataset = dtypes.Dataset(
            dataset=self.inputs.dataset.dataset,
            indices=self.inputs.dataset.indices,
            bg_indices=self.inputs.dataset.bg_indices,
            bg_dataset=self.inputs.dataset.bg_dataset,
        )


class WeakBeam(
    Task,
    input_names=["dataset"],
    optional_input_names=["nvalue"],
    output_names=["dataset"],
):
    """
    Obtain dataset with filtered weak beam and recover its Center of Mass.
    Save file with this COM for further processing.
    """

    def run(self):
        dataset = self.inputs.dataset.dataset
        indices = self.inputs.dataset.indices

        nvalue = self.inputs.nvalue
        if nvalue:
            wb_dataset = dataset.recover_weak_beam(nvalue, indices=indices)
            com = wb_dataset.apply_moments(indices=indices)[0][0]
            filename = os.path.join(dataset.dir, "weakbeam_{}.hdf5".format(nvalue))
            # FIXME: file reading should be done with a context manager
            try:
                _file = h5py.File(filename, "a")
            except OSError:
                if os.path.exists(filename):
                    os.path.remove(filename)
                _file = h5py.File(filename, "w")
            if dataset.title is None:
                letters = string.ascii_lowercase
                result_str = "".join(
                    numpy.random.choice(list(letters)) for i in range(6)
                )
                _file[result_str] = com
            else:
                if dataset.title in _file:
                    del _file[dataset.title]
                _file[dataset.title] = com
            _file.close()

        self.outputs.dataset = dtypes.Dataset(
            dataset=dataset,
            indices=indices,
            bg_indices=self.inputs.dataset.bg_indices,
            bg_dataset=self.inputs.dataset.bg_dataset,
        )
