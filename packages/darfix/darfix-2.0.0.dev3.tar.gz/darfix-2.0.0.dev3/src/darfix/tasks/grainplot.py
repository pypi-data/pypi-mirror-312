import os

from silx.io.dictdump import dicttonx
from ewokscore import Task

from .. import dtypes
from ..core.dataset import ImageDataset
from ..core.grainplot import (
    OrientationDistImage,
    compute_mosaicity,
    compute_orientation_dist_data,
    generate_grain_maps_nxdict,
    get_image_parameters,
)


class GrainPlot(
    Task,
    input_names=["dataset"],
    optional_input_names=["filename", "dimensions", "save_maps"],
    output_names=["dataset"],
):
    """Generates and saves maps of Center of Mass, FWHM, Skewness, Kurtosis, Orientation distribution and Mosaicity"""

    def run(self):
        input_dataset: dtypes.Dataset = self.inputs.dataset
        default_filename = os.path.join(input_dataset.dataset._dir, "maps.h5")
        filename: str = self.get_input_value("filename", default_filename)
        dimensions: tuple[int, int] = self.get_input_value("dimensions", (0, 1))
        save_maps: bool = self.get_input_value("save_maps", True)

        dataset: ImageDataset = input_dataset.dataset
        dataset.apply_moments()
        moments = dataset.moments_dims

        if dataset.dims.ndim > 1:
            xdim = dataset.dims.get(dimensions[1])
            ydim = dataset.dims.get(dimensions[0])
            if xdim is None or ydim is None:
                raise ValueError(
                    f"Could not find dimensions {dimensions} in {dataset.dims.__dims.keys()}"
                )
            mosaicity = compute_mosaicity(moments, dimensions[0], dimensions[1])
            # TODO: What should third_motor be here ?
            orientation_dist_data = compute_orientation_dist_data(
                dataset, dimensions=dimensions, third_motor=0
            )
            assert orientation_dist_data is not None
            # TODO: What should origin be here ?
            image_parameters = get_image_parameters(xdim, ydim, origin="dims")
            orientation_dist_image = OrientationDistImage(
                xlabel=image_parameters.xlabel,
                ylabel=image_parameters.ylabel,
                scale=image_parameters.scale,
                origin=image_parameters.origin,
                data=orientation_dist_data.data,
                as_rgb=orientation_dist_data.as_rgb,
                contours={},
            )
        else:
            mosaicity = None
            orientation_dist_image = None

        # Save data if asked
        if save_maps:
            nxdict = generate_grain_maps_nxdict(
                dataset, moments, mosaicity, orientation_dist_image
            )
            dicttonx(nxdict, filename)

        self.outputs.dataset = dtypes.Dataset(
            dataset=dataset,
            indices=input_dataset.indices,
            bg_indices=input_dataset.bg_indices,
            bg_dataset=input_dataset.bg_dataset,
        )
