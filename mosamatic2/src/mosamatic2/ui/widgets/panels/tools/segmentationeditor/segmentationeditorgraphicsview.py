import numpy as np
from PySide6.QtWidgets import (
    QGraphicsPixmapItem,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsEllipseItem,
    QRubberBand,
    QToolTip,
)
from PySide6.QtCore import Qt, QRectF, QTimer, Signal, QPoint, QRect
from PySide6.QtGui import (
    QPixmap,
    QPainter,
    QPen,
    QColor,
)
from mosamatic2.ui.widgets.panels.tools.segmentationeditor.utils import (
    clamp,
    circle_brush,
    np_u8_gray_to_qimage,
    np_rgba_to_qimage,
)

LABEL_COLORS = {
    0: (0, 0, 0),      # background
    1: (255, 0, 0),    # muscle
    5: (255, 255, 0),  # vat
    7: (0, 255, 255),  # sat
}


class SegmentationEditorGraphicsView(QGraphicsView):

    # SIGNALS

    active_label_changed = Signal(int)
    brush_radius_changed = Signal(int)
    smart_paint_changed = Signal(bool)
    fix_non_active_labels_changed = Signal(bool)

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
        super(SegmentationEditorGraphicsView, self).__init__(parent)

        # Fields
        self._document = None
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

        # Undo
        self._undo_stack = []
        self._undo_limit = 50
        self._stroke_bbox = None
        self._stroke_before = None
        self._stroke_active = False

        # Graphics scene
        self._scene = None
        self._image_item = None
        self._image_overlay_item = None

        # Rendering state
        self._painting = False
        self._panning = False
        self._panning_anchor = None
        self._erase_mode = False
        self._space_down = False
        self._dirty = True
        self._update_timer = None
        self._zoom = 0
        self._brush_cursor_item = None

        # Zoom-rectangle (rubber band)
        self._zoom_rect_mode = False   # toggle on/off (e.g. with Z)
        self._zoom_rb = None
        self._zoom_origin = None       # QPoint (viewport coords)

        # Buffers must stay alive while QImages reference them
        self._disp8_ref = None
        self._disp_qimage_ref = None
        self._image_overlay_rgba_ref = None
        self._image_overlay_qimage_ref = None

        self.init()

    # INITIALIZATION

    #-------------------------------------------------------------------------------------------------------
    def init(self):
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)
        self.setBackgroundBrush(Qt.black)
        self._image_item = QGraphicsPixmapItem()
        self._image_overlay_item = QGraphicsPixmapItem()
        self._image_overlay_item.setZValue(10)
        self._scene.addItem(self._image_item)
        self._scene.addItem(self._image_overlay_item)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFocus(Qt.FocusReason.OtherFocusReason)
        self.setRenderHints(self.renderHints() | QPainter.RenderHint.SmoothPixmapTransform)

        # Zoom rectangle
        self._zoom_rb = QRubberBand(QRubberBand.Shape.Rectangle, self.viewport())
        self._zoom_rb.hide()
        
        # Brush radius circle
        self.setMouseTracking(True)  # important: get mouseMoveEvent even w/o buttons
        self._brush_cursor_item = QGraphicsEllipseItem()
        self._brush_cursor_item.setZValue(1000)  # above overlay
        pen = QPen(QColor(255, 255, 0, 255))
        pen.setStyle(Qt.PenStyle.DashLine)
        pen.setWidth(1)
        pen.setCosmetic(True)  # keep constant on-screen width while zooming
        self._brush_cursor_item.setPen(pen)
        self._brush_cursor_item.setBrush(Qt.BrushStyle.NoBrush)
        self._brush_cursor_item.hide()
        self._scene.addItem(self._brush_cursor_item)
        
        # Cap refresh rate
        self._update_timer = QTimer(self)
        self._update_timer.setInterval(16)  # ~60fps cap
        self._update_timer.timeout.connect(self._maybe_update_overlay)
        self._update_timer.start()
        
        # Zooming
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

    # PUBLIC METHODS

    #-------------------------------------------------------------------------------------------------------
    def document(self):
        return self._document

    #-------------------------------------------------------------------------------------------------------
    def set_document(self, document):
        self._document = document
        self._set_base_image(self._document.disp8)
        self._rebuild_overlay_full()
        self.reset_zoom()

    #-------------------------------------------------------------------------------------------------------
    def set_active_label(self, active_label):
        self._active_label = active_label

    #-------------------------------------------------------------------------------------------------------
    def set_brush_radius(self, brush_radius):
        self._brush_radius = brush_radius
        vp_pos = self.mapFromGlobal(self.cursor().pos())
        self._update_brush_cursor_at_viewport_pos(vp_pos)

    #-------------------------------------------------------------------------------------------------------
    def set_smart_paint(self, smart_paint):
        self._smart_paint = smart_paint

    #-------------------------------------------------------------------------------------------------------
    def set_fix_non_active_labels(self, fix_non_active_labels):
        self._fix_non_active_labels = fix_non_active_labels

    #-------------------------------------------------------------------------------------------------------
    def set_hu_lo_muscle(self, hu):
        self._hu_lo_muscle = hu

    #-------------------------------------------------------------------------------------------------------
    def set_hu_hi_muscle(self, hu):
        self._hu_hi_muscle = hu

    #-------------------------------------------------------------------------------------------------------
    def set_hu_lo_vat(self, hu):
        self._hu_lo_vat = hu

    #-------------------------------------------------------------------------------------------------------
    def set_hu_hi_vat(self, hu):
        self._hu_hi_vat = hu

    #-------------------------------------------------------------------------------------------------------
    def set_hu_lo_sat(self, hu):
        self._hu_lo_sat = hu

    #-------------------------------------------------------------------------------------------------------
    def set_hu_hi_sat(self, hu):
        self._hu_hi_sat = hu

    #-------------------------------------------------------------------------------------------------------
    def set_overall_opacity(self, opacity):
        self._overall_opacity = opacity
        self._rebuild_overlay_full()

    #-------------------------------------------------------------------------------------------------------
    def clear_labels(self):
        if self._document is None:
            return
        self._document.mask.fill(0)
        self._rebuild_overlay_full()

    #-------------------------------------------------------------------------------------------------------
    def reset_zoom(self):
        if self._document is None:
            return
        h, w = self._document.disp8.shape
        self.setSceneRect(QRectF(0, 0, w, h))
        self.resetTransform()
        self._zoom = 0
        self.fitInView(QRectF(0, 0, w, h), Qt.AspectRatioMode.KeepAspectRatio)

    # PRIVATE HELPERS

    #-------------------------------------------------------------------------------------------------------
    def _zoom_to_viewport_rect(self, vp_rect: QRect):
        if self._document is None:
            return
        if vp_rect.width() < 5 or vp_rect.height() < 5:
            return

        # Convert viewport rect -> scene rect and zoom
        scene_rect = self.mapToScene(vp_rect).boundingRect()
        self.fitInView(scene_rect, Qt.AspectRatioMode.KeepAspectRatio)
        self._zoom += 1  # optional bookkeeping

    #-------------------------------------------------------------------------------------------------------
    def _update_brush_cursor_at_viewport_pos(self, vp_pos: QPoint):
        if self._document is None or self._brush_cursor_item is None:
            return

        scene_pos = self.mapToScene(vp_pos)
        item_pos = self._image_item.mapFromScene(scene_pos)

        x = item_pos.x()
        y = item_pos.y()

        h, w = self._document.mask.shape
        if not (0 <= x < w and 0 <= y < h):
            self._brush_cursor_item.hide()
            return

        r = self._brush_radius
        self._brush_cursor_item.setRect(QRectF(x - r, y - r, 2 * r, 2 * r))
        self._brush_cursor_item.show()    

    #-------------------------------------------------------------------------------------------------------
    def _union_bbox(self, a, b):
        # bboxes are (x0,y0,x1,y1) inclusive
        if a is None:
            return b
        ax0, ay0, ax1, ay1 = a
        bx0, by0, bx1, by1 = b
        return (min(ax0, bx0), min(ay0, by0), max(ax1, bx1), max(ay1, by1))

    #-------------------------------------------------------------------------------------------------------
    def _brush_bbox(self, x, y):
        h, w = self._document.mask.shape
        r = self._brush_radius
        x0 = clamp(x - r, 0, w - 1)
        x1 = clamp(x + r, 0, w - 1)
        y0 = clamp(y - r, 0, h - 1)
        y1 = clamp(y + r, 0, h - 1)
        return (x0, y0, x1, y1)

    #-------------------------------------------------------------------------------------------------------
    def _ensure_stroke_before_covers(self, new_bbox):
        """Ensure _stroke_before covers union(current_bbox, new_bbox)."""
        if self._stroke_bbox is None:
            self._stroke_bbox = new_bbox
            x0,y0,x1,y1 = new_bbox
            self._stroke_before = self._document.mask[y0:y1+1, x0:x1+1].copy()
            return

        union = self._union_bbox(self._stroke_bbox, new_bbox)
        if union == self._stroke_bbox:
            return

        # Expand before-snapshot to cover union by re-sampling from current mask,
        # then overwrite the already-captured area with the original "before" pixels.
        ux0,uy0,ux1,uy1 = union
        expanded = self._document.mask[uy0:uy1+1, ux0:ux1+1].copy()

        ox0,oy0,ox1,oy1 = self._stroke_bbox
        # placement of old before inside expanded
        ex0 = ox0 - ux0
        ey0 = oy0 - uy0
        expanded[ey0:ey0+(oy1-oy0+1), ex0:ex0+(ox1-ox0+1)] = self._stroke_before

        self._stroke_bbox = union
        self._stroke_before = expanded

    #-------------------------------------------------------------------------------------------------------
    def _label_hu_ranges(self):
        return {
            1: (self._hu_lo_muscle, self._hu_hi_muscle),
            5: (self._hu_lo_vat, self._hu_hi_vat),
            7: (self._hu_lo_sat, self._hu_hi_sat),
        }        

    #-------------------------------------------------------------------------------------------------------
    def _set_base_image(self, disp8):
        self._disp8_ref = np.ascontiguousarray(disp8)
        self._disp_qimage_ref = np_u8_gray_to_qimage(self._disp8_ref)
        pix = QPixmap.fromImage(self._disp_qimage_ref)
        self._image_item.setPixmap(pix)

    #-------------------------------------------------------------------------------------------------------
    def _rebuild_overlay_full(self):
        if self._document is None:
            return
        h, w = self._document.mask.shape
        rgba = np.zeros((h, w, 4), dtype=np.uint8)
        for lab, (r, g, b) in LABEL_COLORS.items():
            if lab == 0:
                continue
            m = (self._document.mask == lab)
            rgba[m, 0] = r
            rgba[m, 1] = g
            rgba[m, 2] = b
            rgba[m, 3] = int(255 * self._overall_opacity)

        # Keep refs alive
        self._image_overlay_rgba_ref = np.ascontiguousarray(rgba)
        self._image_overlay_qimage_ref = np_rgba_to_qimage(self._image_overlay_rgba_ref)
        self._image_overlay_item.setPixmap(QPixmap.fromImage(self._image_overlay_qimage_ref))
        self._dirty = False

    #-------------------------------------------------------------------------------------------------------
    def _maybe_update_overlay(self):
        if self._dirty and self._document is not None:
            # v1: full rebuild (fast enough for many single-slice cases)
            self._rebuild_overlay_full()

    #-------------------------------------------------------------------------------------------------------
    def _mouse_to_pixel(self, event):
        if self._document is None:
            return None
        scene_pos = self.mapToScene(event.position().toPoint())
        item_pos = self._image_item.mapFromScene(scene_pos)
        x = int(item_pos.x())
        y = int(item_pos.y())
        h, w = self._document.mask.shape
        if 0 <= x < w and 0 <= y < h:
            return x, y
        return None

    #-------------------------------------------------------------------------------------------------------
    def _stamp(self, x, y, label):
        if self._document is None:
            return
        
        if self._stroke_active:
            self._ensure_stroke_before_covers(self._brush_bbox(x, y))

        h, w = self._document.mask.shape
        brush = circle_brush(self._brush_radius)
        r = self._brush_radius

        x0 = clamp(x - r, 0, w - 1)
        x1 = clamp(x + r, 0, w - 1)
        y0 = clamp(y - r, 0, h - 1)
        y1 = clamp(y + r, 0, h - 1)

        # Corresponding brush window
        bx0 = x0 - (x - r)
        by0 = y0 - (y - r)
        bx1 = bx0 + (x1 - x0) + 1
        by1 = by0 + (y1 - y0) + 1

        region = self._document.mask[y0 : y1 + 1, x0 : x1 + 1]
        region_img = self._document.img[y0 : y1 + 1, x0 : x1 + 1]
        b = brush[by0:by1, bx0:bx1]

        if self._fix_non_active_labels:
            writable = (region == 0) | (region == label)
        else:
            writable = np.ones_like(region, dtype=bool)

        if label == 0:
            region[b & (region == self._active_label)] = 0
            self._dirty = True
            return
        
        if not self._smart_paint:
            region[b & writable] = label
            self._dirty = True
            return

        # Smart paint: only paint pixels whose intensity is in the label's range
        lo, hi = self._label_hu_ranges().get(label, (-np.inf, np.inf))
        valid = (region_img >= lo) & (region_img <= hi)
        region[b & writable & valid] = label
        self._dirty = True

    #-------------------------------------------------------------------------------------------------------
    def undo(self):
        if self._document is None or not self._undo_stack:
            return
        item = self._undo_stack.pop()
        x0,y0,x1,y1 = item["bbox"]
        self._document.mask[y0:y1+1, x0:x1+1] = item["before"]
        self._dirty = True

    # EVENT HANDLERS

    #-------------------------------------------------------------------------------------------------------
    def wheelEvent(self, event):
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            # Ctrl+Wheel -> brush size
            delta = event.angleDelta().y()
            step = 1 if delta > 0 else -1
            self._brush_radius = clamp(self._brush_radius + step, 1, 100)
            self.brush_radius_changed.emit(self._brush_radius)
            vp_pos = self.mapFromGlobal(self.cursor().pos())
            self._update_brush_cursor_at_viewport_pos(vp_pos)
            event.accept()
            return

        # Wheel -> zoom
        delta = event.angleDelta().y()
        if delta == 0:
            return
        factor = 1.25 if delta > 0 else 0.8
        self.scale(factor, factor)
        self._zoom += 1 if delta > 0 else -1
        event.accept()

    #-------------------------------------------------------------------------------------------------------
    def mousePressEvent(self, event):
        if self._document is None:
            return super().mousePressEvent(event)

        # Pan: middle mouse OR Space+Left
        if event.button() == Qt.MouseButton.MiddleButton or (
            event.button() == Qt.MouseButton.LeftButton and self._space_down
        ):
            self._panning = True
            self._panning_anchor = event.position().toPoint()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            event.accept()
            return

        # Zoom rectangle: Left click drag when in zoom-rect mode
        if self._zoom_rect_mode and event.button() == Qt.MouseButton.LeftButton and not self._space_down:
            self._painting = False  # ensure we don't paint
            self._zoom_origin = event.position().toPoint()
            self._zoom_rb.setGeometry(QRect(self._zoom_origin, self._zoom_origin))
            self._zoom_rb.show()
            event.accept()
            return
        
        if event.button() in (Qt.MouseButton.LeftButton, Qt.MouseButton.RightButton):
            pos = self._mouse_to_pixel(event)
            if pos is None:
                return
            x, y = pos

            self._stroke_active = True
            self._stroke_bbox = None
            self._stroke_before = None

            # Right button always erase; left button paints active label (unless erase_mode)
            if event.button() == Qt.MouseButton.RightButton or self._erase_mode:
                self._stamp(x, y, 0)
            else:
                self._stamp(x, y, self._active_label)

            self._painting = True
            event.accept()
            return
        super().mousePressEvent(event)

    #-------------------------------------------------------------------------------------------------------
    def mouseMoveEvent(self, event):
        if self._document is None:
            return super().mouseMoveEvent(event)
        
        self._update_brush_cursor_at_viewport_pos(event.position().toPoint())
        
        if self._zoom_rb.isVisible() and self._zoom_origin is not None:
            cur = event.position().toPoint()
            self._zoom_rb.setGeometry(QRect(self._zoom_origin, cur).normalized())
            event.accept()
            return
            
        if self._panning and self._panning_anchor is not None:
            delta = event.position().toPoint() - self._panning_anchor
            self._panning_anchor = event.position().toPoint()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
            event.accept()
            return

        if self._painting:
            pos = self._mouse_to_pixel(event)
            if pos is None:
                return
            x, y = pos
            buttons = event.buttons()

            if (event.modifiers() & Qt.KeyboardModifier.ShiftModifier) and (buttons & Qt.MouseButton.LeftButton):
                self._stamp(x, y, 0)
            elif buttons & Qt.MouseButton.RightButton or self._erase_mode:
                self._stamp(x, y, 0)
            elif buttons & Qt.MouseButton.LeftButton:
                self._stamp(x, y, self._active_label)

            event.accept()
            return
        super().mouseMoveEvent(event)

    #-------------------------------------------------------------------------------------------------------
    def mouseReleaseEvent(self, event):
        if self._zoom_rb.isVisible() and event.button() == Qt.MouseButton.LeftButton:
            rect = self._zoom_rb.geometry()
            self._zoom_rb.hide()
            self._zoom_to_viewport_rect(rect)
            self._zoom_origin = None
            event.accept()
            return
            
        if self._panning and event.button() in (Qt.MouseButton.MiddleButton, Qt.MouseButton.LeftButton):
            self._panning = False
            self._panning_anchor = None
            self.setCursor(Qt.CursorShape.ArrowCursor)
            event.accept()
            return
        
        if event.button() in (Qt.MouseButton.LeftButton, Qt.MouseButton.RightButton):
            # Commit one undo item per stroke
            if self._stroke_bbox is not None and self._stroke_before is not None:
                x0, y0, x1, y1 = self._stroke_bbox
                after = self._document.mask[y0:y1+1, x0:x1+1].copy()
                if not np.array_equal(after, self._stroke_before):
                    self._undo_stack.append({"bbox": self._stroke_bbox, "before": self._stroke_before, "after": after})
                    if len(self._undo_stack) > self._undo_limit:
                        self._undo_stack.pop(0)

            # End stroke capture
            self._stroke_active = False
            self._stroke_bbox = None
            self._stroke_before = None
            self._painting = False
            event.accept()
            return
        super().mouseReleaseEvent(event)

    #-------------------------------------------------------------------------------------------------------
    def keyPressEvent(self, event):
        key = event.key()

        if (event.modifiers() & Qt.KeyboardModifier.ControlModifier) and key == Qt.Key.Key_Z:
            self.undo()
            event.accept()
            return
        
        if key == Qt.Key.Key_U:
            self.undo()
            event.accept()
            return
        
        if key == Qt.Key.Key_Z:
            self._zoom_rect_mode = True
            QToolTip.showText(self.mapToGlobal(QPoint(10, 10)), "Ready to zoom", self)
            # nice UX: hide cursor circle while zooming
            if self._zoom_rect_mode:
                self._brush_cursor_item.hide()
            event.accept()
            return
            
        if key == Qt.Key.Key_R:
            self.reset_zoom()
            event.accept()
            return

        if key in (Qt.Key.Key_BracketLeft, Qt.Key.Key_BracketRight):
            step = -1 if key == Qt.Key.Key_BracketLeft else 1
            self._brush_radius = clamp(self._brush_radius + step, 1, 100)
            QToolTip.showText(self.mapToGlobal(QPoint(10, 10)), "Updating brush radius", self)
            self.brush_radius_changed.emit(self._brush_radius)
            vp_pos = self.mapFromGlobal(self.cursor().pos())
            self._update_brush_cursor_at_viewport_pos(vp_pos)
            event.accept()
            return

        if key == Qt.Key.Key_E:
            self._erase_mode = True
            QToolTip.showText(self.mapToGlobal(QPoint(10, 10)), "Ready to erase", self)
            event.accept()
            return

        if key == Qt.Key.Key_1:
            self._active_label = 1
            QToolTip.showText(self.mapToGlobal(QPoint(10, 10)), "Selected muscle", self)
            self.active_label_changed.emit(self._active_label)
            event.accept()
            return
        
        if key == Qt.Key.Key_5:
            self._active_label = 5
            QToolTip.showText(self.mapToGlobal(QPoint(10, 10)), "Selected visceral fat", self)
            self.active_label_changed.emit(self._active_label)
            event.accept()
            return
        
        if key == Qt.Key.Key_7:
            self._active_label = 7
            QToolTip.showText(self.mapToGlobal(QPoint(10, 10)), "Selected subcutaneous fat", self)
            self.active_label_changed.emit(self._active_label)
            event.accept()
            return
        
        if key == Qt.Key.Key_Space:
            self._space_down = True
            QToolTip.showText(self.mapToGlobal(QPoint(10, 10)), "Reading for panning", self)
            event.accept()
            return

        if key == Qt.Key.Key_S:
            self._smart_paint = not self._smart_paint
            enabled = 'enabled' if self._smart_paint else 'disabled'
            QToolTip.showText(self.mapToGlobal(QPoint(10, 10)), f"SmartPaint {enabled}", self)
            self.smart_paint_changed.emit(self._smart_paint)
            event.accept()
            return

        if key == Qt.Key.Key_F:
            self._fix_non_active_labels = not self._fix_non_active_labels
            # self._smart_paint = not self._smart_paint
            enabled = 'enabled' if self._smart_paint else 'disabled'
            QToolTip.showText(self.mapToGlobal(QPoint(10, 10)), f"Fix non-active labels: {enabled}", self)
            self.fix_non_active_labels_changed.emit(self._fix_non_active_labels)
            event.accept()
            return

        super().keyPressEvent(event)

    #-------------------------------------------------------------------------------------------------------
    def keyReleaseEvent(self, event):
        key = event.key()

        if key == Qt.Key.Key_Z:
            self._zoom_rect_mode = False
            vp_pos = self.mapFromGlobal(self.cursor().pos())
            self._update_brush_cursor_at_viewport_pos(vp_pos)
            event.accept()
            return
            
        if key == Qt.Key.Key_E:
            self._erase_mode = False
            event.accept()
            return
        
        if key == Qt.Key.Key_Space:
            self._space_down = False
            event.accept()
            return
        
        super().keyReleaseEvent(event)