import os
from ewoksorange.tests.conftest import qtapp  # noqa F401
from orangecontrib.darfix.widgets.transformation import TransformationWidgetOW
from darfix.gui.magnificationWidget import MagnificationWidget

from darfix.core.dataset import ImageDataset
from silx.io.url import DataUrl

try:
    from importlib.resources import files as resource_files
except ImportError:
    from importlib_resources import files as resource_files
import darfix.resources.tests
from darfix.dtypes import OWDataset, OWSendDataset


def test_TransformationWidgetOW(
    qtapp,  # noqa F811
):
    _316H_dummy_insitu_g1_RSM_2 = str(
        resource_files(darfix.resources.tests).joinpath(
            os.path.join("transformation", "316H_dummy_insitu_g1_RSM_2.h5")
        )
    )

    data_file_url = DataUrl(
        file_path=_316H_dummy_insitu_g1_RSM_2,
        data_path="/1.1/measurement/basler_ff",
        scheme="silx",
    )

    dataset = OWDataset(
        dataset=ImageDataset(
            first_filename=data_file_url.path(),
            metadata_url=DataUrl(
                file_path=str(_316H_dummy_insitu_g1_RSM_2),
                data_path="/1.1/instrument/positioners",
                scheme="silx",
            ).path(),
            isH5=True,
            _dir=None,
            in_memory=False,
        ),
        parent=None,
    )
    dataset.dataset.find_dimensions(kind=None)

    widget = TransformationWidgetOW()
    widget.setDataset(
        OWSendDataset(
            dataset=dataset,
        )
    )
    sub_wiget = widget._widget
    assert isinstance(sub_wiget, MagnificationWidget)
    # check transformation has been correctly computed.
    assert dataset.dataset.transformation is None
    widget._widget._saveMagnification()
    assert dataset.dataset.transformation is not None
