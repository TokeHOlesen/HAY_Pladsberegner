import sys
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow

WIDGET_RECT_WIDTH = 2.4
WIDGET_RECT_HEIGHT = 13.6
# Not needed - remove
PALLET_WIDTH = 0.8
PALLET_HEIGHT = 1.2
GUTTER = 4


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

    def update_standard_pallet_width(self):
        standard_pallet_width = self.width() - 4 * self.gutter // 3
        while standard_pallet_width > 0:
            truck_rect_width = 3 * standard_pallet_width + 4 * self.gutter
            truck_rect_height = int(round(truck_rect_width * self.aspect))
            if truck_rect_width <= self.width() and truck_rect_height <= self.height():
                break
            standard_pallet_width -= 1
        return standard_pallet_width

    def update_border_rect(self, standard_pallet_width):
        width = 3 * standard_pallet_width + 4 * self.gutter
        height = int(round(width * self.aspect))
        return QRect(self.x_pos, self.y_pos, width, height)

    @staticmethod
    def draw_border_rect(painter, border_rect):
        painter.setPen(QPen(QColor("#111"), 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(border_rect)

    def generate_60_60_60(self, standard_pallet_width, border_rect):
        initial_x = border_rect.left() + self.gutter
        initial_y = border_rect.top() + self.gutter + self.brush_offset
        pallet_width_px = standard_pallet_width
        pallet_height_px = border_rect.height() // 21 - (self.gutter * 2)

        self.pallet_rects.append(QRect(initial_x,
                                       initial_y,
                                       pallet_width_px,
                                       pallet_height_px))

        self.pallet_rects.append(QRect(initial_x + pallet_width_px + self.gutter,
                                       initial_y,
                                       pallet_width_px,
                                       pallet_height_px))

        self.pallet_rects.append(QRect(initial_x + 2 * (pallet_width_px + self.gutter),
                                       initial_y,
                                       pallet_width_px,
                                       pallet_height_px))

        self.brush_offset += pallet_height_px + self.gutter

    def generate_120_120_120(self, standard_pallet_width, border_rect):
        initial_x = border_rect.left() + self.gutter
        initial_y = border_rect.top() + self.gutter + self.brush_offset
        pallet_width_px = standard_pallet_width
        pallet_height_px = border_rect.height() // 11 - (self.gutter * 2)

        self.pallet_rects.append(QRect(initial_x,
                                       initial_y,
                                       pallet_width_px,
                                       pallet_height_px))

        self.pallet_rects.append(QRect(initial_x + pallet_width_px + self.gutter,
                                       initial_y,
                                       pallet_width_px,
                                       pallet_height_px))

        self.pallet_rects.append(QRect(initial_x + 2 * (pallet_width_px + self.gutter),
                                       initial_y,
                                       pallet_width_px,
                                       pallet_height_px))

        self.brush_offset += pallet_height_px + self.gutter

    def generate_120_120(self, standard_pallet_width, border_rect):
        initial_x = border_rect.left() + self.gutter
        initial_y = border_rect.top() + self.gutter + self.brush_offset
        pallet_width_px = (border_rect.width() - self.gutter * 3) // 2
        pallet_last_width_px = border_rect.width() - pallet_width_px - self.gutter * 3
        pallet_height_px = int(round(border_rect.height() / 16.1)) - (self.gutter * 2)

        self.pallet_rects.append(QRect(initial_x,
                                       initial_y,
                                       pallet_width_px,
                                       pallet_height_px))

        self.pallet_rects.append(QRect(initial_x + pallet_width_px + self.gutter,
                                       initial_y,
                                       pallet_last_width_px,
                                       pallet_height_px))

        self.brush_offset += pallet_height_px + self.gutter

    def generate_120_120_60_60(self, standard_pallet_width, border_rect):
        initial_x = border_rect.left() + self.gutter
        initial_y = border_rect.top() + self.gutter + self.brush_offset
        pallet_width_px = standard_pallet_width
        p120_height_px = border_rect.height() // 11 - (self.gutter * 2)
        p60_height_px = (p120_height_px - self.gutter) // 2
        p60_last_height_px = p120_height_px - p60_height_px - self.gutter

        self.pallet_rects.append(QRect(initial_x,
                                       initial_y,
                                       pallet_width_px,
                                       p120_height_px))

        self.pallet_rects.append(QRect(initial_x + pallet_width_px + self.gutter,
                                       initial_y,
                                       pallet_width_px,
                                       p120_height_px))

        self.pallet_rects.append(QRect(initial_x + 2 * (pallet_width_px + self.gutter),
                                       initial_y,
                                       pallet_width_px,
                                       p60_height_px))

        self.pallet_rects.append(QRect(initial_x + 2 * (pallet_width_px + self.gutter),
                                       initial_y + p60_height_px + self.gutter,
                                       pallet_width_px,
                                       p60_last_height_px))

        self.brush_offset += p120_height_px + self.gutter

    def generate_17080_17080_120_60(self, standard_pallet_width, border_rect):
        initial_x = border_rect.left() + self.gutter
        initial_y = border_rect.top() + self.gutter + self.brush_offset
        pallet_width_px = standard_pallet_width
        p170_height_px = int(round(border_rect.height() / 7.45)) - (self.gutter * 2)
        p120_height_px = border_rect.height() // 11 - (self.gutter * 2)
        p60_height_px = p170_height_px - p120_height_px - self.gutter

        self.pallet_rects.append(QRect(initial_x,
                                       initial_y,
                                       pallet_width_px,
                                       p170_height_px))

        self.pallet_rects.append(QRect(initial_x + pallet_width_px + self.gutter,
                                       initial_y,
                                       pallet_width_px,
                                       p170_height_px))

        self.pallet_rects.append(QRect(initial_x + 2 * (pallet_width_px + self.gutter),
                                       initial_y,
                                       pallet_width_px,
                                       p120_height_px))

        self.pallet_rects.append(QRect(initial_x + 2 * (pallet_width_px + self.gutter),
                                       initial_y + p120_height_px + self.gutter,
                                       pallet_width_px,
                                       p60_height_px))

        self.brush_offset += p170_height_px + self.gutter

    def generate_17080_120_120_60_60(self, standard_pallet_width, border_rect):
        initial_x = border_rect.left() + self.gutter
        initial_y = border_rect.top() + self.gutter + self.brush_offset
        pallet_width_px = standard_pallet_width
        p170_height_px = int(round(border_rect.height() / 7.45)) - (self.gutter * 2)
        p120_height_px = border_rect.height() // 11 - (self.gutter * 2)
        p60_height_px = p170_height_px - p120_height_px - self.gutter

        self.pallet_rects.append(QRect(initial_x,
                                       initial_y,
                                       pallet_width_px,
                                       p170_height_px))

        self.pallet_rects.append(QRect(initial_x + pallet_width_px + self.gutter,
                                       initial_y,
                                       pallet_width_px,
                                       p120_height_px))

        self.pallet_rects.append(QRect(initial_x + 2 * (pallet_width_px + self.gutter),
                                       initial_y,
                                       pallet_width_px,
                                       p120_height_px))

        self.pallet_rects.append(QRect(initial_x + pallet_width_px + self.gutter,
                                       initial_y + p120_height_px + self.gutter,
                                       pallet_width_px,
                                       p60_height_px))

        self.pallet_rects.append(QRect(initial_x + 2 * (pallet_width_px + self.gutter),
                                       initial_y + p120_height_px + self.gutter,
                                       pallet_width_px,
                                       p60_height_px))

        self.brush_offset += p170_height_px + self.gutter

    def generate_120_60_60_60_60(self, standard_pallet_width, border_rect):
        initial_x = border_rect.left() + self.gutter
        initial_y = border_rect.top() + self.gutter + self.brush_offset
        pallet_width_px = standard_pallet_width
        p120_height_px = border_rect.height() // 11 - (self.gutter * 2)
        p60_height_px = (p120_height_px - self.gutter) // 2
        p60_last_height_px = p120_height_px - p60_height_px - self.gutter

        self.pallet_rects.append(QRect(initial_x,
                                       initial_y,
                                       pallet_width_px,
                                       p120_height_px))

        self.pallet_rects.append(QRect(initial_x + pallet_width_px + self.gutter,
                                       initial_y,
                                       pallet_width_px,
                                       p60_height_px))

        self.pallet_rects.append(QRect(initial_x + 2 * (pallet_width_px + self.gutter),
                                       initial_y,
                                       pallet_width_px,
                                       p60_height_px))

        self.pallet_rects.append(QRect(initial_x + pallet_width_px + self.gutter,
                                       initial_y + p60_height_px + self.gutter,
                                       pallet_width_px,
                                       p60_last_height_px))

        self.pallet_rects.append(QRect(initial_x + 2 * (pallet_width_px + self.gutter),
                                       initial_y + p60_height_px + self.gutter,
                                       pallet_width_px,
                                       p60_last_height_px))

        self.brush_offset += p120_height_px + self.gutter

    def generate_145_145_145(self, standard_pallet_width, border_rect):
        initial_x = border_rect.left() + self.gutter
        initial_y = border_rect.top() + self.gutter + self.brush_offset
        pallet_width_px = standard_pallet_width
        pallet_height_px = border_rect.height() // 9 - (self.gutter * 2)

        self.pallet_rects.append(QRect(initial_x,
                                       initial_y,
                                       pallet_width_px,
                                       pallet_height_px))

        self.pallet_rects.append(QRect(initial_x + pallet_width_px + self.gutter,
                                       initial_y,
                                       pallet_width_px,
                                       pallet_height_px))

        self.pallet_rects.append(QRect(initial_x + 2 * (pallet_width_px + self.gutter),
                                       initial_y,
                                       pallet_width_px,
                                       pallet_height_px))

        self.brush_offset += pallet_height_px + self.gutter

    def generate_17080_17080_17080(self, standard_pallet_width, border_rect):
        initial_x = border_rect.left() + self.gutter
        initial_y = border_rect.top() + self.gutter + self.brush_offset
        pallet_width_px = standard_pallet_width
        pallet_height_px = int(round(border_rect.height() / 7.45)) - (self.gutter * 2)

        self.pallet_rects.append(QRect(initial_x,
                                       initial_y,
                                       pallet_width_px,
                                       pallet_height_px))

        self.pallet_rects.append(QRect(initial_x + pallet_width_px + self.gutter,
                                       initial_y,
                                       pallet_width_px,
                                       pallet_height_px))

        self.pallet_rects.append(QRect(initial_x + 2 * (pallet_width_px + self.gutter),
                                       initial_y,
                                       pallet_width_px,
                                       pallet_height_px))

        self.brush_offset += pallet_height_px + self.gutter

    def generate_17090_145_145(self, standard_pallet_width, border_rect):
        initial_x = border_rect.left() + self.gutter
        initial_y = border_rect.top() + self.gutter + self.brush_offset
        p17090_width_px = int(round((border_rect.width() - self.gutter * 2) / 2.7))
        p145_width_px = border_rect.width() - p17090_width_px - self.gutter * 3
        p17090_height_px = int(round(border_rect.height() / 7.45)) - (self.gutter * 2)
        p145_height_px = border_rect.height() // 15 - (self.gutter * 2)

        self.pallet_rects.append(QRect(initial_x,
                                       initial_y,
                                       p17090_width_px,
                                       p17090_height_px))

        self.pallet_rects.append(QRect(initial_x + p17090_width_px + self.gutter,
                                       initial_y,
                                       p145_width_px,
                                       p145_height_px))

        self.pallet_rects.append(QRect(initial_x + p17090_width_px + self.gutter,
                                       initial_y + p145_height_px + self.gutter,
                                       p145_width_px,
                                       p145_height_px))

        self.brush_offset += p17090_height_px + self.gutter

    def generate_17090_17090_130_130_130(self, standard_pallet_width, border_rect):
        initial_x = border_rect.left() + self.gutter
        initial_y = border_rect.top() + self.gutter + self.brush_offset
        p17090_width_px = int(round((border_rect.width() - self.gutter * 2) / 2.7))
        p130_width_px = border_rect.width() - p17090_width_px - self.gutter * 3
        p17090_height_px = int(round(border_rect.height() / 7.45)) - (self.gutter * 2)
        p130_height_px = int(round((p17090_height_px * 2 - self.gutter) / 3))
        p130_last_height_px = (p17090_height_px * 2 + self.gutter) - (p130_height_px + self.gutter) * 2

        self.pallet_rects.append(QRect(initial_x,
                                       initial_y,
                                       p17090_width_px,
                                       p17090_height_px))

        self.pallet_rects.append(QRect(initial_x,
                                       initial_y + p17090_height_px + self.gutter,
                                       p17090_width_px,
                                       p17090_height_px))

        self.pallet_rects.append(QRect(initial_x + p17090_width_px + self.gutter,
                                       initial_y,
                                       p130_width_px,
                                       p130_height_px))

        self.pallet_rects.append(QRect(initial_x + p17090_width_px + self.gutter,
                                       initial_y + p130_height_px + self.gutter,
                                       p130_width_px,
                                       p130_height_px))

        self.pallet_rects.append(QRect(initial_x + p17090_width_px + self.gutter,
                                       initial_y + (p130_height_px + self.gutter) * 2,
                                       p130_width_px,
                                       p130_last_height_px))

        self.brush_offset += (p17090_height_px + self.gutter) * 2

    def generate_130_120_120(self, standard_pallet_width, border_rect):
        initial_x = border_rect.left() + self.gutter
        initial_y = border_rect.top() + self.gutter + self.brush_offset
        p130_width_px = (border_rect.width() - self.gutter * 3) // 2
        p120_width_px = border_rect.width() - p130_width_px - self.gutter * 3
        p130_height_px = int(round(border_rect.height() / 9.4)) - (self.gutter * 2)
        p120_height_px = int(round(border_rect.height() / 16.1)) - (self.gutter * 2)

        self.pallet_rects.append(QRect(initial_x,
                                       initial_y,
                                       p130_width_px,
                                       p130_height_px))

        self.pallet_rects.append(QRect(initial_x + p130_width_px + self.gutter,
                                       initial_y,
                                       p120_width_px,
                                       p120_height_px))

        self.pallet_rects.append(QRect(initial_x + p130_width_px + self.gutter,
                                       initial_y + p120_height_px + self.gutter,
                                       p120_width_px,
                                       p120_height_px))

        self.brush_offset += (p120_height_px * 2) + (self.gutter * 2)

    def generate_130_130(self, standard_pallet_width, border_rect):
        initial_x = border_rect.left() + self.gutter
        initial_y = border_rect.top() + self.gutter + self.brush_offset
        pallet_width_px = (border_rect.width() - self.gutter * 3) // 2
        pallet_height_px = int(round(border_rect.height() / 9.4)) - (self.gutter * 2)

        self.pallet_rects.append(QRect(initial_x,
                                       initial_y,
                                       pallet_width_px,
                                       pallet_height_px))

        self.pallet_rects.append(QRect(initial_x + pallet_width_px + self.gutter,
                                       initial_y,
                                       pallet_width_px,
                                       pallet_height_px))

        self.brush_offset += pallet_height_px + self.gutter

    def generate_17080_60(self, standard_pallet_width, border_rect):
        initial_x = border_rect.left() + self.gutter
        initial_y = border_rect.top() + self.gutter + self.brush_offset
        p17080_width_px = int(round((border_rect.width() - self.gutter * 3) / 1.35))
        p60_width_px = border_rect.width() - p17080_width_px - self.gutter * 3
        pallet_height_px = int(round(border_rect.height() / 16.3)) - (self.gutter * 2)

        self.pallet_rects.append(QRect(initial_x,
                                       initial_y,
                                       p17080_width_px,
                                       pallet_height_px))

        self.pallet_rects.append(QRect(initial_x + p17080_width_px + self.gutter,
                                       initial_y,
                                       p60_width_px,
                                       pallet_height_px))

        self.brush_offset += pallet_height_px + self.gutter

    def generate_17090_60(self, standard_pallet_width, border_rect):
        initial_x = border_rect.left() + self.gutter
        initial_y = border_rect.top() + self.gutter + self.brush_offset
        p17090_width_px = int(round((border_rect.width() - self.gutter * 3) / 1.35))
        p60_width_px = border_rect.width() - p17090_width_px - self.gutter * 3
        p17090_height_px = int(round(border_rect.height() / 14.5)) - (self.gutter * 2)
        p60_height_px = int(round(border_rect.height() / 16.3)) - (self.gutter * 2)

        self.pallet_rects.append(QRect(initial_x,
                                       initial_y,
                                       p17090_width_px,
                                       p17090_height_px))

        self.pallet_rects.append(QRect(initial_x + p17090_width_px + self.gutter,
                                       initial_y,
                                       p60_width_px,
                                       p60_height_px))

        self.brush_offset += p17090_height_px + self.gutter

    def generate_23090(self, standard_pallet_width, border_rect):
        initial_x = border_rect.left() + self.gutter
        initial_y = border_rect.top() + self.gutter + self.brush_offset
        pallet_width_px = border_rect.width() - self.gutter * 2
        pallet_height_px = int(round(border_rect.height() / 14.5)) - (self.gutter * 2)

        self.pallet_rects.append(QRect(initial_x,
                                       initial_y,
                                       pallet_width_px,
                                       pallet_height_px))

        self.brush_offset += pallet_height_px + self.gutter

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

        standard_pallet_width = self.update_standard_pallet_width()
        border_rect = self.update_border_rect(standard_pallet_width)

        self.draw_border_rect(painter, border_rect)

        self.pallet_rects = []
        self.brush_offset = 0
        self.generate_17090_17090_130_130_130(standard_pallet_width, border_rect)
        self.generate_120_120_60_60(standard_pallet_width, border_rect)
        self.generate_17080_17080_120_60(standard_pallet_width, border_rect)
        self.generate_17080_120_120_60_60(standard_pallet_width, border_rect)
        self.generate_120_60_60_60_60(standard_pallet_width, border_rect)
        self.generate_17080_60(standard_pallet_width, border_rect)
        self.generate_17090_145_145(standard_pallet_width, border_rect)
        self.generate_130_120_120(standard_pallet_width, border_rect)

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
