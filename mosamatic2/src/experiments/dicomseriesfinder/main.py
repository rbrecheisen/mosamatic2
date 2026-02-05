import sys
import os
import fnmatch

from PySide6.QtCore import Qt, QThread, Signal, Slot, QTimer, QSettings
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QMessageBox,
)


class DirSearchWorker(QThread):
    results_ready = Signal(list)  # list[tuple[str, str, int]] -> (name, path, depth)
    error = Signal(str)

    def __init__(self, root: str, pattern: str, max_depth: int = 1, parent=None):
        super().__init__(parent)
        self.root = root
        self.pattern = pattern
        self.max_depth = max_depth

    def path_contains(full_path: str, needle: str) -> bool:
        return needle.lower() in full_path.lower()
    
    def run(self) -> None:
        try:
            root = os.path.abspath(os.path.expanduser(self.root))
            if not os.path.isdir(root):
                self.error.emit(f"Root directory does not exist or is not a directory:\n{root}")
                return

            root_sep_count = root.rstrip(os.sep).count(os.sep)
            out: list[tuple[str, str, int]] = []

            for dirpath, dirnames, _filenames in os.walk(root):
                # depth relative to root (root's direct children => depth=1)
                depth = dirpath.rstrip(os.sep).count(os.sep) - root_sep_count
                if depth >= self.max_depth:
                    # prune: prevent walking deeper
                    dirnames[:] = []
                    # but still process current dirpath's direct children (already in dirnames before pruning)
                    # (pruning here stops recursion below current dirpath)
                # We want to match *child directories* (not the root itself).
                if depth < 0:
                    continue

                # Match current level's subdirectories (dirnames) as results
                # For the root itself: depth=0 => its children are depth=1
                child_depth = depth + 1
                if child_depth <= self.max_depth:
                    pat = (self.pattern or "").strip()
                    pat_l = pat.lower()
                    is_glob = any(ch in pat for ch in "*?[")

                    for d in dirnames:
                        full = os.path.join(dirpath, d)
                        full_l = full.lower()

                        if not pat:
                            ok = True
                        elif is_glob:
                            ok = fnmatch.fnmatch(full_l, pat_l)  # glob on full path
                        else:
                            # ok = pat_l in full_l                # substring on full path
                            ok = fnmatch.fnmatch(full_l, f"*{pat_l}*")

                        if ok:
                            out.append((d, full, child_depth))
                    # needle = (self.pattern or "").strip().lower()
                    # for d in dirnames:
                    #     full = os.path.join(dirpath, d)
                    #     if not needle or needle in full.lower():
                    #         out.append((d, full, child_depth))
                    # for d in dirnames:
                    #     if fnmatch.fnmatch(d, self.pattern):
                    #         full = os.path.join(dirpath, d)
                    #         out.append((d, full, child_depth))

            out.sort(key=lambda t: (t[2], t[0].lower()))
            self.results_ready.emit(out)

        except Exception as e:
            self.error.emit(f"{type(e).__name__}: {e}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._settings = QSettings(
            QSettings.IniFormat, 
            QSettings.UserScope, 
            'mosamatic2.experiments', 
            'dicomseriesfinder',
        )
        self.setWindowTitle("Directory Search (os.walk)")

        self._auto_timer = QTimer(self)
        self._auto_timer.setSingleShot(True)
        self._auto_timer.setInterval(250)  # ms debounce
        self._auto_timer.timeout.connect(self._trigger_search_from_fields)

        self.root_edit = QLineEdit(self._settings.value('root_dir', ''))
        self.root_edit.textChanged.connect(self._on_pattern_changed)
        self.root_browse_btn = QPushButton("Browse…")

        self.pattern_edit = QLineEdit(self._settings.value('pattern', ''))
        self.pattern_edit.textChanged.connect(self._on_pattern_changed)
        self.depth_edit = QLineEdit("10")
        self.depth_edit.textChanged.connect(self._on_pattern_changed)
        self.depth_edit.setMaximumWidth(60)

        self.search_btn = QPushButton("Search")
        self.search_btn.setDefault(True)

        self.view = QTableView()
        self.model = QStandardItemModel(0, 3, self)
        self.model.setHorizontalHeaderLabels(["Name", "Path", "Depth"])
        self.view.setModel(self.model)
        self.view.setSelectionBehavior(QTableView.SelectRows)
        self.view.setSelectionMode(QTableView.SingleSelection)
        self.view.horizontalHeader().setStretchLastSection(True)

        top_row = QHBoxLayout()
        top_row.addWidget(QLabel("Root:"))
        top_row.addWidget(self.root_edit, 1)
        top_row.addWidget(self.root_browse_btn)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Pattern:"))
        row2.addWidget(self.pattern_edit, 1)
        row2.addWidget(QLabel("Max depth:"))
        row2.addWidget(self.depth_edit)
        row2.addWidget(self.search_btn)

        layout = QVBoxLayout()
        layout.addLayout(top_row)
        layout.addLayout(row2)
        layout.addWidget(self.view, 1)

        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

        self.root_browse_btn.clicked.connect(self.on_browse_root)
        self.search_btn.clicked.connect(self.on_search)

        self._worker: DirSearchWorker | None = None
        self._on_pattern_changed(self.pattern_edit.text())

    @Slot()
    def on_browse_root(self):
        d = QFileDialog.getExistingDirectory(self, "Select root directory")
        if d:
            self.root_edit.setText(d)

    @Slot(str)
    def _on_pattern_changed(self, _text: str):
        # restart debounce on every keystroke
        self._auto_timer.start()
    
    @Slot()
    def _trigger_search_from_fields(self):
        # don't queue multiple concurrent searches
        if self._worker is not None and self._worker.isRunning():
            return
        self.on_search()

    @Slot()
    def on_search(self):
        root = self.root_edit.text().strip()
        if not root:
            return
        pattern = self.pattern_edit.text().strip() or "*"

        try:
            max_depth = int(self.depth_edit.text().strip() or "1")
            if max_depth < 1:
                raise ValueError
        except ValueError:
            # QMessageBox.warning(self, "Invalid depth", "Max depth must be an integer >= 1.")
            return

        if not root:
            QMessageBox.warning(self, "Missing root", "Please choose a root directory.")
            return

        self.search_btn.setEnabled(False)
        self.search_btn.setText("Searching…")
        self.model.removeRows(0, self.model.rowCount())

        self._worker = DirSearchWorker(root=root, pattern=pattern, max_depth=max_depth, parent=self)
        self._worker.results_ready.connect(self.on_results)
        self._worker.error.connect(self.on_error)
        self._worker.finished.connect(self.on_finished)
        self._worker.start()

    @Slot(list)
    def on_results(self, rows: list):
        for name, path, depth in rows:
            items = [QStandardItem(name), QStandardItem(path), QStandardItem(str(depth))]
            for it in items:
                it.setEditable(False)
            items[2].setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.model.appendRow(items)
        self.view.resizeColumnsToContents()

    @Slot(str)
    def on_error(self, msg: str):
        QMessageBox.critical(self, "Search error", msg)

    @Slot()
    def on_finished(self):
        self.search_btn.setEnabled(True)
        self.search_btn.setText("Search")
        self._worker = None

    def closeEvent(self, event):
        self._settings.setValue('root_dir', self.root_edit.text())
        self._settings.setValue('pattern', self.pattern_edit.text())
        return super().closeEvent(event)


def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.resize(900, 500)
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
