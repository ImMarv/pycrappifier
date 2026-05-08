import os
from PyQt5 import QtWidgets, QtCore # type: ignore
from core.AudioPlayer import AudioPlayer
from core.AudioProcessor import AudioProcessor
from core.dto.command import Command, SamplingMode

class MainWindow:
    """Controller that binds UI signals to logic."""

    def __init__(self, ui):
        self.ui = ui
        self.processor = AudioProcessor()
        self.audio_player = AudioPlayer()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)  # Update slider every 100 ms
        self.connect_signals()

    def connect_signals(self):
        """Connect UI signals to their respective slots."""
        self.ui.browse_btn.clicked.connect(self.browse_file)
        self.ui.export_btn.clicked.connect(self.export_audio)
        self.ui.bitrateSlider.valueChanged.connect(self.update_bitrate_label)
        # update the music player slider position every time the timer ticks
        self.ui.music_slider.sliderMoved.connect(self.update_slider_position)
        self.timer.timeout.connect(self.update_music_player_slider)
        self.ui.play_btn.clicked.connect(self.music_player_play)
        self.ui.pause_btn.clicked.connect(self.audio_player.pause)
        self.ui.stop_btn.clicked.connect(self.music_player_stop)
        self.ui.bitcrush_switch.stateChanged.connect(self.update_bitcrush_settings_visibility)

    def browse_file(self):
        """Open a file dialog to select an audio file."""
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.ui, "Select Audio File", "", "Audio Files (*.mp3 *.wav *.flac)"
        )
        if file_name:
            if self.audio_player.is_playing:
                self.audio_player.stop()
                self.ui.music_slider.setValue(0)
            self.ui.file_label.setVisible(True)
            self.ui.file_label.setText(file_name)
            self.update_audio_settings(file_name)
            self.audio_player.load(file_name)
            self.update_music_player_slider_length()

    def update_audio_settings(self, file_path=None):
        """Update UI elements based on the selected audio file's properties."""
        if not isinstance(file_path, str) or not file_path:
            file_path = self.ui.file_label.text()
        if not file_path:
            self.ui.audioDetailsLabel.setText("Could not read audio info.")
            return

        info = self.processor.get_audio_info(file_path)
        if not info:
            self.ui.audioDetailsLabel.setText("Could not read audio info.")
            return
        # unhide audio details label
        self.ui.audioDetailsLabel.setVisible(True)

        mins, secs = divmod(int(info["duration"]), 60)
        duration_str = f"{mins}:{secs:02d} min"
        bitrate_kbps = info["bitrate"] // 1000
        sample_rate_str = f"{info['sample_rate'] / 1000:.1f} kHz"
        channels_str = "Mono" if info["channels"] == 1 else "Stereo"

        self.ui.audioDetailsLabel.setText(
            f"{info['filename']} - {duration_str} | {bitrate_kbps} kbps, {sample_rate_str} | {channels_str}"
        )
        self.ui.bitrateSlider.setMaximum(max(bitrate_kbps, 320))
        self.ui.stereo_switch.setChecked(info["channels"] == 1)
    
    def update_bitcrush_settings_visibility(self):
        """Show or hide bitcrush settings based on the checkbox state."""
        is_bitcrush_enabled = self.ui.bitcrush_switch.isChecked()
        self.ui.bitcrush_settings_widget.setVisible(is_bitcrush_enabled)

    def update_bitcrush_settings(self):
        """Update bitcrush settings based on the UI inputs."""
        level_in = str(self.ui.bitcrush_level_in_slider.value() / 10.0)
        level_out = str(self.ui.bitcrush_level_out_slider.value() / 10.0)
        bits = str(self.ui.bitcrush_bits_slider.value())
        mix = str(self.ui.bitcrush_mix_slider.value() / 100.0)
        sampling_mode = self.ui.bitcrush_sampling_combo.currentText()
        sampling_mode = SamplingMode.LINEAR.name if sampling_mode == "Linear" else SamplingMode.LOGARITHMIC.name

    def update_bitrate_label(self):
        """Update the bitrate label when the slider value changes."""
        self.ui.bitrate_label.setText(f"Bitrate: {self.ui.bitrateSlider.value()}k")
    def music_player_play(self):
        """Starts the music player and timer."""
        self.audio_player.play()
        self.timer.start()
        self.audio_player.is_playing = True
    def music_player_stop(self):
        """Stops the music player and reset the timer and slider."""
        self.audio_player.stop()
        self.timer.stop()
        self.audio_player.is_playing = False
        self.ui.music_slider.setValue(0)
    def music_player_pause(self):
        """Pauses the music player and stops the timer."""
        self.audio_player.pause()
        self.timer.stop()
        self.audio_player.is_playing = False
    
    def update_music_player_slider_length(self):
        """Updates the length of the music player slider based on the audio's total length."""
        total_length = self.audio_player.get_duration()
        self.ui.music_slider.setMaximum(total_length)
        self.ui.music_slider.setValue(0)

    def update_music_player_slider(self):
        """Updates the position slider based on the audio's current timeframe."""
        if self.audio_player.is_playing:
            self.update_music_player_slider_length()  # ensure slider max is correct
            current_pos = int(self.audio_player.get_current_position())
            self.ui.elapsed_time_label.setText(f"{current_pos // 60000}:{(current_pos // 1000) % 60:02d}")
            self.ui.music_slider.setValue(current_pos)

    def update_slider_position(self, position):
        """Updates the audio player's position based on the UI values."""
        self.audio_player.player.setPosition(position)

    def export_audio(self):
        """Export the audio file with the selected settings."""
        input_file = self.ui.file_label.text()
        if not input_file:
            QtWidgets.QMessageBox.warning(self.ui, "No File", "Please select an audio file first.")
            return

        output_file = input_file.rsplit('.', 1)[0] + "_processed.mp3"
        bitrate = self.ui.bitrateSlider.value()
        sample_rate = int(self.ui.sampleRateCombo.currentText())
        level_in = self.ui.bitcrush_level_in_slider.value() / 10.0
        level_out = self.ui.bitcrush_level_out_slider.value() / 10.0
        bits = self.ui.bitcrush_bits_slider.value()
        mix = self.ui.bitcrush_mix_slider.value() / 100.0
        sampling_mode = self.ui.bitcrush_sampling_combo.currentText()
        if sampling_mode == "Linear":
            sampling_mode = SamplingMode.LINEAR
        else:
            sampling_mode = SamplingMode.LOGARITHMIC
        mono = self.ui.stereo_switch.isChecked()

        if os.path.exists(output_file):
            msg = QtWidgets.QMessageBox.question(
                self.ui, "Overwrite?", "Output file exists. Overwrite?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No
            )
            if msg != QtWidgets.QMessageBox.Yes:
                return
        command = Command(
            input_file=input_file,
            output_file=output_file,
            bitrate=bitrate,
            sample_Rate=sample_rate,
            level_in=level_in,
            level_out=level_out,
            bits=bits,
            mix=mix,
            sampling=sampling_mode,
            has_bitcrush=self.ui.bitcrush_switch.isChecked(),
            overwrite=True,
            mono=mono
        )

        try:
            self.processor.compress(command)
            QtWidgets.QMessageBox.information(self.ui, "Success", "Audio exported successfully!")
        except Exception as exc:
            QtWidgets.QMessageBox.critical(self.ui, "Error", f"Failed to export audio:\n{exc}")
