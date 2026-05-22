"""File selector component for choosing audio files."""

from PyQt5 import QtWidgets

from PyQt5.QtCore import pyqtSignal


class FileSelector(QtWidgets.QWidget):
    """A reusable file selector component."""

    file_selected = pyqtSignal(str)  # Signal emitted when a file is selected

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_file = ""
        self.init_ui()

    def init_ui(self):
        """Initialize the UI components."""
        self.browse_btn = QtWidgets.QPushButton("Browse", self)
        self.file_label = QtWidgets.QLabel("No file selected", self)
        self.file_label.setVisible(False)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.browse_btn)
        layout.addWidget(self.file_label)
        self.setLayout(layout)

        self.browse_btn.clicked.connect(self.browse_file)

    def browse_file(self):
        """Open a file dialog to select an audio file."""
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select Audio File", "", "Audio Files (*.mp3 *.wav *.flac)"
        )
        if file_name:
            self.selected_file = file_name
            self.file_label.setVisible(True)
            self.file_label.setText(file_name)
            self.file_selected.emit(file_name)

    def get_selected_file(self):
        """Return the currently selected file path."""
        return self.selected_file