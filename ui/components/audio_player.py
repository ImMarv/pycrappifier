from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QSlider
from PyQt5.QtCore import Qt, QTimer


class AudioPlayer(QWidget):
    """A reusable audio player component."""

    def __init__(self, parent=None, player=None, processor=None):
        super().__init__(parent)
        self.player = player
        self.processor = processor
        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_music_player_slider)
        self.init_ui()

    def init_ui(self):
        """Initialize the UI components."""
        self.audioDetailsLabel = QLabel("No file selected")
        self.audioDetailsLabel.setVisible(False)

        self.music_slider = QSlider(Qt.Horizontal)
        self.music_slider.setMinimum(0)
        self.music_slider.setMaximum(0)
        self.music_slider.sliderMoved.connect(self.update_slider_position)

        self.play_btn = QPushButton("▶")
        self.pause_btn = QPushButton("⏸")
        self.stop_btn = QPushButton("⏹")
        self.elapsed_time_label = QLabel("0:00")

        for btn in (self.play_btn, self.pause_btn, self.stop_btn):
            btn.setFixedSize(30, 30)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.play_btn)
        button_layout.addWidget(self.pause_btn)
        button_layout.addWidget(self.stop_btn)
        button_layout.addWidget(self.elapsed_time_label)

        layout = QVBoxLayout()
        layout.addWidget(self.audioDetailsLabel)
        layout.addWidget(self.music_slider)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.play_btn.clicked.connect(self.music_player_play)
        self.pause_btn.clicked.connect(self.music_player_pause)
        self.stop_btn.clicked.connect(self.music_player_stop)

    def set_player(self, player):
        """Attach the backend player instance."""
        self.player = player

    def update_audio_settings(self, file_path=None):
        """Update UI elements based on the selected audio file's properties."""
        if not file_path:
            return

        if not self.processor or not hasattr(self.processor, "get_audio_info"):
            self.audioDetailsLabel.setVisible(True)
            self.audioDetailsLabel.setText(file_path)
            return

        info = self.processor.get_audio_info(file_path)
        if not info:
            self.audioDetailsLabel.setVisible(True)
            self.audioDetailsLabel.setText("Could not read audio info.")
            return

        self.audioDetailsLabel.setVisible(True)

        mins, secs = divmod(int(info["duration"]), 60)
        duration_str = f"{mins}:{secs:02d} min"
        bitrate_kbps = info["bitrate"] // 1000
        sample_rate_str = f"{info['sample_rate'] / 1000:.1f} kHz"
        channels_str = "Mono" if info["channels"] == 1 else "Stereo"

        self.audioDetailsLabel.setText(
            f"{info['filename']} - {duration_str} | {bitrate_kbps} kbps, {sample_rate_str} | {channels_str}"
        )
        self.update_music_player_slider_length()

    def music_player_play(self):
        """Starts the music player and timer."""
        if not self.player or not hasattr(self.player, "play"):
            return
        self.player.play()
        self.timer.start()
        setattr(self.player, "is_playing", True)

    def music_player_stop(self):
        """Stops the music player and reset the timer and slider."""
        if not self.player or not hasattr(self.player, "stop"):
            return
        self.player.stop()
        self.timer.stop()
        setattr(self.player, "is_playing", False)
        self.music_slider.setValue(0)

    def music_player_pause(self):
        """Pauses the music player and stops the timer."""
        if not self.player or not hasattr(self.player, "pause"):
            return
        self.player.pause()
        self.timer.stop()
        setattr(self.player, "is_playing", False)

    def update_music_player_slider_length(self):
        """Updates the length of the music player slider based on the audio's total length."""
        if not self.player or not hasattr(self.player, "get_duration"):
            return
        total_length = self.player.get_duration()
        self.music_slider.setMaximum(total_length)
        self.music_slider.setValue(0)

    def update_music_player_slider(self):
        """Updates the position slider based on the audio's current timeframe."""
        if not self.player:
            return
        is_playing = getattr(self.player, "is_playing", False)
        if is_playing:
            self.update_music_player_slider_length()
            current_pos = int(self.player.get_current_position())
            self.elapsed_time_label.setText(f"{current_pos // 60000}:{(current_pos // 1000) % 60:02d}")
            self.music_slider.setValue(current_pos)

    def update_slider_position(self, position):
        """Updates the audio player's position based on the UI values."""
        if not self.player:
            return
        if hasattr(self.player, "set_position"):
            self.player.set_position(position)
        elif hasattr(self.player, "player") and hasattr(self.player.player, "setPosition"):
            self.player.player.setPosition(position)
