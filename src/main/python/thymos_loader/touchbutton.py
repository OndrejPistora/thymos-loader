from PyQt6.QtWidgets import QApplication, QPushButton
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
            touch_point = self.mapToGlobal(self.rect().center()).toPointF()  # Convert to QPointF
            mouse_event = QMouseEvent(
                QEvent.Type.MouseButtonPress,
                touch_point,
                Qt.MouseButton.LeftButton,
                Qt.MouseButton.LeftButton,
                Qt.KeyboardModifier.NoModifier
            )
            QApplication.sendEvent(self, mouse_event)  # Trigger mouse press
            return True

        elif event.type() == QEvent.Type.TouchEnd:  # Detect finger release
            print(f"Touch UP on {self.text()}")
            touch_point = self.mapToGlobal(self.rect().center()).toPointF()  # Convert to QPointF
            mouse_event = QMouseEvent(
                QEvent.Type.MouseButtonRelease,
                touch_point,
                Qt.MouseButton.LeftButton,
                Qt.MouseButton.NoButton,
                Qt.KeyboardModifier.NoModifier
            )
            QApplication.sendEvent(self, mouse_event)  # Trigger mouse release
            return True

        return super().eventFilter(obj, event)