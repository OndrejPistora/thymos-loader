from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import  QVariantAnimation, QEasingCurve
from PyQt6.QtGui import QColor

class FlashLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.default_color = self.palette().color(self.backgroundRole())

    def flash_green(self, duration=1000):
        start_color = QColor("lightgreen")
        end_color = QColor(self.default_color)

        self.anim = QVariantAnimation(
            startValue=start_color,
            endValue=end_color,
            duration=duration,
            easingCurve=QEasingCurve.Type.InOutQuad
        )
        self.anim.valueChanged.connect(self._update_background)
        self.anim.finished.connect(self._clear_stylesheet)
        self.anim.start()

    def _update_background(self, color):
        rgba = color.name(QColor.NameFormat.HexArgb)
        self.setStyleSheet(f"background-color: {rgba};")

    def _clear_stylesheet(self):
        self.setStyleSheet("")