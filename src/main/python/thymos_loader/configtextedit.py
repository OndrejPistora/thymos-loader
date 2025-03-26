from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtCore import pyqtSignal, QEvent

class ConfigTextEdit(QTextEdit):
    editingFinished = pyqtSignal()

    def focusOutEvent(self, event: QEvent):
        self.editingFinished.emit()
        super().focusOutEvent(event)