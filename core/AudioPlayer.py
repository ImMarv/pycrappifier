import os
import sys
from pygame import mixer

class AudioPlayer:
    def __init__(self):
        self.is_playing = False
        self.current_position = 0
        mixer.init()
    def get_current_position(self):
        if self.is_playing:
            return mixer.music.get_pos() / 1000  # return position in seconds
        return self.current_position
    def load(self, file_path):
        if os.path.exists(file_path):
            self.file_path = file_path
        else:
            raise FileNotFoundError("Audio file not found.")
    def play(self):
        mixer.music.load(self.file_path)
        mixer.music.play()
        self.is_playing = True
    def stop(self):
        self.is_playing = False
        self.current_position = 0
        mixer.music.stop()
    