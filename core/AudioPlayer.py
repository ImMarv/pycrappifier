from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent # type: ignore
from PyQt5.QtCore import QUrl # type: ignore


class AudioPlayer:
    def __init__(self):
        self.player = QMediaPlayer()
        self.player.setVolume(100)
        self.is_playing = False
    def load(self, file_path):
        url = QUrl.fromLocalFile(file_path)
        self.player.setMedia(QMediaContent(url))
    def play(self):
        self.player.play()
    def pause(self):
        self.player.pause()
    def stop(self):
        self.player.stop()
    def get_current_position(self):
        return self.player.position()
    def get_duration(self):
        return self.player.duration()
    