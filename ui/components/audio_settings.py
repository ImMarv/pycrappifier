from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSlider, QComboBox, QCheckBox
from PyQt5.QtCore import pyqtSignal, Qt


class AudioSettings(QWidget):
    """A reusable audio settings component."""

    settings_changed = pyqtSignal()

    def __init__(self, parent=None, processor=None):
        super().__init__(parent)
        self.processor = processor
        self.init_ui()

    def init_ui(self):
        self.bitrate_label = QLabel("Bitrate: ")
        self.bitrateSlider = QSlider(Qt.Horizontal)
        self.bitrateSlider.setMinimum(1)
        self.bitrateSlider.setMaximum(320)
        self.bitrateSlider.setValue(160)
        self.bitrateSlider.valueChanged.connect(self.update_bitrate_label)
        self.bitrateSlider.valueChanged.connect(self.settings_changed.emit)

        bitrateSlider_layout = QHBoxLayout()
        bitrateSlider_layout.addWidget(self.bitrate_label)
        bitrateSlider_layout.addWidget(self.bitrateSlider)

        self.sample_rates = [8000, 12000, 16000, 22050, 32000, 44100, 48000]
        self.sample_rate_label = QLabel("Sample Rate: ")
        self.sampleRateCombo = QComboBox()
        self.sampleRateCombo.addItems([str(rate) for rate in self.sample_rates])
        try:
            idx = self.sample_rates.index(44100)
            self.sampleRateCombo.setCurrentIndex(idx)
        except ValueError:
            pass
        self.sampleRateCombo.currentIndexChanged.connect(self.settings_changed.emit)

        self.monoCheckBox = QCheckBox("Output mono")
        self.monoCheckBox.setChecked(False)
        self.monoCheckBox.toggled.connect(self.settings_changed.emit)

        sample_rate_layout = QHBoxLayout()
        sample_rate_layout.addWidget(self.sample_rate_label)
        sample_rate_layout.addWidget(self.sampleRateCombo)

        mono_layout = QHBoxLayout()
        mono_layout.addWidget(self.monoCheckBox)
        mono_layout.addStretch(1)

        main_layout = QVBoxLayout()
        main_layout.addLayout(bitrateSlider_layout)
        main_layout.addLayout(sample_rate_layout)
        main_layout.addLayout(mono_layout)
        self.setLayout(main_layout)

    def update_bitrate_label(self):
        """Update the bitrate label when the slider value changes."""
        self.bitrate_label.setText(f"Bitrate: {self.bitrateSlider.value()}k")

    def get_settings(self):
        """Return the current settings as a dictionary."""
        return {
            "bitrate": self.bitrateSlider.value(),
            "sample_rate": int(self.sampleRateCombo.currentText()),
            "mono": self.monoCheckBox.isChecked(),
        }

    def update_from_file(self, file_path):
        """Optional hook to update settings based on selected file."""
        if not file_path or not self.processor:
            return
        info = self.processor.get_audio_info(file_path)
        if not info:
            return

        bitrate_kbps = max(1, int(info.get("bitrate", 0) / 1000))
        self.bitrateSlider.setMaximum(max(320, bitrate_kbps))
        self.bitrateSlider.setValue(min(bitrate_kbps, self.bitrateSlider.maximum()))

        sr = info.get("sample_rate")
        if sr and sr in self.sample_rates:
            self.sampleRateCombo.setCurrentIndex(self.sample_rates.index(sr))
        self.monoCheckBox.setChecked(info.get("channels", 2) == 1)
