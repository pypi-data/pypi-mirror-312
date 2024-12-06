from typing import NamedTuple, Optional
from dataclasses import dataclass

import numpy
from ewoksorange.bindings.owwidgets import OWWidget
from silx.gui import qt

from darfix.core.dataset import ImageDataset


@dataclass
class Dataset:
    """Darfix dataset with indices and background"""

    dataset: ImageDataset  # Darfix dataset object that holds the image stack
    indices: Optional[numpy.ndarray] = (
        None  # Image stack indices to be taking into account. Usually set by the 'partition data' task
    )
    bg_indices: Optional[numpy.ndarray] = (
        None  # Dark image stack indices to be taking into account. Usually set by the 'partition data' task
    )
    bg_dataset: Optional[ImageDataset] = (
        None  # Darfix dataset object that holds the dark image stack
    )


@dataclass
class OWDataset(Dataset):
    """Darfix dataset with indices and background and associated Orange widget"""

    parent: Optional[OWWidget] = None  # Orange widget corresponding to an ewoks task


class OWSendDataset(NamedTuple):
    """Object send between Orange widgets"""

    dataset: OWDataset  # Resulting dataset with associated widget
    update: Optional[qt.QWidget] = None  # ???
