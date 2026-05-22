import os
import subprocess

from .components.file_selector import FileSelector
from .components.audio_player import AudioPlayer
from .components.audio_settings import AudioSettings
from .components.effects_panel import EffectsPanel

from core.AudioProcessor import AudioProcessor
from core.AudioPlayer import MusicPlayer
from core.dto.command import Command
try:
    from PyQt5 import QtWidgets
    from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLabel
except ImportError as exc:
    raise ImportError("PyQt5 is required to run this application. Please install it via pip.") from exc


class AudioExporterUI(QtWidgets.QWidget):
    """UI class for the audio exporter application."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pycrappify")
        self.setFixedSize(400, self.sizeHint().height())
        self.setStyleSheet("background-color: #1a1a1f; color: white; font-size: 12pt;")

        self.processor = AudioProcessor()
        self.audio_backend = MusicPlayer()

        self.file_selector = FileSelector()
        self.audio_player = AudioPlayer(player=self.audio_backend, processor=self.processor)
        self.audio_settings = AudioSettings(processor=self.processor)
        self.effects_panel = EffectsPanel()
        self.export_btn = QPushButton("Export audio")
        self.status_label = QLabel("")

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.file_selector)
        main_layout.addWidget(self.audio_player)
        main_layout.addWidget(self.audio_settings)
        main_layout.addWidget(self.effects_panel)
        main_layout.addWidget(self.export_btn)
        main_layout.addWidget(self.status_label)
        self.setLayout(main_layout)

        self.file_selector.file_selected.connect(self.audio_backend.load)
        self.file_selector.file_selected.connect(self.audio_player.update_audio_settings)
        self.file_selector.file_selected.connect(self.audio_settings.update_from_file)
        self.file_selector.file_selected.connect(self._clear_status)
        self.export_btn.clicked.connect(self.export_audio)
        self.audio_settings.settings_changed.connect(self._clear_status)
        self.effects_panel.settings_changed.connect(self._clear_status)

    def _clear_status(self):
        self.status_label.setText("")

    def _selected_file(self):
        selected_file = self.file_selector.get_selected_file()
        if selected_file:
            return selected_file
        label_text = self.file_selector.file_label.text()
        return label_text if label_text and label_text != "No file selected" else ""

    def _build_command_args(self, input_file, output_file):
        settings = self.audio_settings.get_settings()
        effects = self.effects_panel.get_bitcrush_settings()
        return Command(
            input_file=input_file,
            output_file=output_file,
            bitrate=settings["bitrate"],
            sample_Rate=settings["sample_rate"],
            mono=settings["mono"],
            **effects,
        )

    def export_audio(self):
        """Export the audio file with the selected settings."""
        input_file = self._selected_file()
        if not input_file:
            QtWidgets.QMessageBox.warning(self, "No File", "Please select an audio file first.")
            return

        output_file = os.path.splitext(input_file)[0] + "_processed.mp3"
        command_args = self._build_command_args(input_file, output_file)

        if os.path.exists(output_file):
            msg = QtWidgets.QMessageBox.question(
                self,
                "Overwrite File",
                f"Output file '{output_file}' exists. Do you want to overwrite it?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No,
            )
            if msg != QtWidgets.QMessageBox.Yes:
                return

        try:
            self.processor.compress(command_args)
            self.status_label.setText("Audio exported successfully.")
            QtWidgets.QMessageBox.information(self, "Success", "Audio exported successfully!")
        except (subprocess.CalledProcessError, ValueError, OSError) as exc:
            self.status_label.setText("Export failed.")
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to export audio:\n{exc}")
