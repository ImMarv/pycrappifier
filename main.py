import sys
try:
    from PyQt5.QtWidgets import QApplication
except ImportError:
    try:
        from PySide2.QtWidgets import QApplication
    except ImportError:
        try:
            from PyQt6.QtWidgets import QApplication
        except ImportError:
            from PySide6.QtWidgets import QApplication
from ui.AudioExporterUi import AudioExporterUI

def main():
    app = QApplication(sys.argv)
    window = AudioExporterUI()
    window.show()
    # support bindings that expose exec() instead of exec_()
    exec_func = getattr(app, "exec_", getattr(app, "exec"))
    sys.exit(exec_func())

if __name__ == "__main__":
    main()
