from PyQt6.QtWidgets import QProgressBar
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtCore import Qt

class ZeroProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(Qt.GlobalColor.red, 2))  # Red line for zero
        progress_range = self.maximum() - self.minimum()
        zero_pos = abs(self.minimum()) / progress_range if progress_range != 0 else 0.5
        mid_y = int(self.height() * (1 - zero_pos))  # Corrected zero-line position
        painter.drawLine(0, mid_y, self.width(), mid_y)