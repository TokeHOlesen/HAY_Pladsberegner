from PyQt6.QtGui import QColor
from PyQt6.QtCore import QRect


class PalletRect(QRect):
    def __init__(self, *args, color=QColor("white")):
        super().__init__(*args)
        self.color = QColor(color)
