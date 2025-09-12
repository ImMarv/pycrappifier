import sys
from PyQt5.QtWidgets import QApplication
from ui import AudioExporterUI
import ffmpeg_bitrate as logic

def main():
    app = QApplication(sys.argv)
    window = AudioExporterUI()
    logic.connect_signals(window)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
