from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QMouseEvent

class TouchButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setAttribute(Qt.WidgetAttribute.WA_AcceptTouchEvents)  # Enable touch events
        self.installEventFilter(self)  # Install event filter to handle touch

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.TouchBegin:  # Detect finger press
            print(f"Touch DOWN on {self.text()}")
            mouse_event = QMouseEvent(
                QEvent.Type.MouseButtonPress,
                self.rect().center(),  # Center of the button
                Qt.MouseButton.LeftButton,
                Qt.MouseButton.LeftButton,
                Qt.KeyboardModifier.NoModifier
            )
            QApplication.sendEvent(self, mouse_event)  # Trigger mouse press
            return True

        elif event.type() == QEvent.Type.TouchEnd:  # Detect finger release
            print(f"Touch UP on {self.text()}")
            mouse_event = QMouseEvent(
                QEvent.Type.MouseButtonRelease,
                self.rect().center(),
                Qt.MouseButton.LeftButton,
                Qt.MouseButton.NoButton,
                Qt.KeyboardModifier.NoModifier
            )
            QApplication.sendEvent(self, mouse_event)  # Trigger mouse release
            return True

        return super().eventFilter(obj, event)

class TouchApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Touch Button Example")

        # Create buttons using the new TouchButton class
        self.buttonUp = TouchButton("UP", self)
        self.buttonDown = TouchButton("DOWN", self)

        # Set positions
        self.buttonUp.setGeometry(50, 50, 100, 50)
        self.buttonDown.setGeometry(50, 120, 100, 50)

        # Connect buttons to movement functions
        self.buttonUp.pressed.connect(lambda: self.start_moving("UP"))
        self.buttonDown.pressed.connect(lambda: self.start_moving("DOWN"))
        self.buttonUp.released.connect(self.stop_moving)
        self.buttonDown.released.connect(self.stop_moving)

    def start_moving(self, direction):
        print(f"Moving {direction}...")

    def stop_moving(self):
        print("Stopping movement...")

if __name__ == "__main__":
    app = QApplication([])
    window = TouchApp()
    window.show()
    app.exec()