from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtGui import QPainter, QPen, QColor, QPageSize, QFont, QFontMetrics
from truck_view_widget_class import TruckView
from math import ceil
from collections import Counter
from constants import PALLET_FORMATTED_OUTPUT

MARGIN_LEFT = 800
MARGIN_TOP = 1200
# Empty space between the two truck views on the page
SPACE_BETWEEN_TRUCKS = 500

FONT = "Calibri"
FONT_MAIN_HEADER = QFont(FONT, 24)
FONT_TRUCK_HEADER = QFont(FONT, 16)
FONT_TRUCK_CONTENTS = QFont(FONT, 12)
FONT_PALLET_COUNT = QFont(FONT, 10)

# Relative starting position for drawing the truck contents description (details about arrangements on truck)
DESCRIPTION_ORIGIN = 680
# Line spacing for the contents description
DESCRIPTION_LINE_SPACING = 300
# Size of the gap between different text sections
SECTION_GAP = 400
# Line spacing for the pallet count section
PALLET_COUNT_LINE_SPACING = 200


def draw_main_header(painter, reference_name, page_rect, page_number, total_pages) -> None:
    """Draws the main header with reference number and page numbering."""
    painter.save()
    painter.setFont(FONT_MAIN_HEADER)
    painter.drawText(MARGIN_LEFT, MARGIN_TOP - 300, f"Læsseplan: {reference_name}")
    page_numbering_text: str = f"{page_number}/{total_pages}"
    page_numbering_width = painter.fontMetrics().horizontalAdvance(page_numbering_text)
    painter.drawText(int(page_rect.width()) - MARGIN_LEFT - page_numbering_width, MARGIN_TOP - 300, page_numbering_text)
    painter.restore()


def draw_truck_contents(truck, painter, page_rect, truck_number) -> None:
    """Draws the TruckView for a given truck and the text describing the contents."""
    truck_width: int = int(page_rect.width() * 0.4)
    truck_height: int = int(page_rect.height() * 0.4)
    truck_view: TruckView = TruckView()
    truck_view.load_truck(truck)
    pallet_count_font_height: int = QFontMetrics(FONT_PALLET_COUNT).height()

    painter.save()

    # Draws a horizontal spacer line
    painter.translate(MARGIN_LEFT, MARGIN_TOP)
    painter.setPen(QPen(QColor("black"), 10))
    painter.drawLine(0, 0, int(page_rect.width() - MARGIN_LEFT * 2), 0)

    # Draws the header text
    painter.translate(0, 200)
    painter.setFont(FONT_TRUCK_HEADER)
    painter.drawText(MARGIN_LEFT * 2, 200, f"Bil {truck_number}:")

    # Draws the truck contents description
    painter.setFont(FONT_TRUCK_CONTENTS)
    for i, description_line in enumerate(truck.description_lines):
        painter.drawText(MARGIN_LEFT * 2, DESCRIPTION_ORIGIN + DESCRIPTION_LINE_SPACING * i, description_line)

    # Draws the pallet count
    pallet_count_origin: int = truck_height - (len(truck.pallet_count_lines) * pallet_count_font_height + (len(truck.pallet_count_lines) * PALLET_COUNT_LINE_SPACING) + SECTION_GAP)
    total_info_origin: int = pallet_count_origin + len(truck.pallet_count_lines) + SECTION_GAP
    painter.setFont(FONT_PALLET_COUNT)
    for i, pallet_count_line in enumerate(truck.pallet_count_lines):
        painter.drawText(MARGIN_LEFT * 2, pallet_count_origin + PALLET_COUNT_LINE_SPACING * i, pallet_count_line)
        total_info_origin += PALLET_COUNT_LINE_SPACING

    # Draws the text containing information about total number of pallets and ldm.
    painter.drawText(MARGIN_LEFT * 2, total_info_origin, f"{truck.number_of_pallets} paller i alt, {round((truck.total_ldm / 100), 2)} ldm.")

    # Draws the truck content rects
    truck_view.draw_truck(painter, truck_width, truck_height, to_print=True)

    painter.restore()


def draw_loose_pallets(loose_pallets, loose_pallets_ldm, painter, page_rect):
    truck_width: int = int(page_rect.width() * 0.4)
    truck_height: int = int(page_rect.height() * 0.4)
    truck_view: TruckView = TruckView()
    truck_view.load_loose_pallets(loose_pallets)
    pallet_count_font_height: int = QFontMetrics(FONT_PALLET_COUNT).height()

    painter.save()

    # Draws a horizontal spacer line
    painter.translate(MARGIN_LEFT, MARGIN_TOP)
    painter.setPen(QPen(QColor("black"), 10))
    painter.drawLine(0, 0, int(page_rect.width() - MARGIN_LEFT * 2), 0)

    painter.translate(0, 200)
    painter.setFont(FONT_TRUCK_HEADER)
    painter.drawText(MARGIN_LEFT * 2, 200, "Rester:")

    leftover_count: Counter = Counter(loose_pallets)

    painter.setFont(FONT_TRUCK_CONTENTS)
    for i, pallet_type in enumerate(leftover_count):
        painter.drawText(MARGIN_LEFT * 2, DESCRIPTION_ORIGIN + DESCRIPTION_LINE_SPACING * i, f"{leftover_count[pallet_type]} x {PALLET_FORMATTED_OUTPUT[pallet_type]}")

    truck_view.draw_loose_pallets(painter, truck_width, truck_height, to_print=True)

    painter.setFont(FONT_PALLET_COUNT)
    painter.drawText(MARGIN_LEFT * 2, truck_height - pallet_count_font_height, f"{len(loose_pallets)} restpaller i alt, ca. {round(loose_pallets_ldm / 100, 2)} ldm.")

    painter.restore()


def generate_pdf(trucks, loose_pallets, loose_pallets_ldm, reference_name, filename: str):
    """Generates a pdf file based on the passed data."""
    # Printer setup
    printer = QPrinter(QPrinter.PrinterMode.HighResolution)
    printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
    printer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
    printer.setOutputFileName(filename)
    page_rect = printer.pageRect(QPrinter.Unit.DevicePixel)
    painter = QPainter()
    painter.begin(printer)

    painter.save()

    total_entries: int = len(trucks) + int(loose_pallets != [])
    total_pages: int = ceil(total_entries / 2)
    page_number: int = 0

    # Since there are two trucks per page, adds a new page every other truck.
    # Prints a header on top of every new page.
    for i in range(total_entries):
        if i % 2 == 0:
            page_number += 1
            if page_number > 1:
                printer.newPage()
                painter.resetTransform()
            draw_main_header(painter, reference_name, page_rect, page_number, total_pages)
            if i == total_entries - 1 and loose_pallets != []:
                draw_loose_pallets(loose_pallets, loose_pallets_ldm, painter, page_rect)
            else:
                draw_truck_contents(trucks[i], painter, page_rect, i + 1)
        else:
            painter.translate(0, int(page_rect.height() * 0.4) + SPACE_BETWEEN_TRUCKS)
            if i == total_entries - 1 and loose_pallets != []:
                draw_loose_pallets(loose_pallets, loose_pallets_ldm, painter, page_rect)
            else:
                draw_truck_contents(trucks[i], painter, page_rect, i + 1)

    painter.restore()
    painter.end()
