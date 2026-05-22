from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QSlider, QComboBox, QCheckBox
from PyQt5.QtCore import pyqtSignal, Qt

from core.dto.command import SamplingMode


class EffectsPanel(QWidget):
    """Bitcrush settings panel."""

    settings_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.bitcrush_switch = QCheckBox("Enable bitcrush")
        self.bitcrush_switch.toggled.connect(self._sync_visibility)
        self.bitcrush_switch.toggled.connect(self.settings_changed.emit)

        self.bitcrush_level_in_slider = QSlider(Qt.Horizontal)
        self.bitcrush_level_in_slider.setRange(2, 640)
        self.bitcrush_level_in_slider.setValue(20)
        self.bitcrush_level_in_slider.valueChanged.connect(self.settings_changed.emit)

        self.bitcrush_level_out_slider = QSlider(Qt.Horizontal)
        self.bitcrush_level_out_slider.setRange(2, 640)
        self.bitcrush_level_out_slider.setValue(20)
        self.bitcrush_level_out_slider.valueChanged.connect(self.settings_changed.emit)

        self.bitcrush_bits_slider = QSlider(Qt.Horizontal)
        self.bitcrush_bits_slider.setRange(1, 64)
        self.bitcrush_bits_slider.setValue(8)
        self.bitcrush_bits_slider.valueChanged.connect(self.settings_changed.emit)

        self.bitcrush_mix_slider = QSlider(Qt.Horizontal)
        self.bitcrush_mix_slider.setRange(0, 100)
        self.bitcrush_mix_slider.setValue(100)
        self.bitcrush_mix_slider.valueChanged.connect(self.settings_changed.emit)

        self.bitcrush_sampling_combo = QComboBox()
        self.bitcrush_sampling_combo.addItems(["Linear", "Logarithmic"])
        self.bitcrush_sampling_combo.currentIndexChanged.connect(self.settings_changed.emit)

        self.bitcrush_settings_widget = QWidget(self)
        settings_layout = QVBoxLayout(self.bitcrush_settings_widget)
        settings_layout.addWidget(QLabel("Level in"))
        settings_layout.addWidget(self.bitcrush_level_in_slider)
        settings_layout.addWidget(QLabel("Level out"))
        settings_layout.addWidget(self.bitcrush_level_out_slider)
        settings_layout.addWidget(QLabel("Bits"))
        settings_layout.addWidget(self.bitcrush_bits_slider)
        settings_layout.addWidget(QLabel("Mix"))
        settings_layout.addWidget(self.bitcrush_mix_slider)
        settings_layout.addWidget(QLabel("Sampling mode"))
        settings_layout.addWidget(self.bitcrush_sampling_combo)

        layout = QVBoxLayout()
        layout.addWidget(self.bitcrush_switch)
        layout.addWidget(self.bitcrush_settings_widget)
        self.setLayout(layout)
        self._sync_visibility(self.bitcrush_switch.isChecked())

    def _sync_visibility(self, enabled):
        self.bitcrush_settings_widget.setVisible(enabled)

    def get_bitcrush_settings(self):
        """Return the current bitcrush settings."""
        sampling_text = self.bitcrush_sampling_combo.currentText()
        return {
            "has_bitcrush": self.bitcrush_switch.isChecked(),
            "level_in": self.bitcrush_level_in_slider.value() / 10.0,
            "level_out": self.bitcrush_level_out_slider.value() / 10.0,
            "bits": self.bitcrush_bits_slider.value(),
            "mix": self.bitcrush_mix_slider.value() / 100.0,
            "sampling": SamplingMode.LINEAR if sampling_text == "Linear" else SamplingMode.LOGARITHMIC,
        }
