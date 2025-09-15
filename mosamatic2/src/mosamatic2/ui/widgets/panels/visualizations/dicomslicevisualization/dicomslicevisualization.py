from mosamatic2.ui.widgets.panels.visualizations.dicomslicevisualization.multistyleinteractor import MultiStyleInteractor
from mosamatic2.ui.widgets.panels.visualizations.visualization import Visualization


class DicomSliceVisualization(Visualization):
    """
    DicomSliceVisualization

    This visualization can load a single NIFTI volume and display it as a stack of slices
    through which you can scroll. You can also add a mask volume, possibly with multiple
    labels, that will be shown as an overlay.
    """
    def __init__(self):
        super(DicomSliceVisualization, self).__init__()