from PyQt6.QtGui import QColor
from PyQt6.QtCore import QRect


class PalletRect(QRect):
    """A child class of QRect, which adds a .color property. Requires a color= keyword argument."""
    def __init__(self, *args, color) -> None:
        super().__init__(*args)
        self.color: QColor = QColor(color)
