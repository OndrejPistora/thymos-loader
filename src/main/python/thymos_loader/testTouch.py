from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt, QEvent

class TouchWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Touch Event Test")

        # Install event filter
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.TouchBegin:  # Finger Down
            print("Touch DOWN detected!")
            return True  # Stop further processing

        elif event.type() == QEvent.Type.TouchEnd:  # Finger Up
            print("Touch UP detected!")
            return True  # Stop further processing

        return super().eventFilter(obj, event)

if __name__ == "__main__":
    app = QApplication([])
    window = TouchWindow()
    window.show()
    app.exec()