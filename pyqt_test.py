import sys
import arrangement_rect_generator as arr_rect_gen
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow

WIDGET_RECT_HEIGHT = 13.6
WIDGET_RECT_WIDTH = 2.4


class TruckView(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(320, 480)
        self.aspect = WIDGET_RECT_HEIGHT / WIDGET_RECT_WIDTH
        self.x_pos = 20
        self.y_pos = 4
        self.brush_offset = 0
        self.pallet_rects = []
        self.gutter = self.width() // 110
        self.standard_pallet_width = 0
        self.border_rect = None

    def update_standard_pallet_width(self):
        pallet_width = self.width() - 4 * self.gutter // 3
        while pallet_width > 0:
            truck_rect_width = 3 * pallet_width + 4 * self.gutter
            truck_rect_height = int(round(truck_rect_width * self.aspect))
            if truck_rect_width <= self.width() and truck_rect_height <= self.height():
                break
            pallet_width -= 1
        self.standard_pallet_width = pallet_width

    def update_border_rect(self):
        width = 3 * self.standard_pallet_width + 4 * self.gutter
        height = int(round(width * self.aspect))
        self.border_rect = QRect(self.x_pos, self.y_pos, width, height)

    def draw_border_rect(self, painter):
        painter.setPen(QPen(QColor("#111"), 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(self.border_rect)

    def generate_arrangement(self, arrangement):
        x = self.border_rect.left() + self.gutter
        y = self.border_rect.top() + self.gutter + self.brush_offset
        generated_pallet_rects, new_brush_offset = arr_rect_gen.generate[arrangement](x,
                                                                                      y,
                                                                                      self.standard_pallet_width,
                                                                                      self.border_rect,
                                                                                      self.gutter)

        self.pallet_rects.extend(generated_pallet_rects)
        self.brush_offset += new_brush_offset

    def draw_pallets(self, painter):
        fill_color = QColor("#87c6ff")

        for pallet in self.pallet_rects:
            painter.fillRect(pallet, fill_color)
            painter.setPen(QPen(QColor("black"), 1))
            painter.drawRect(pallet)

    def paintEvent(self, _):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        self.gutter = self.height() // 200
        self.update_standard_pallet_width()
        self.update_border_rect()

        self.pallet_rects = []
        self.brush_offset = 0
        self.generate_arrangement((60, 60, 60))
        self.generate_arrangement((120, 120, 120))
        self.generate_arrangement((120, 120))

        self.draw_border_rect(painter)
        self.draw_pallets(painter)

        painter.end()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Vector drawing test")
        self.setCentralWidget(TruckView())
        self.resize(500, 900)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
