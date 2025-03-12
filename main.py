# setup.py
from PyQt6.QtWidgets import QApplication
from src.MainWindow import FWHMWindow

if __name__ == "__main__":
    app = QApplication([])
    window = FWHMWindow()
    window.show()
    app.exec()

