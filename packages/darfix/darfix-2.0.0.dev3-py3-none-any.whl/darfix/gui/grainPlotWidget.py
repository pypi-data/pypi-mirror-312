from __future__ import annotations
import numpy
import logging

from silx.gui import qt
from silx.gui.colors import Colormap
from silx.gui.plot.items import ImageBase
from silx.gui.plot import Plot2D
from silx.image.marchingsquares import find_contours
from silx.utils.enum import Enum as _Enum
from silx.io.dictdump import dicttonx

from .. import dtypes
from ..core.grainplot import (
    MomentType,
    MultiDimMomentType,
    OrientationDistData,
    OrientationDistImage,
    compute_mosaicity,
    compute_orientation_dist_data,
    generate_grain_maps_nxdict,
    get_image_parameters,
    get_third_motor_index,
)
from .chooseDimensions import ChooseDimensionWidget
from ewoksorange.gui.parameterform import block_signals

_logger = logging.getLogger(__file__)


class MapType(_Enum):
    """
    Different maps to show
    """

    COM = MomentType.COM.value
    FWHM = MomentType.FWHM.value
    SKEWNESS = MomentType.SKEWNESS.value
    KURTOSIS = MomentType.KURTOSIS.value
    ORIENTATION_DIST = MultiDimMomentType.ORIENTATION_DIST.value
    MOSAICITY = MultiDimMomentType.MOSAICITY.value


class GrainPlotWidget(qt.QMainWindow):
    """
    Widget to show a series of maps for the analysis of the data.
    """

    def __init__(self, parent=None):
        qt.QMainWindow.__init__(self, parent)

        self._mapTypeComboBox = qt.QComboBox()
        self._mapTypeComboBox.addItems(MapType.values())
        for i in range(len(MapType)):
            self._mapTypeComboBox.model().item(i).setEnabled(False)
        self._mapTypeComboBox.currentTextChanged.connect(self._updatePlot)
        self._plotWidget = qt.QWidget()
        plotsLayout = qt.QHBoxLayout()
        self._plotWidget.setLayout(plotsLayout)
        self._contoursPlot = Plot2D(parent=self)
        widget = qt.QWidget(parent=self)
        layout = qt.QVBoxLayout()
        self._levelsWidget = qt.QWidget()
        levelsLayout = qt.QGridLayout()
        levelsLabel = qt.QLabel("Number of levels:")
        self._levelsLE = qt.QLineEdit("20")
        self._levelsLE.setToolTip("Number of levels to use when finding the contours")
        self._levelsLE.setValidator(qt.QIntValidator())
        self._computeContoursB = qt.QPushButton("Compute")
        self._motorValuesCheckbox = qt.QCheckBox("Use motor values")
        self._motorValuesCheckbox.setChecked(True)
        self._motorValuesCheckbox.stateChanged.connect(self._update_orientation_image)
        self._centerDataCheckbox = qt.QCheckBox("Center angle values")
        self._centerDataCheckbox.setEnabled(False)
        self._centerDataCheckbox.stateChanged.connect(self._update_orientation_image)
        self._chooseDimensionWidget = ChooseDimensionWidget(
            self, vertical=False, values=False, _filter=False
        )
        self._chooseDimensionWidget.filterChanged.connect(self._updateMotorAxis)
        self._thirdMotorCB = qt.QComboBox(self)
        self._thirdMotorCB.currentIndexChanged.connect(self._updateThirdMotor)
        levelsLayout.addWidget(levelsLabel, 0, 0, 1, 1)
        levelsLayout.addWidget(self._levelsLE, 0, 1, 1, 1)
        levelsLayout.addWidget(self._motorValuesCheckbox, 0, 2, 1, 1)
        levelsLayout.addWidget(self._centerDataCheckbox, 0, 3, 1, 1)
        levelsLayout.addWidget(self._thirdMotorCB, 1, 2, 1, 1)
        levelsLayout.addWidget(self._computeContoursB, 1, 3, 1, 1)
        levelsLayout.addWidget(self._contoursPlot, 2, 0, 1, 4)
        self._levelsWidget.setLayout(levelsLayout)
        self._levelsWidget.hide()
        self._mosaicityPlot = Plot2D(parent=self)
        self._exportButton = qt.QPushButton("Export maps")
        self._exportButton.setEnabled(False)
        self._exportButton.clicked.connect(self.exportMaps)
        layout.addWidget(self._mapTypeComboBox)
        layout.addWidget(self._chooseDimensionWidget)
        layout.addWidget(self._levelsWidget)
        layout.addWidget(self._plotWidget)
        layout.addWidget(self._mosaicityPlot)
        layout.addWidget(self._exportButton)
        self._plotWidget.hide()
        self._thirdMotorCB.hide()
        self._chooseDimensionWidget.hide()
        self._mosaicityPlot.hide()
        self._mosaicityPlot.getColorBarWidget().hide()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self._orientation_dist_data: OrientationDistData | None = None
        self._mosaicity: numpy.ndarray | None = None
        self._moments: numpy.ndarray | None = None
        self.dimensions: tuple[int, int] = (0, 1)
        self._plots = []

    def setDataset(self, owdataset: dtypes.OWDataset):
        self._parent = owdataset.parent
        self.dataset = owdataset.dataset

        with block_signals(self._mapTypeComboBox):
            for i in range(len(MapType)):
                self._mapTypeComboBox.model().item(i).setEnabled(False)

        self._curves = {}
        if self.dataset.dims.ndim == 3:
            # Update chooseDimensionWidget and thirdMotorCB
            with block_signals(self._chooseDimensionWidget):
                self._chooseDimensionWidget.setDimensions(self.dataset.dims)
                self._chooseDimensionWidget._updateState(True)
            self._thirdMotorCB.clear()
            third_motor = self.dataset.dims.get(
                get_third_motor_index(self._chooseDimensionWidget.dimension)
            )
            with block_signals(self._thirdMotorCB):
                self._thirdMotorCB.addItems(
                    numpy.array(third_motor.unique_values, dtype=str)
                )

        # allow orientation if ndim >= 2
        if self.dataset.dims.ndim >= 2:
            self._update_orientation_image()
            self._contoursPlot.getColorBarWidget().hide()

            self._computeContoursB.clicked.connect(self._computeContours)
            self._mapTypeComboBox.model().item(4).setEnabled(True)
            self._mapTypeComboBox.setCurrentIndex(4)

        for i in reversed(range(self._plotWidget.layout().count())):
            self._plotWidget.layout().itemAt(i).widget().setParent(None)

        self._contoursPlot.setGraphTitle(
            self.dataset.title + "\n" + MapType.ORIENTATION_DIST.value
        )
        self._mosaicityPlot.setGraphTitle(
            self.dataset.title + "\n" + MapType.MOSAICITY.value
        )
        self._plots.clear()
        for dim in self.dataset.dims.values():
            plot = Plot2D(parent=self)
            plot.setGraphTitle(self.dataset.title + "\n" + dim.name)
            plot.setDefaultColormap(Colormap(name="viridis"))
            self._plots.append(plot)
            self._plotWidget.layout().addWidget(plot)

    def set_moments(self, moments):
        self._moments = moments
        self._updatePlot(self._mapTypeComboBox.currentText())
        rg = len(MapType) if self.dataset.dims.ndim > 1 else 4
        for i in range(rg):
            self._mapTypeComboBox.model().item(i).setEnabled(True)
        self.mosaicity = self.compute_mosaicity()
        self._orientation_dist_data = compute_orientation_dist_data(
            self.dataset, third_motor=0
        )
        self._update_orientation_image()
        self._mapTypeComboBox.setCurrentIndex(0)
        self._exportButton.setEnabled(True)

    def _updateDataset(self, widget, dataset):
        self._parent._updateDataset(widget, dataset)
        self.dataset = dataset

    def _update_orientation_image(self, state=None):
        if self._orientation_dist_data is None:
            return

        self._centerDataCheckbox.setEnabled(not self._motorValuesCheckbox.isChecked())
        self._contoursPlot.remove(kind="curve")
        self._contoursPlot.resetZoom()

        if self._motorValuesCheckbox.isChecked():
            origin = "dims"
        elif self._centerDataCheckbox.isChecked():
            origin = "center"
        else:
            origin = None

        xdim = self.dataset.dims.get(self.dimensions[1])
        ydim = self.dataset.dims.get(self.dimensions[0])
        image_params = get_image_parameters(xdim, ydim, origin)

        self._contoursPlot.addImage(
            self._orientation_dist_data.as_rgb,
            xlabel=image_params.xlabel,
            ylabel=image_params.ylabel,
            origin=image_params.origin,
            scale=image_params.scale,
        )

    def _computeContours(self):
        """
        Compute contours map based on orientation distribution.
        """
        self._contoursPlot.remove(kind="curve")
        orientation_image_plot: ImageBase | None = self._contoursPlot.getImage()

        if self._orientation_dist_data is None or orientation_image_plot is None:
            return

        min_orientation = numpy.min(self._orientation_dist_data.data)
        max_orientation = numpy.max(self._orientation_dist_data.data)

        polygons = []
        levels = []
        for i in numpy.linspace(
            min_orientation, max_orientation, int(self._levelsLE.text())
        ):
            polygons.append(find_contours(self._orientation_dist_data.data, i))
            levels.append(i)

        colormap = Colormap(
            name="temperature", vmin=min_orientation, vmax=max_orientation
        )
        colors = colormap.applyToData(levels)
        xdim = self.dataset.dims.get(self.dimensions[1])
        ydim = self.dataset.dims.get(self.dimensions[0])
        self._curves = {}
        for ipolygon, polygon in enumerate(polygons):
            # iso contours
            for icontour, contour in enumerate(polygon):
                if len(contour) == 0:
                    continue
                # isClosed = numpy.allclose(contour[0], contour[-1])
                x = contour[:, 1]
                y = contour[:, 0]
                xscale = xdim.range[2]
                yscale = ydim.range[2]
                x_pts = orientation_image_plot.getOrigin()[0] + x * xscale + xscale / 2
                y_pts = orientation_image_plot.getOrigin()[1] + y * yscale + yscale / 2
                legend = "poly{}.{}".format(icontour, ipolygon)
                self._curves[legend] = {
                    "points": (x_pts.copy(), y_pts.copy()),
                    "color": colors[ipolygon],
                    "value": levels[ipolygon],
                    "pixels": (x, y),
                }
                self._contoursPlot.addCurve(
                    x=x_pts,
                    y=y_pts,
                    linestyle="-",
                    linewidth=2.0,
                    legend=legend,
                    resetzoom=False,
                    color=colors[ipolygon],
                )

    def compute_mosaicity(self):
        """
        Compute mosaicity map depending on the selected dimensions, if any.
        """
        if self._moments is not None and self.dataset.dims.ndim > 1:
            return compute_mosaicity(
                self._moments, self.dimensions[0], self.dimensions[1]
            )

    def _updatePlot(self, raw_map_type: str):
        """
        Update shown plots in the widget
        """
        self._levelsWidget.hide()
        self._mosaicityPlot.hide()
        self._thirdMotorCB.hide()
        self._chooseDimensionWidget.hide()

        map_type = MapType(raw_map_type)
        if map_type == MapType.ORIENTATION_DIST:
            self._levelsWidget.show()
            self._plotWidget.hide()
            if self.dataset.dims.ndim == 3:
                self._chooseDimensionWidget.show()
                self._thirdMotorCB.show()
        elif map_type == MapType.FWHM:
            self._plotWidget.show()
            for i, plot in enumerate(self._plots):
                self._addImage(plot, self._moments[i][1])
        elif map_type == MapType.COM:
            self._plotWidget.show()
            for i, plot in enumerate(self._plots):
                self._addImage(plot, self._moments[i][0])
        elif map_type == MapType.SKEWNESS:
            self._plotWidget.show()
            for i, plot in enumerate(self._plots):
                self._addImage(plot, self._moments[i][2])
        elif map_type == MapType.KURTOSIS:
            self._plotWidget.show()
            for i, plot in enumerate(self._plots):
                self._addImage(plot, self._moments[i][3])
        elif map_type == MapType.MOSAICITY:
            try:
                self._plotWidget.hide()
                self._addImage(self._mosaicityPlot, self.mosaicity)
                self._mosaicityPlot.show()
                if self.dataset.dims.ndim == 3:
                    self._chooseDimensionWidget.show()
            except Exception as e:
                _logger.error("Couldn't compute mosaicity: ", e)
        else:
            _logger.warning("Unexisting map method")

    def _updateMotorAxis(self):
        """
        Update dimensions used for orientation distribution and mosaicity maps.
        This is only used on datasets with more than two dimensions.
        """

        self.dimensions = self._chooseDimensionWidget.dimension
        self.mosaicity = self.compute_mosaicity()

        self._thirdMotorCB.clear()
        third_motor = self.dataset.dims.get(get_third_motor_index(self.dimensions))

        state = self._thirdMotorCB.blockSignals(True)
        self._thirdMotorCB.addItems(numpy.array(third_motor.unique_values, dtype=str))
        self._thirdMotorCB.blockSignals(state)
        self._update_orientation_image()

        self._orientation_dist_data = compute_orientation_dist_data(
            self.dataset, dimensions=self.dimensions, third_motor=0
        )

        self._updatePlot(self._mapTypeComboBox.currentText())

    def _updateThirdMotor(self, index=-1):
        """
        Update orientation distribution according to the third motor chosen
        """
        if index > -1:
            self._orientation_dist_data = compute_orientation_dist_data(
                self.dataset,
                dimensions=self._chooseDimensionWidget.dimension,
                third_motor=index,
            )
            self._updatePlot(self._mapTypeComboBox.currentText())

    def _generate_maps_nxdict(self) -> dict:
        orientation_image_plot: ImageBase | None = self._contoursPlot.getImage()

        if orientation_image_plot and self._orientation_dist_data:
            orientation_dist_image = OrientationDistImage(
                data=self._orientation_dist_data.data,
                as_rgb=self._orientation_dist_data.as_rgb,
                origin=orientation_image_plot.getOrigin(),
                scale=orientation_image_plot.getScale(),
                xlabel=orientation_image_plot.getXLabel(),
                ylabel=orientation_image_plot.getYLabel(),
                contours=self._curves,
            )
        else:
            orientation_dist_image = None

        return generate_grain_maps_nxdict(
            self.dataset, self._moments, self.mosaicity, orientation_dist_image
        )

    def exportMaps(self):
        """
        Creates dictionary with maps information and exports it to a nexus file
        """
        nx = self._generate_maps_nxdict()

        fileDialog = qt.QFileDialog()

        fileDialog.setFileMode(fileDialog.AnyFile)
        fileDialog.setAcceptMode(fileDialog.AcceptSave)
        fileDialog.setOption(fileDialog.DontUseNativeDialog)
        fileDialog.setDefaultSuffix(".h5")
        if fileDialog.exec_():
            dicttonx(nx, fileDialog.selectedFiles()[0])

    def _addImage(self, plot, image):
        if self.dataset.transformation is None:
            plot.addImage(image, xlabel="pixels", ylabel="pixels")
            return
        if self.dataset.transformation.rotate:
            image = numpy.rot90(image, 3)
        plot.addImage(
            image,
            origin=self.dataset.transformation.origin,
            scale=self.dataset.transformation.scale,
            xlabel=self.dataset.transformation.label,
            ylabel=self.dataset.transformation.label,
        )
