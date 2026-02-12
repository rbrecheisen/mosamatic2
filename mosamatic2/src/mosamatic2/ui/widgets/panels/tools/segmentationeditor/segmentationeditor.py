from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QSplitter,
    QHBoxLayout,
)
from mosamatic2.core.managers.logmanager import LogManager
from mosamatic2.ui.widgets.panels.defaultpanel import DefaultPanel
from mosamatic2.ui.widgets.panels.tools.segmentationeditor.segmentationeditorcontrols import SegmentationEditorControls
from mosamatic2.ui.widgets.panels.tools.segmentationeditor.segmentationeditorgraphicsview import SegmentationEditorGraphicsView

LOG = LogManager()
PANEL_TITLE = 'SegmentationEditor'
PANEL_NAME = 'segmentationeditor'


class SegmentationEditor(DefaultPanel):

    #-------------------------------------------------------------------------------------------------------
    def __init__(self, settings):
        super(SegmentationEditor, self).__init__()
        self.set_title(PANEL_TITLE)
        self._view = None
        self._controls = None
        self.init()

    # INITIALIZATION

    #-------------------------------------------------------------------------------------------------------
    def init(self):
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.view())
        splitter.addWidget(self.controls())
        splitter.setChildrenCollapsible(False)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 0)
        layout = QHBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)
        self.setObjectName(PANEL_NAME)

    # GETTERS

    #-------------------------------------------------------------------------------------------------------
    def view(self):
        if not self._view:
            self._view = SegmentationEditorGraphicsView(
                self.controls().active_label(),
                self.controls().brush_radius(),
                self.controls().smart_paint(),
                self.controls().fix_non_active_labels(),
                self.controls().overall_opacity(),
                self.controls().hu_lo_muscle(),
                self.controls().hu_hi_muscle(),
                self.controls().hu_lo_vat(),
                self.controls().hu_hi_vat(),
                self.controls().hu_lo_sat(),
                self.controls().hu_hi_sat(),
                self,
            )
            self._view.active_label_changed.connect(self.controls().set_active_label)
            self._view.brush_radius_changed.connect(self.controls().set_brush_radius)
            self._view.smart_paint_changed.connect(self.controls().set_smart_paint)
            self._view.fix_non_active_labels_changed.connect(self.controls().set_fix_non_active_labels)
        return self._view
    
    #-------------------------------------------------------------------------------------------------------
    def controls(self):
        if not self._controls:
            self._controls = SegmentationEditorControls(
                self.settings().get_int('annotationview/active_label', 1),
                self.settings().get_int('annotationview/brush_radius', 10),
                self.settings().get_bool('annotationview/smart_paint', True),
                self.settings().get_bool('annotationview/fix_non_active_labels', True),
                self.settings().get_float('annotationview/overall_opacity', 0.5),
                self.settings().get_int('annotationview/hu_lo_muscle', -29),
                self.settings().get_int('annotationview/hu_hi_muscle', 150),
                self.settings().get_int('annotationview/hu_lo_vat', -190),
                self.settings().get_int('annotationview/hu_hi_vat', -30),
                self.settings().get_int('annotationview/hu_lo_sat', -150),
                self.settings().get_int('annotationview/hu_hi_sat', -30),
                self,
            )
            self._controls.image_loaded.connect(self.handle_image_loaded)
            self._controls.segmentation_loaded.connect(self.segmentation_loaded)
            self._controls.active_label_changed.connect(self.handle_active_label_changed)
            self._controls.smart_paint_changed.connect(self.handle_smart_paint_changed)
            self._controls.fix_non_active_labels_changed.connect(self.handle_fix_non_active_labels_changed)
            self._controls.hu_lo_muscle_changed.connect(self.handle_hu_lo_range_muscle_changed)
            self._controls.hu_hi_muscle_changed.connect(self.handle_hu_hi_range_muscle_changed)
            self._controls.hu_lo_vat_changed.connect(self.handle_hu_lo_range_vat_changed)
            self._controls.hu_hi_vat_changed.connect(self.handle_hu_hi_range_vat_changed)
            self._controls.hu_lo_sat_changed.connect(self.handle_hu_lo_range_sat_changed)
            self._controls.hu_hi_sat_changed.connect(self.handle_hu_hi_range_sat_changed)
            self._controls.overall_opacity_changed.connect(self.handle_overall_opacity_changed)
            self._controls.clear_labels.connect(self.handle_clear_labels)
            self._controls.reset_zoom.connect(self.handle_reset_zoom)
        return self._controls
    
    # EVENT HANDLERS

    #-------------------------------------------------------------------------------------------------------
    def handle_image_loaded(self):
        pass

    #-------------------------------------------------------------------------------------------------------
    def handle_segmentation_loaded(self):
        pass
    
    #-------------------------------------------------------------------------------------------------------
    def handle_active_label_changed(self, label):
        self.view().set_active_label(label)

    #-------------------------------------------------------------------------------------------------------
    def handle_smart_paint_changed(self, smart_paint):
        self.view().set_smart_paint(smart_paint)

    #-------------------------------------------------------------------------------------------------------
    def handle_fix_non_active_labels_changed(self, fix_non_active_labels):
        self.view().set_fix_non_active_labels(fix_non_active_labels)

    #-------------------------------------------------------------------------------------------------------
    def handle_hu_lo_range_muscle_changed(self, value):
        self.view().set_hu_lo_muscle(value)

    #-------------------------------------------------------------------------------------------------------
    def handle_hu_hi_range_muscle_changed(self, value):
        self.view().set_hu_hi_muscle(value)

    #-------------------------------------------------------------------------------------------------------
    def handle_hu_lo_range_vat_changed(self, value):
        self.view().set_hu_lo_vat(value)

    #-------------------------------------------------------------------------------------------------------
    def handle_hu_hi_range_vat_changed(self, value):
        self.view().set_hu_hi_vat(value)

    #-------------------------------------------------------------------------------------------------------
    def handle_hu_lo_range_sat_changed(self, value):
        self.view().set_hu_lo_sat(value)

    #-------------------------------------------------------------------------------------------------------
    def handle_hu_hi_range_sat_changed(self, value):
        self.view().set_hu_hi_sat(value)

    #-------------------------------------------------------------------------------------------------------
    def handle_overall_opacity_changed(self, value):
        self.view().set_overall_opacity(value)

    #-------------------------------------------------------------------------------------------------------
    def handle_clear_labels(self):
        self.view().clear_labels()

    #-------------------------------------------------------------------------------------------------------
    def handle_reset_zoom(self):
        self.view().reset_zoom()