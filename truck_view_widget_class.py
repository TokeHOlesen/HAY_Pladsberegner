import arrangement_rect_generator as arr_rect_gen
from constants import DEFAULT_MAX_TRUCK_LDM
from truck_class import Truck
from PyQt6.QtCore import QRect
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtWidgets import QWidget

# Relative dimensions of the truck; 13.6 x 2.4m is the standard trailer size
RELATIVE_HEIGHT = 13.6
RELATIVE_WIDTH = 2.4


class TruckView(QWidget):
    """A widget containing a view representing the contents of one truck."""
    def __init__(self):
        super().__init__()
        self.setMinimumSize(150, 400)
        self.aspect = RELATIVE_HEIGHT / RELATIVE_WIDTH
        # By how much to offset the drawing of the next arrangement
        self.brush_offset = 0
        # Empty space around pallets
        self.gutter = 0
        # Holds PalletRect objects, each one representing a pallet
        self.pallet_rects = []
        # How many pixels to represent the width of a standard pallet (80 cm)
        self.standard_pallet_width = 0
        self.border_rect = None
        # Holds pixel values for every pallet type; populated by calling update_pallet_rect_dimensions()
        self.pallet_rect_dimensions = {}
        # A Truck object providing the data to be drawn
        self.truck: Truck = Truck(DEFAULT_MAX_TRUCK_LDM)

    def load_truck(self, truck):
        self.truck = truck

    def update_standard_pallet_width(self):
        """
        Calculates how many pixels correspond to a standard pallet width (80cm).
        This number forms the basis for calculating the size, in pixels, of the border rectangle and, in turn,
        the sizes of all other pallets.
        """
        pallet_width = self.width() - 4 * self.gutter // 3
        while pallet_width > 0:
            truck_rect_width = 3 * pallet_width + 4 * self.gutter
            truck_rect_height = int(round(truck_rect_width * self.aspect))
            if truck_rect_width <= self.width() and truck_rect_height <= self.height():
                break
            pallet_width -= 1
        self.standard_pallet_width = pallet_width

    def update_border_rect(self):
        """
        Calculates the size of the border rectangle by using the pixel value of the width of a standard pallet
        as the starting point. This ensures that the pallet view remains consistent and resolution independent.
        """
        width = 3 * self.standard_pallet_width + 4 * self.gutter
        height = int(round(width * self.aspect))
        self.border_rect = QRect(0, 0, width, height)

    def update_pallet_rect_dimensions(self):
        """
        Calculates the pixel sizes of all pallets, in all relevant orientations.
        Because of the limited number of pixels on most displays and the need to keep the sizes constant relative to
        each other, the pixel sizes don't correspond exactly to real life dimensions.
        The vertical sizes are calculated by dividing the truck height by the approximate maximum number of times the
        relevant pallet in a given orientation fits inside a truck, then subtracting the pixels used for gutter (blank)
        space between pallets.
        Because the numbers are approximate, they may differ between arrangements even if the pallets used are the same.
        Orientation is described by a prefix: v- for vertical, h- for horizontal.
        """
        # Standard width is the width of an EUR pallet in vertical orientation; 80 cm.
        # Relevant for 60, 120, 145 and 17080 type pallets.
        self.pallet_rect_dimensions["standard_width"] = self.standard_pallet_width
        self.pallet_rect_dimensions["v-60-height"] = self.border_rect.height() // 21 - (self.gutter * 2)
        self.pallet_rect_dimensions["h-60-height"] = int(round(self.border_rect.height() / 16.3)) - (self.gutter * 2)
        self.pallet_rect_dimensions["v-120-height"] = self.border_rect.height() // 11 - (self.gutter * 2)
        self.pallet_rect_dimensions["h-120-height"] = int(round(self.border_rect.height() / 16.1)) - (self.gutter * 2)
        self.pallet_rect_dimensions["h-120-width"] = (self.border_rect.width() - self.gutter * 3) // 2
        self.pallet_rect_dimensions["v-130-height"] = int(round(self.border_rect.height() / 9.4)) - (self.gutter * 2)
        self.pallet_rect_dimensions["v-130-width"] = (self.border_rect.width() - self.gutter * 3) // 2
        self.pallet_rect_dimensions["v-145-height"] = self.border_rect.height() // 9 - (self.gutter * 2)
        self.pallet_rect_dimensions["h-145-height"] = self.border_rect.height() // 15 - (self.gutter * 2)
        self.pallet_rect_dimensions["v-17080-height"] = int(round(self.border_rect.height() / 7.45)) - (self.gutter * 2)
        self.pallet_rect_dimensions["h-17080-height"] = int(round(self.border_rect.height() / 16.3)) - (self.gutter * 2)
        self.pallet_rect_dimensions["h-17080-width"] = int(round((self.border_rect.width() - self.gutter * 3) / 1.35))
        self.pallet_rect_dimensions["v-17090-height"] = int(round(self.border_rect.height() / 7.45)) - (self.gutter * 2)
        self.pallet_rect_dimensions["v-17090-width"] = int(round((self.border_rect.width() - self.gutter * 2) / 2.7))
        self.pallet_rect_dimensions["h-17090-height"] = int(round(self.border_rect.height() / 14.5)) - (self.gutter * 2)
        self.pallet_rect_dimensions["h-17090-width"] = int(round((self.border_rect.width() - self.gutter * 3) / 1.35))
        self.pallet_rect_dimensions["h-23090-height"] = int(round(self.border_rect.height() / 14.5)) - (self.gutter * 2)
        self.pallet_rect_dimensions["h-23090-width"] = self.border_rect.width() - self.gutter * 2

    def generate_arrangement(self, arrangement):
        """
        Takes an arrangement tuple (for example, (120, 120, 120) as an argument and generates a list of PalletRect
        objects, each object corresponding to one pallet. These objects are then appended to self.pallet_rects.
        self.brush_offset, which keeps track of where the next arrangement will be drawn, gets updated."""
        x = self.border_rect.left() + self.gutter
        y = self.border_rect.top() + self.gutter + self.brush_offset
        generated_pallet_rects, brush_offset = arr_rect_gen.generate[arrangement](x,
                                                                                  y,
                                                                                  self.border_rect,
                                                                                  self.gutter,
                                                                                  self.pallet_rect_dimensions)

        self.pallet_rects.extend(generated_pallet_rects)
        self.brush_offset += brush_offset

    def draw_border_rect(self, painter, border_thickness):
        """Draws the border rectangle."""
        painter.fillRect(self.border_rect, QColor("white"))
        painter.setPen(QPen(QColor("black"), border_thickness))
        painter.drawRect(self.border_rect)

    def draw_arrangements(self, painter, border_thickness):
        """Draws all the pallets (PalletRect objects) in self.pallet_rects."""
        for pallet in self.pallet_rects:
            painter.fillRect(pallet, pallet.color)
            painter.setPen(QPen(QColor("black"), border_thickness))
            painter.drawRect(pallet)

    def draw_truck(self, painter, width, height, to_print=False):
        """
        Updates pixel sizes, generates PalletRect objects (to self.pallet_rects[]) and draws them using a QPainter
        object. Can be used to draw both to screen and to a printer.
        If the to_print parameter is True, the border will be drawn thicker, to appear properly on the printed page.
        """
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        self.resize(width, height)
        self.gutter = height // 200

        self.update_standard_pallet_width()
        self.update_border_rect()
        self.update_pallet_rect_dimensions()

        self.pallet_rects = []
        self.brush_offset = 0
        for arrangement in self.truck.arrangements:
            self.generate_arrangement(arrangement)

        border_thickness = 10 if to_print else 1
        self.draw_border_rect(painter, border_thickness)
        self.draw_arrangements(painter, border_thickness)

    def paintEvent(self, _):
        """
        Instantiates a QPainter object and calls the draw_truck() function, which draws the arrengements inside the
        widget.
        """
        painter = QPainter(self)
        self.draw_truck(painter, self.width(), self.height())
        painter.end()



