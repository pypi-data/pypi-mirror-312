import pytest
import numpy
import os

from darfix.tests import utils
from darfix.core.dataset import ImageDataset, Data
from darfix.core.dimension import Dimension, POSITIONER_METADATA
import h5py
from silx.io.url import DataUrl

try:
    from importlib.resources import files as resource_files
except ImportError:
    from importlib_resources import files as resource_files
import darfix.resources.tests
from darfix.dtypes import Dataset


@pytest.fixture
def dataset_args():
    """ "
    Creating random dataset with specific headers.
    """
    counter_mne = "a b c d e f g h"
    motor_mne = "obpitch y z mainx ffz m obx"
    dims = (20, 100, 100)
    # Create headers
    header = []
    # Dimensions for reshaping
    a = numpy.random.rand(2)
    b = numpy.random.rand(5)
    c = numpy.random.rand(2)
    motors = numpy.random.rand(7)
    for i in numpy.arange(20):
        header.append({})
        header[i]["HeaderID"] = i
        header[i]["counter_mne"] = counter_mne
        header[i]["motor_mne"] = motor_mne
        header[i]["counter_pos"] = ""
        header[i]["motor_pos"] = ""
        for count in counter_mne:
            header[i]["counter_pos"] += str(numpy.random.rand(1)[0]) + " "
        for j, m in enumerate(motor_mne.split()):
            if m == "z":
                header[i]["motor_pos"] += (
                    str(a[int((i > 4 and i < 10) or i > 14)]) + " "
                )
            elif m == "m":
                header[i]["motor_pos"] += str(b[i % 5]) + " "
            elif m == "obpitch":
                header[i]["motor_pos"] += str(c[int(i > 9)]) + " "
            elif m == "mainx":
                header[i]["motor_pos"] += "50 "
            else:
                header[i]["motor_pos"] += str(motors[j]) + " "

    data = numpy.zeros(dims)
    background = numpy.random.random(dims)
    idxs = [0, 2, 4]
    data[idxs] += background[idxs]
    return utils.DatasetArgs(data=data, header=header)


@pytest.fixture
def in_memory_dataset(tmpdir, dataset_args):
    return utils.createDataset(
        data=dataset_args.data,
        header=dataset_args.header,
        _dir=str(tmpdir),
        backend="edf",
    )


@pytest.fixture
def on_disk_dataset(tmpdir, dataset_args):
    return utils.createDataset(
        data=dataset_args.data,
        header=dataset_args.header,
        _dir=str(tmpdir),
        in_memory=False,
        backend="edf",
    )


def test_add_one_dimension(in_memory_dataset, on_disk_dataset):
    """Tests the correct add of a dimension"""

    dimension = Dimension(POSITIONER_METADATA, "test", 20)
    # In memory
    in_memory_dataset.add_dim(0, dimension)
    saved_dimension = in_memory_dataset.dims.get(0)
    assert saved_dimension.name == "test"
    assert saved_dimension.kind == POSITIONER_METADATA
    assert saved_dimension.size == 20

    # On disk
    on_disk_dataset.add_dim(0, dimension)
    saved_dimension = on_disk_dataset.dims.get(0)
    assert saved_dimension.name == "test"
    assert saved_dimension.kind == POSITIONER_METADATA
    assert saved_dimension.size == 20


def test_add_several_dimensions(in_memory_dataset, on_disk_dataset):
    """Tests the correct add of several dimensions"""

    dimension1 = Dimension(POSITIONER_METADATA, "test1", 20)
    dimension2 = Dimension(POSITIONER_METADATA, "test2", 30)
    dimension3 = Dimension(POSITIONER_METADATA, "test3", 40)

    # In memory
    in_memory_dataset.add_dim(0, dimension1)
    in_memory_dataset.add_dim(1, dimension2)
    in_memory_dataset.add_dim(2, dimension3)
    assert in_memory_dataset.dims.ndim == 3

    # On disk
    on_disk_dataset.add_dim(0, dimension1)
    on_disk_dataset.add_dim(1, dimension2)
    on_disk_dataset.add_dim(2, dimension3)
    assert on_disk_dataset.dims.ndim == 3


def test_remove_dimension(in_memory_dataset, on_disk_dataset):
    """Tests the correct removal of a dimension"""

    dimension = Dimension(POSITIONER_METADATA, "test", 20)

    # In memory
    in_memory_dataset.add_dim(0, dimension)
    in_memory_dataset.remove_dim(0)
    assert in_memory_dataset.dims.ndim == 0

    # On disk
    on_disk_dataset.add_dim(0, dimension)
    on_disk_dataset.remove_dim(0)
    assert on_disk_dataset.dims.ndim == 0


def test_remove_dimensions(in_memory_dataset, on_disk_dataset):
    """Tests the correct removal of several dimensions"""

    dimension1 = Dimension(POSITIONER_METADATA, "test1", 20)
    dimension2 = Dimension(POSITIONER_METADATA, "test2", 30)
    dimension3 = Dimension(POSITIONER_METADATA, "test3", 40)

    # In memory
    in_memory_dataset.add_dim(0, dimension1)
    in_memory_dataset.add_dim(1, dimension2)
    in_memory_dataset.add_dim(2, dimension3)
    in_memory_dataset.remove_dim(0)
    in_memory_dataset.remove_dim(2)
    assert in_memory_dataset.dims.ndim == 1
    assert in_memory_dataset.dims.get(1).name == "test2"

    # On disk
    on_disk_dataset.add_dim(0, dimension1)
    on_disk_dataset.add_dim(1, dimension2)
    on_disk_dataset.add_dim(2, dimension3)
    on_disk_dataset.remove_dim(0)
    on_disk_dataset.remove_dim(2)
    assert on_disk_dataset.dims.ndim == 1
    assert on_disk_dataset.dims.get(1).name == "test2"


def test_find_dimensions(in_memory_dataset, on_disk_dataset):
    """Tests the correct finding of the dimensions"""

    # In memory
    in_memory_dataset.find_dimensions(POSITIONER_METADATA)
    assert in_memory_dataset.dims.ndim == 3
    assert in_memory_dataset.dims.get(0).name == "m"
    assert in_memory_dataset.dims.get(1).name == "z"
    assert in_memory_dataset.dims.get(2).name == "obpitch"

    # On disk
    on_disk_dataset.find_dimensions(POSITIONER_METADATA)
    assert on_disk_dataset.dims.ndim == 3
    assert on_disk_dataset.dims.get(0).name == "m"
    assert on_disk_dataset.dims.get(1).name == "z"
    assert on_disk_dataset.dims.get(2).name == "obpitch"


def test_reshaped_data(in_memory_dataset, on_disk_dataset):
    """Tests the correct reshaping of the data"""

    # In memory
    in_memory_dataset.find_dimensions(POSITIONER_METADATA)
    dataset = in_memory_dataset.reshape_data()
    assert dataset.data.shape == (2, 2, 5, 100, 100)

    # On disk
    on_disk_dataset.find_dimensions(POSITIONER_METADATA)
    dataset = on_disk_dataset.reshape_data()
    assert dataset.data.shape == (2, 2, 5, 100, 100)


def test_find_shift(in_memory_dataset, on_disk_dataset):
    """Tests the shift detection with dimensions and indices"""

    # In memory
    in_memory_dataset.find_dimensions(POSITIONER_METADATA)
    dataset = in_memory_dataset.reshape_data()
    indices = [1, 2, 3, 4]
    shift = dataset.find_shift(dimension=[1, 1], indices=indices)
    assert len(shift) == 0
    shift = dataset.find_shift(dimension=[0, 1], indices=indices)
    assert shift.shape == (2, 1)

    # On disk
    on_disk_dataset.find_dimensions(POSITIONER_METADATA)
    dataset = on_disk_dataset.reshape_data()
    indices = [1, 2, 3, 4]
    shift = dataset.find_shift(dimension=[1, 1], indices=indices)
    assert len(shift) == 0
    shift = dataset.find_shift(dimension=[0, 1], indices=indices)
    assert shift.shape == (2, 1)


def test_apply_shift(in_memory_dataset, on_disk_dataset):
    """Tests the shift correction with dimensions and indices"""

    # In memory
    in_memory_dataset.find_dimensions(POSITIONER_METADATA)
    dataset = in_memory_dataset.reshape_data()
    new_dataset = dataset.apply_shift(
        shift=numpy.array([[0, 0.5], [0, 0.5]]),
        dimension=[0, 1],
        indices=[1, 2, 3, 4],
    )
    assert new_dataset.data.urls[0, 0, 0] == dataset.data.urls[0, 0, 0]
    assert new_dataset.data.urls[0, 0, 1] != dataset.data.urls[0, 0, 1]

    #  On disk
    on_disk_dataset.find_dimensions(POSITIONER_METADATA)
    dataset = on_disk_dataset.reshape_data()
    new_dataset = dataset.apply_shift(
        shift=numpy.array([[0, 0.5], [0, 0.5]]),
        dimension=[0, 1],
        indices=[1, 2, 3, 4],
    )

    assert new_dataset.data.urls[0, 0, 0] == dataset.data.urls[0, 0, 0]
    assert new_dataset.data.urls[0, 0, 1] != dataset.data.urls[0, 0, 1]


def test_find_shift_along_dimension(in_memory_dataset, on_disk_dataset):
    """Tests the shift detection along a dimension"""

    # In memory
    in_memory_dataset.find_dimensions(POSITIONER_METADATA)
    dataset = in_memory_dataset.reshape_data()
    indices = numpy.arange(10)
    shift = dataset.find_shift_along_dimension(dimension=[1], indices=indices)
    assert shift.shape == (2, 2, 5)
    shift = dataset.find_shift_along_dimension(dimension=[0], indices=indices)
    assert shift.shape == (5, 2, 2)

    # On disk
    on_disk_dataset.find_dimensions(POSITIONER_METADATA)
    dataset = on_disk_dataset.reshape_data()
    indices = numpy.arange(10)
    shift = dataset.find_shift_along_dimension(dimension=[1], indices=indices)
    assert shift.shape == (2, 2, 5)
    shift = dataset.find_shift_along_dimension(dimension=[0], indices=indices)
    assert shift.shape == (5, 2, 2)


def test_apply_shift_along_dimension(in_memory_dataset, on_disk_dataset):
    """Tests the shift correction with dimensions and indices"""

    # In memory
    in_memory_dataset.find_dimensions(POSITIONER_METADATA)
    dataset = in_memory_dataset.reshape_data()
    shift = numpy.random.random((4, 2, 2))
    new_dataset = dataset.apply_shift_along_dimension(
        shift=shift, dimension=[1], indices=[1, 2, 3, 4]
    )
    assert new_dataset.data.urls[0, 0, 0] == dataset.data.urls[0, 0, 0]
    assert new_dataset.data.urls[0, 0, 1] != dataset.data.urls[0, 0, 1]
    #  On disk
    on_disk_dataset.find_dimensions(POSITIONER_METADATA)
    dataset = on_disk_dataset.reshape_data()
    shift = numpy.random.random((4, 2, 2))
    new_dataset = dataset.apply_shift_along_dimension(
        shift=shift, dimension=[1], indices=[1, 2, 3, 4]
    )

    assert new_dataset.data.urls[0, 0, 0] == dataset.data.urls[0, 0, 0]
    assert new_dataset.data.urls[0, 0, 1] != dataset.data.urls[0, 0, 1]


def test_zsum(in_memory_dataset, on_disk_dataset):
    """Tests the shift detection with dimensions and indices"""

    indices = [1, 2, 3, 6]
    # In memory
    in_memory_dataset.find_dimensions(POSITIONER_METADATA)
    dataset = in_memory_dataset.reshape_data()
    result = numpy.sum(dataset.get_data(dimension=[0, 1], indices=indices), axis=0)
    zsum = dataset.zsum(dimension=[0, 1], indices=indices)
    numpy.testing.assert_array_equal(zsum, result)

    # On disk
    on_disk_dataset.find_dimensions(POSITIONER_METADATA)
    dataset = on_disk_dataset.reshape_data()
    zsum = dataset.zsum(dimension=[0, 1], indices=indices)
    numpy.testing.assert_array_equal(zsum, result)


def test_apply_2d_fit(in_memory_dataset, on_disk_dataset):
    """Tests the fit with dimensions and indices"""

    # In memory
    data = Data(
        urls=in_memory_dataset.get_data().urls[:10],
        metadata=in_memory_dataset.get_data().metadata[:10],
        in_memory=True,
    )
    dataset = ImageDataset(_dir=in_memory_dataset.dir, data=data)
    dataset.find_dimensions(POSITIONER_METADATA)
    dataset = dataset.reshape_data()
    new_dataset, maps = dataset.apply_fit(indices=[1, 2, 3, 4])
    assert new_dataset.data.urls[0, 0] == dataset.data.urls[0, 0]
    assert new_dataset.data.urls[0, 1] != dataset.data.urls[0, 1]
    assert len(maps) == 7
    assert maps[0].shape == in_memory_dataset.get_data(0).shape

    #  On disk
    data = Data(
        urls=on_disk_dataset.get_data().urls[:10],
        metadata=on_disk_dataset.get_data().metadata[:10],
        in_memory=False,
    )
    dataset = ImageDataset(_dir=on_disk_dataset.dir, data=data)
    dataset.find_dimensions(POSITIONER_METADATA)
    dataset = dataset.reshape_data()
    new_dataset, maps = dataset.apply_fit(indices=[1, 2, 3, 4])

    assert new_dataset.data.urls[0, 0] == dataset.data.urls[0, 0]
    assert new_dataset.data.urls[0, 1] != dataset.data.urls[0, 1]
    assert len(maps) == 7
    assert maps[0].shape == in_memory_dataset.get_data(0).shape


def test_data_reshaped_data(in_memory_dataset, on_disk_dataset):
    """Tests that data and reshaped data have same values"""

    # In memory
    in_memory_dataset.find_dimensions(POSITIONER_METADATA)
    dataset = in_memory_dataset.reshape_data()
    numpy.testing.assert_array_equal(dataset.get_data(0), in_memory_dataset.get_data(0))

    # On disk
    on_disk_dataset.find_dimensions(POSITIONER_METADATA)
    dataset = on_disk_dataset.reshape_data()
    numpy.testing.assert_array_equal(dataset.get_data(0), on_disk_dataset.get_data(0))


def test_clear_dimensions(in_memory_dataset, on_disk_dataset):
    """Tests the clear dimensions function"""

    # In memory
    in_memory_dataset.find_dimensions(POSITIONER_METADATA)
    in_memory_dataset.clear_dims()
    assert in_memory_dataset.dims.ndim == 0

    # On disk
    on_disk_dataset.find_dimensions(POSITIONER_METADATA)
    on_disk_dataset.clear_dims()
    assert on_disk_dataset.dims.ndim == 0


def test_apply_moments_in_memory(in_memory_dataset, on_disk_dataset):
    """Tests finding moments"""

    # In memory
    in_memory_dataset.find_dimensions(POSITIONER_METADATA)
    dataset = in_memory_dataset.reshape_data()
    moments = dataset.apply_moments(indices=[1, 2, 3, 4])
    assert moments[0][0].shape == dataset.get_data(0).shape
    assert moments[1][3].shape == dataset.get_data(0).shape

    #  On disk
    on_disk_dataset.find_dimensions(POSITIONER_METADATA)
    dataset = on_disk_dataset.reshape_data()
    moments = dataset.apply_moments(indices=[1, 2, 3, 4])
    assert moments[0][0].shape == dataset.get_data(0).shape
    assert moments[1][3].shape == dataset.get_data(0).shape


def test_compute_magnification(in_memory_dataset, on_disk_dataset):
    """Tests fitting data in memory"""

    # In memory
    in_memory_dataset.find_dimensions(POSITIONER_METADATA)
    dataset = in_memory_dataset.reshape_data()
    dataset.compute_transformation(d=0.1)
    assert dataset.transformation.shape == dataset.get_data(0).shape

    #  On disk
    on_disk_dataset.find_dimensions(POSITIONER_METADATA)
    dataset = on_disk_dataset.reshape_data()
    dataset.compute_transformation(d=0.1)
    assert dataset.transformation.shape == dataset.get_data(0).shape


def test_find_dimension_silicon_111_reflection(tmp_path):
    """
    Test 'find_dimension' with a bunch of motor position over a real use cases that used to bring troubles.
    """
    silicon_111_reflection_file = resource_files(darfix.resources.tests).joinpath(
        os.path.join("dimensions_definition", "silicon_111_reflection.h5")
    )

    raw_motor_values = {}
    with h5py.File(silicon_111_reflection_file, mode="r") as h5f:
        raw_motor_values["chi"] = h5f["positioners/chi"][()]
        raw_motor_values["mu"] = h5f["positioners/mu"][()]

    data_folder = tmp_path / "test_fitting"
    data_folder.mkdir()
    data_file_url = DataUrl(
        file_path=os.path.join(str(data_folder), "data.h5"),
        data_path="data",
        scheme="silx",
    )
    number_of_points = 1891
    with h5py.File(data_file_url.file_path(), mode="w") as h5f:
        h5f["data"] = numpy.random.random(number_of_points)

    dataset = Dataset(
        dataset=ImageDataset(
            first_filename=data_file_url.path(),
            metadata_url=DataUrl(
                file_path=str(silicon_111_reflection_file),
                data_path="positioners",
                scheme="silx",
            ).path(),
            isH5=True,
            _dir=None,
            in_memory=False,
        )
    )
    image_dataset = dataset.dataset

    # with a tolerance of 10e-9 we won't find 1081 steps over 2 dimensions
    assert len(image_dataset.dims) == 0
    image_dataset.find_dimensions(kind=None, tolerance=1e-9)
    assert len(image_dataset.dims) == 2
    assert (
        numpy.prod([val.size for val in image_dataset.dims.values()]) > number_of_points
    )

    image_dataset.clear_dims()
    image_dataset.find_dimensions(kind=None, tolerance=1e-5)
    assert (
        numpy.prod([val.size for val in image_dataset.dims.values()])
        == number_of_points
    )
    for dim in image_dataset.dims.values():
        numpy.testing.assert_almost_equal(
            dim.range[0], min(raw_motor_values[dim.name]), decimal=3
        )
        numpy.testing.assert_almost_equal(
            dim.range[1], max(raw_motor_values[dim.name]), decimal=3
        )


def test_find_dimension_NiTi_1PD_002_g411_420MPa_mosalayers_2x(tmp_path):
    """
    Test 'find_dimension' with a bunch of motor position over a real use cases that used to bring troubles.
    """
    dataset_file = resource_files(darfix.resources.tests).joinpath(
        os.path.join(
            "dimensions_definition", "NiTi_1PD_002_g411_420MPa_mosalayers_2x.h5"
        )
    )

    raw_motor_values = {}
    with h5py.File(dataset_file, mode="r") as h5f:
        raw_motor_values["chi"] = h5f["positioners/chi"][()]
        raw_motor_values["diffry"] = h5f["positioners/diffry"][()]
        raw_motor_values["difftz"] = h5f["positioners/difftz"][()]

    data_folder = tmp_path / "test_fitting"
    data_folder.mkdir()
    data_file_url = DataUrl(
        file_path=os.path.join(str(data_folder), "data.h5"),
        data_path="data",
        scheme="silx",
    )
    number_of_points = 31500
    with h5py.File(data_file_url.file_path(), mode="w") as h5f:
        h5f["data"] = numpy.random.random(number_of_points)

    dataset = Dataset(
        dataset=ImageDataset(
            first_filename=data_file_url.path(),
            metadata_url=DataUrl(
                file_path=str(dataset_file),
                data_path="positioners",
                scheme="silx",
            ).path(),
            isH5=True,
            _dir=None,
            in_memory=False,
        )
    )
    image_dataset = dataset.dataset

    def check_dimensions_bounds(dims: dict):
        """Make sure find_dimension is correctly fitting motor bounds"""
        for dim in dims.values():
            numpy.testing.assert_almost_equal(
                dim.range[0], min(raw_motor_values[dim.name]), decimal=3
            )
            numpy.testing.assert_almost_equal(
                dim.range[1], max(raw_motor_values[dim.name]), decimal=3
            )

    # with a tolerance of 10e-9 we won't find 1081 steps over 2 dimensions
    assert len(image_dataset.dims) == 0
    image_dataset.find_dimensions(kind=None, tolerance=1e-5)
    assert len(image_dataset.dims) == 3
    check_dimensions_bounds(dims=image_dataset.dims)
    assert (
        numpy.prod([val.size for val in image_dataset.dims.values()]) > number_of_points
    )

    image_dataset.clear_dims()
    image_dataset.find_dimensions(kind=None, tolerance=1e-4)
    assert len(image_dataset.dims) == 3
    check_dimensions_bounds(dims=image_dataset.dims)
    assert (
        numpy.prod([val.size for val in image_dataset.dims.values()])
        == number_of_points
    )
