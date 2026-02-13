from PySide6.QtCore import Qt, Signal, QSignalBlocker
from PySide6.QtWidgets import (
    QWidget,
    QGroupBox,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QSpinBox,
    QLabel,
    QPushButton,
    QSlider,
    QCheckBox,
    QGridLayout,
    QRadioButton,
    QButtonGroup,
    QFrame,
)

HELP_INFO = """
<b>Shortcuts</b>
<table>
    <tr><td>Brush radius:</td><td>CTRL + mouse wheel</td></tr>
    <tr><td>Active labels:</td><td>
        "1" for muscle<br>
        "5" for visceral fat<br>
        "7" for subcutaneous fat
    </td></tr>
    <tr><td>Zooming</td><td>Mouse wheel</td></tr>
    <tr><td>Zoom rectangle</td><td>Hold "Z" + mouse click and drag</td></tr>
    <tr><td>Panning</td><td>SPACE + mouse click and drag</td></tr>
    <tr><td>Undo</td><td>
        CTRL + "Z"<br>
        "U"
    </td></tr>
    <tr><td>Remove annotation</td><td>
        "E" + mouse click and drag<br>
        Right mouse button click and drag
    </td></tr>
    <tr><td>Toggle SmartPaint</td><td>"S"</td></tr>
    <tr><td>Toggle fix non-active labels</td><td>"F"</td></tr>
</table>
"""


class SegmentationEditorControls(QWidget):

    # SIGNALS

    image_loaded = Signal()
    segmentation_loaded = Signal()
    segmentation_saved = Signal()
    active_label_changed = Signal(int)
    smart_paint_changed = Signal(bool)
    fix_non_active_labels_changed = Signal(bool)
    hu_lo_muscle_changed = Signal(int)
    hu_hi_muscle_changed = Signal(int)
    hu_lo_vat_changed = Signal(int)
    hu_hi_vat_changed = Signal(int)
    hu_lo_sat_changed = Signal(int)
    hu_hi_sat_changed = Signal(int)
    overall_opacity_changed = Signal(float)
    clear_labels = Signal()
    reset_zoom = Signal()

    #-------------------------------------------------------------------------------------------------------
    def __init__(self, 
                 active_label, 
                 brush_radius, 
                 smart_paint, 
                 fix_non_active_labels,
                 overall_opacity,
                 hu_lo_muscle,
                 hu_hi_muscle,
                 hu_lo_vat,
                 hu_hi_vat,
                 hu_lo_sat,
                 hu_hi_sat,
                 parent,
        ):
        super(SegmentationEditorControls, self).__init__(parent)

        # Fields
        self._active_label = active_label
        self._brush_radius = brush_radius
        self._smart_paint = smart_paint
        self._fix_non_active_labels = fix_non_active_labels
        self._overall_opacity = overall_opacity
        self._hu_lo_muscle = hu_lo_muscle
        self._hu_hi_muscle = hu_hi_muscle
        self._hu_lo_vat = hu_lo_vat
        self._hu_hi_vat = hu_hi_vat
        self._hu_lo_sat = hu_lo_sat
        self._hu_hi_sat = hu_hi_sat

        # UI widgets
        self._load_image_button = None
        self._load_segmentation_button = None
        self._save_segmentation_button = None
        self._active_label_group = None
        self._fix_non_active_labels_checkbox = None
        self._hu_hi_range_muscle_spinbox = None
        self._hu_lo_range_muscle_spinbox = None
        self._hu_hi_range_vat_spinbox = None
        self._hu_lo_range_vat_spinbox = None
        self._hu_hi_range_sat_spinbox = None
        self._hu_lo_range_sat_spinbox = None
        self._brush_radius_label = None
        self._overall_opacity_label = None
        self._overall_opacity_slider = None
        self._reset_zoom_button = None
        self._clear_all_labels_button = None
        self._help_info_label = None
        self.init()

    # INITIALIZATION

    #-------------------------------------------------------------------------------------------------------
    def init(self):

        # Loading image and saving segmentation
        self._load_image_button = QPushButton('Load DICOM image...')
        self._load_image_button.clicked.connect(self.handle_load_image_button)
        self._load_segmentation_button = QPushButton('Load segmentation...')
        self._load_segmentation_button.clicked.connect(self.handle_load_segmentation_button)
        self._save_segmentation_button = QPushButton('Save segmentation...')
        self._save_segmentation_button.clicked.connect(self.handle_save_segmentation_button)

        # Active label groupbox and radiobuttons
        active_label_groupbox = QGroupBox('Active label')
        muscle_radio_button = QRadioButton('Muscle (1)')
        vat_radio_button = QRadioButton('Visceral fat (5)')
        sat_radio_button = QRadioButton('Subcutaneous fat (7)')
        for rb in [muscle_radio_button, vat_radio_button, sat_radio_button]:
            if str(self._active_label) in rb.text():
                rb.setChecked(True)
            else:
                rb.setChecked(False)

        # Active label layout
        active_label_layout = QVBoxLayout(active_label_groupbox)
        active_label_layout.addWidget(muscle_radio_button)
        active_label_layout.addWidget(vat_radio_button)
        active_label_layout.addWidget(sat_radio_button)

        # Active label group
        self._active_label_group = QButtonGroup(active_label_groupbox)
        self._active_label_group.setExclusive(True)
        self._active_label_group.addButton(muscle_radio_button, 1)
        self._active_label_group.addButton(vat_radio_button, 5)
        self._active_label_group.addButton(sat_radio_button, 7)
        self._active_label_group.idClicked.connect(self.handle_active_label_changed)

        # Fix non-active labels
        self._fix_non_active_labels_checkbox = QCheckBox('Fix non-active labels', checked=self._fix_non_active_labels)
        self._fix_non_active_labels_checkbox.checkStateChanged.connect(self.handle_fix_non_active_labels_changed)

        # HU range groupbox and widgets
        hu_range_groupbox = QGroupBox('Hounsfield Unit ranges')
        self._hu_lo_range_muscle_spinbox = QSpinBox(self, minimum=-200, maximum=200, value=self._hu_lo_muscle)
        self._hu_lo_range_muscle_spinbox.valueChanged.connect(self.handle_hu_lo_range_muscle_changed)
        self._hu_hi_range_muscle_spinbox = QSpinBox(self, minimum=-200, maximum=200, value=self._hu_hi_muscle)
        self._hu_hi_range_muscle_spinbox.valueChanged.connect(self.handle_hu_hi_range_muscle_changed)
        self._hu_lo_range_vat_spinbox = QSpinBox(self, minimum=-200, maximum=200, value=self._hu_lo_vat)
        self._hu_lo_range_vat_spinbox.valueChanged.connect(self.handle_hu_lo_range_vat_changed)
        self._hu_hi_range_vat_spinbox = QSpinBox(self, minimum=-200, maximum=200, value=self._hu_hi_vat)
        self._hu_hi_range_vat_spinbox.valueChanged.connect(self.handle_hu_hi_range_vat_changed)
        self._hu_lo_range_sat_spinbox = QSpinBox(self, minimum=-200, maximum=200, value=self._hu_lo_sat)
        self._hu_lo_range_sat_spinbox.valueChanged.connect(self.handle_hu_lo_range_sat_changed)
        self._hu_hi_range_sat_spinbox = QSpinBox(self, minimum=-200, maximum=200, value=self._hu_hi_sat)
        self._hu_hi_range_sat_spinbox.valueChanged.connect(self.handle_hu_hi_range_sat_changed)

        # HU range layout
        hu_range_layout = QGridLayout(hu_range_groupbox)
        hu_range_layout.addWidget(QLabel(''), 0, 0)
        hu_range_layout.addWidget(QLabel('Low'), 0, 1)
        hu_range_layout.addWidget(QLabel('High'), 0, 2)
        hu_range_layout.addWidget(QLabel('Muscle'), 1, 0)
        hu_range_layout.addWidget(self._hu_lo_range_muscle_spinbox, 1, 1)
        hu_range_layout.addWidget(self._hu_hi_range_muscle_spinbox, 1, 2)
        hu_range_layout.addWidget(QLabel('Visceral fat'), 2, 0)
        hu_range_layout.addWidget(self._hu_lo_range_vat_spinbox, 2, 1)
        hu_range_layout.addWidget(self._hu_hi_range_vat_spinbox, 2, 2)
        hu_range_layout.addWidget(QLabel('Subcutaneous fat'), 3, 0)
        hu_range_layout.addWidget(self._hu_lo_range_sat_spinbox, 3, 1)
        hu_range_layout.addWidget(self._hu_hi_range_sat_spinbox, 3, 2)

        # Separator line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Plain)

        # Smart paint
        self._smart_paint_checkbox = QCheckBox('Smart paint', checked=self._smart_paint)
        self._smart_paint_checkbox.checkStateChanged.connect(self.handle_smart_paint_changed)

        # Brush radius
        self._brush_radius_label = QLabel(f'Brush radius: {str(self._brush_radius)}')
        
        # Overall opacity
        self._overall_opacity_slider = QSlider(Qt.Horizontal)
        self._overall_opacity_slider.setRange(0, 100)
        self._overall_opacity_slider.setValue(int(self._overall_opacity * 100))
        self._overall_opacity_slider.valueChanged.connect(self.handle_overall_opacity_changed)
        self._overall_opacity_label = QLabel(str(self._overall_opacity))
        overall_opacity_layout = QHBoxLayout()
        overall_opacity_layout.addWidget(self._overall_opacity_slider)
        overall_opacity_layout.addWidget(self._overall_opacity_label)
        
        # Reset zoom
        self._reset_zoom_button = QPushButton('Reset zoom')
        self._reset_zoom_button.clicked.connect(self.handle_reset_zoom_button)
        
        # Clear all labels
        self._clear_all_labels_button = QPushButton('Clear all labels')
        self._clear_all_labels_button.clicked.connect(self.handle_clear_all_labels_button)

        # Help info
        self._help_info_label = QLabel(HELP_INFO)
        self._help_info_label.setWordWrap(True)
        self._help_info_label.setTextFormat(Qt.RichText)
        self._help_info_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # Main layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self._load_image_button)
        layout.addWidget(self._save_segmentation_button)
        layout.addWidget(active_label_groupbox)
        layout.addWidget(hu_range_groupbox)
        layout.addWidget(self._fix_non_active_labels_checkbox)
        layout.addWidget(self._smart_paint_checkbox)
        layout.addWidget(line)
        layout.addWidget(QLabel('Overall opacity'))
        layout.addLayout(overall_opacity_layout)
        layout.addWidget(self._brush_radius_label)
        layout.addWidget(self._reset_zoom_button)
        layout.addWidget(self._clear_all_labels_button)
        layout.addWidget(self._help_info_label)
        self.setLayout(layout)

    # GETTERS

    #-------------------------------------------------------------------------------------------------------
    def active_label(self):
        return self._active_label
    
    #-------------------------------------------------------------------------------------------------------
    def set_active_label(self, active_label):
        self._active_label = active_label
        button = self._active_label_group.button(self._active_label)
        with QSignalBlocker(button):
            button.setChecked(True)
    
    #-------------------------------------------------------------------------------------------------------
    def brush_radius(self):
        return self._brush_radius
    
    #-------------------------------------------------------------------------------------------------------
    def set_brush_radius(self, brush_radius):
        self._brush_radius = brush_radius
        self._brush_radius_label.setText(f'Brush radius: {str(self._brush_radius)}')
    
    #-------------------------------------------------------------------------------------------------------
    def smart_paint(self):
        return self._smart_paint

    #-------------------------------------------------------------------------------------------------------
    def set_smart_paint(self, smart_paint):
        self._smart_paint = smart_paint
        with QSignalBlocker(self._smart_paint_checkbox):
            self._smart_paint_checkbox.setChecked(self._smart_paint)
    
    #-------------------------------------------------------------------------------------------------------
    def fix_non_active_labels(self):
        return self._fix_non_active_labels
    
    #-------------------------------------------------------------------------------------------------------
    def set_fix_non_active_labels(self, fix_non_active_labels):
        self._fix_non_active_labels = fix_non_active_labels
        with QSignalBlocker(self._fix_non_active_labels_checkbox):
            self._fix_non_active_labels_checkbox.setChecked(self._fix_non_active_labels)
    
    #-------------------------------------------------------------------------------------------------------
    def overall_opacity(self):
        return self._overall_opacity
    
    #-------------------------------------------------------------------------------------------------------
    def hu_lo_muscle(self):
        return self._hu_lo_muscle
    
    #-------------------------------------------------------------------------------------------------------
    def hu_hi_muscle(self):
        return self._hu_hi_muscle
    
    #-------------------------------------------------------------------------------------------------------
    def hu_lo_vat(self):
        return self._hu_lo_vat
    
    #-------------------------------------------------------------------------------------------------------
    def hu_hi_vat(self):
        return self._hu_hi_vat
    
    #-------------------------------------------------------------------------------------------------------
    def hu_lo_sat(self):
        return self._hu_lo_sat
    
    #-------------------------------------------------------------------------------------------------------
    def hu_hi_sat(self):
        return self._hu_hi_sat
    
    # EVENT HANDLERS

    #-------------------------------------------------------------------------------------------------------
    def handle_load_image_button(self):
        self.image_loaded.emit()

    #-------------------------------------------------------------------------------------------------------
    def handle_load_segmentation_button(self):
        self.segmentation_loaded.emit()

    #-------------------------------------------------------------------------------------------------------
    def handle_save_segmentation_button(self):
        self.segmentation_saved.emit()

    #-------------------------------------------------------------------------------------------------------
    def handle_active_label_changed(self, label_id):
        if label_id < 0:
            return
        self._active_label = label_id
        self.active_label_changed.emit(self._active_label)

    #-------------------------------------------------------------------------------------------------------
    def handle_smart_paint_changed(self, state):
        self._smart_paint = True if state == Qt.CheckState.Checked else False
        self.smart_paint_changed.emit(self._smart_paint)
        
    #-------------------------------------------------------------------------------------------------------
    def handle_fix_non_active_labels_changed(self, state):
        self._fix_non_active_labels = True if state == Qt.CheckState.Checked else False
        self.fix_non_active_labels_changed.emit(self._fix_non_active_labels)

    #-------------------------------------------------------------------------------------------------------
    def handle_hu_lo_range_muscle_changed(self, value):
        self._hu_lo_muscle = value
        self.hu_lo_muscle_changed.emit(self._hu_lo_muscle)

    #-------------------------------------------------------------------------------------------------------
    def handle_hu_hi_range_muscle_changed(self, value):
        self._hu_hi_muscle = value
        self.hu_hi_muscle_changed.emit(self._hu_hi_muscle)

    #-------------------------------------------------------------------------------------------------------
    def handle_hu_lo_range_vat_changed(self, value):
        self._hu_lo_vat = value
        self.hu_lo_vat_changed.emit(self._hu_lo_vat)

    #-------------------------------------------------------------------------------------------------------
    def handle_hu_hi_range_vat_changed(self, value):
        self._hu_hi_vat = value
        self.hu_hi_vat_changed.emit(self._hu_hi_vat)

    #-------------------------------------------------------------------------------------------------------
    def handle_hu_lo_range_sat_changed(self, value):
        self._hu_lo_sat = value
        self.hu_lo_sat_changed.emit(self._hu_lo_sat)

    #-------------------------------------------------------------------------------------------------------
    def handle_hu_hi_range_sat_changed(self, value):
        self._hu_hi_sat = value
        self.hu_hi_sat_changed.emit(self._hu_hi_sat)

    #-------------------------------------------------------------------------------------------------------
    def handle_overall_opacity_changed(self, value):
        opacity = float(value) / 100.0
        self._overall_opacity_label.setText(str(opacity))
        self._overall_opacity = opacity
        self.overall_opacity_changed.emit(opacity)

    #-------------------------------------------------------------------------------------------------------
    def handle_reset_zoom_button(self):
        self.reset_zoom.emit()

    #-------------------------------------------------------------------------------------------------------
    def handle_clear_all_labels_button(self):
        self.clear_labels.emit()