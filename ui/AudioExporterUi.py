import sys
try:
    from PyQt5 import QtWidgets, QtCore
    from PyQt5.QtWidgets import QPushButton, QLabel, QCheckBox, QHBoxLayout, QVBoxLayout
except ImportError as exc:
    raise ImportError("PyQt5 is required to run this application. Please install it via pip.") from exc

class AudioExporterUI(QtWidgets.QWidget):
    """UI class for the audio exporter application."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pycrappify")
        self.setFixedSize(480, 320)
        self.setStyleSheet("background-color: #1a1a1f; color: white; font-size: 12pt;")

        # === File selection ===
        self.browse_btn = QPushButton("Choose File")
        self.file_label = QLabel("")
        self.file_label.setVisible(False)
        file_layout = QHBoxLayout()
        file_layout.addWidget(self.browse_btn)
        file_layout.addWidget(self.file_label)

        # === Song Details ===
        self.audioDetailsLabel = QLabel("")
        self.audioDetailsLabel.setVisible(False)
        audioDetailsLayout = QHBoxLayout()
        audioDetailsLayout.setAlignment(QtCore.Qt.AlignCenter)
        audioDetailsLayout.addWidget(self.audioDetailsLabel)

        # === Music Player ===
        self.play_btn = QPushButton("▶")
        self.pause_btn = QPushButton("⏸")
        self.stop_btn = QPushButton("⏹")
        self.elapsed_time_label = QLabel("0:00")

        for btn in (self.play_btn, self.stop_btn):
            btn.setFixedSize(30, 30)

        self.music_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)

        controlsLayout = QHBoxLayout()
        controlsLayout.setAlignment(QtCore.Qt.AlignCenter)
        controlsLayout.setSpacing(8)
        controlsLayout.addWidget(self.play_btn)
        controlsLayout.addWidget(self.pause_btn)
        controlsLayout.addWidget(self.stop_btn)
        controlsLayout.addWidget(self.music_slider)
        controlsLayout.addWidget(self.elapsed_time_label)

        musicPlayerLayout = QVBoxLayout()
        musicPlayerLayout.addLayout(controlsLayout)


        # === Bitrate slider ===
        self.bitrate_label = QLabel("Bitrate: ")
        self.bitrate_label = QtWidgets.QLabel("Bitrate: ")
        self.bitrateSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.bitrateSlider.setMinimum(1)
        self.bitrateSlider.setMaximum(320)
        self.bitrateSlider.setValue(160)

        bitrateSlider_layout = QtWidgets.QHBoxLayout()
        bitrateSlider_layout.addWidget(self.bitrate_label)
        bitrateSlider_layout.addWidget(self.bitrateSlider)

        # === Sample Rate Combo Box ===
        self.sample_rates = [8000, 12000, 16000, 22050, 32000, 44100, 48000]
        self.sample_rates = [8000, 12000, 16000, 22050, 32000, 44100, 48000]
        self.sample_rate_label = QLabel("Sample Rate: ")
        self.sampleRateCombo = QtWidgets.QComboBox()
        self.sampleRateCombo.addItems([str(rate) for rate in self.sample_rates])
        self.sampleRateCombo.setCurrentIndex(self.sample_rates.index(44100))
        sample_rate_layout = QHBoxLayout()
        sample_rate_layout.addWidget(self.sample_rate_label)
        sample_rate_layout.addWidget(self.sampleRateCombo)

        # === Stereo to Mono CheckBox ===
        self.stereo_label = QLabel("Mono")
        self.stereoSwitch = QCheckBox()
        self.stereoSwitch.setChecked(False)
        stereo_layout = QHBoxLayout()
        stereo_layout.addWidget(self.stereo_label)
        stereo_layout.addWidget(self.stereoSwitch)

        # === Export button ===
        self.export_btn = QPushButton("Export")
        exportButton_layout = QHBoxLayout()
        exportButton_layout.addWidget(self.export_btn)

        # === Main layout ===
        ## Info layout
        info_layout = QVBoxLayout()
        info_layout.addLayout(file_layout)
        info_layout.addLayout(audioDetailsLayout)
        ## Settings layout
        settings_layout = QVBoxLayout()
        settings_layout.addLayout(bitrateSlider_layout)
        settings_layout.addSpacing(5)
        settings_layout.addLayout(sample_rate_layout)
        settings_layout.addSpacing(5)
        settings_layout.addLayout(stereo_layout)
        ## Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(info_layout)
        main_layout.addLayout(musicPlayerLayout)
        main_layout.addLayout(settings_layout)
        main_layout.addSpacing(5)
        ## Export button layout
        main_layout.addLayout(exportButton_layout)
        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AudioExporterUI()
    window.show()
    sys.exit(app.exec_())
