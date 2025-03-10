from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt, QEvent, QPointF
from PyQt6.QtGui import QMouseEvent

class TouchButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_AcceptTouchEvents)  # Enable touch events
        self.installEventFilter(self)  # Install event filter to handle touch

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.TouchBegin:  # Detect touch press
            touch_point = self.mapToGlobal(self.rect().center()).toPointF()
            mouse_event = QMouseEvent(
                QEvent.Type.MouseButtonPress,
                touch_point,
                Qt.MouseButton.LeftButton,
                Qt.MouseButton.LeftButton,
                Qt.KeyboardModifier.NoModifier
            )
            self.setDown(True)  # Visually press button
            self.clicked.emit()  # Manually trigger clicked() signal
            return True

        elif event.type() == QEvent.Type.TouchEnd:  # Detect touch release
            touch_point = self.mapToGlobal(self.rect().center()).toPointF()
            mouse_event = QMouseEvent(
                QEvent.Type.MouseButtonRelease,
                touch_point,
                Qt.MouseButton.LeftButton,
                Qt.MouseButton.NoButton,
                Qt.KeyboardModifier.NoModifier
            )
            self.setDown(False)  # Release button visually
            return True

        return super().eventFilter(obj, event)