import os
from PyQt5 import QtWidgets
from tools.AudioProcessor import AudioProcessor

class MainWindow:
    """Controller that binds UI signals to logic."""

    def __init__(self, ui):
        self.ui = ui
        self.processor = AudioProcessor()
        self.connect_signals()

    def connect_signals(self):
        """Connect UI signals to their respective slots."""
        self.ui.browse_btn.clicked.connect(self.browse_file)
        self.ui.export_btn.clicked.connect(self.export_audio)
        self.ui.bitrateSlider.valueChanged.connect(self.update_bitrate_label)

    def browse_file(self):
        """Open a file dialog to select an audio file."""
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.ui, "Select Audio File", "", "Audio Files (*.mp3 *.wav *.flac)"
        )
        if file_name:
            self.ui.file_label.setText(file_name)
            self.update_audio_settings(file_name)

    def update_audio_settings(self, file_path):
        """Update UI elements based on the selected audio file's properties."""
        info = self.processor.get_audio_info(file_path)
        if not info:
            self.ui.audioDetailsLabel.setText("Could not read audio info.")
            return

        mins, secs = divmod(int(info["duration"]), 60)
        duration_str = f"{mins}:{secs:02d} min"
        bitrate_kbps = info["bitrate"] // 1000
        sample_rate_str = f"{info['sample_rate'] / 1000:.1f} kHz"
        channels_str = "Mono" if info["channels"] == 1 else "Stereo"

        self.ui.audioDetailsLabel.setText(
            f"{info['filename']} - {duration_str} | {bitrate_kbps} kbps, {sample_rate_str} | {channels_str}"
        )
        self.ui.bitrateSlider.setMaximum(max(bitrate_kbps, 320))
        self.ui.stereoSwitch.setChecked(info["channels"] == 1)

    def update_bitrate_label(self):
        """Update the bitrate label when the slider value changes."""
        self.ui.bitrate_label.setText(f"Bitrate: {self.ui.bitrateSlider.value()}k")

    def export_audio(self):
        """Export the audio file with the selected settings."""
        input_file = self.ui.file_label.text()
        if not input_file:
            QtWidgets.QMessageBox.warning(self.ui, "No File", "Please select an audio file first.")
            return

        output_file = input_file.rsplit('.', 1)[0] + "_processed.mp3"
        bitrate = f"{self.ui.bitrateSlider.value()}k"
        sample_rate = int(self.ui.sampleRateCombo.currentText())
        mono = self.ui.stereoSwitch.isChecked()

        if os.path.exists(output_file):
            msg = QtWidgets.QMessageBox.question(
                self.ui, "Overwrite?", "Output file exists. Overwrite?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No
            )
            if msg != QtWidgets.QMessageBox.Yes:
                return

        try:
            self.processor.compress(input_file, output_file, bitrate, sample_rate, mono)
            QtWidgets.QMessageBox.information(self.ui, "Success", "Audio exported successfully!")
        except Exception as exc:
            QtWidgets.QMessageBox.critical(self.ui, "Error", f"Failed to export audio:\n{exc}")
