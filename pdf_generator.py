from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtGui import QPainter, QPen, QColor, QPageSize, QFont
from truck_view_widget_class import TruckView
from math import ceil

MARGIN_LEFT = 800
MARGIN_TOP = 1200
SPACE_BETWEEN_TRUCKS = 500

FONT_MAIN_HEADER = QFont("Calibri", 24)
FONT_TRUCK_HEADER = QFont("Calibri", 16)
FONT_TRUCK_CONTENTS = QFont("Calibri", 12)


def draw_main_header(painter, reference_name, page_number, total_pages):
    painter.save()
    painter.setFont(FONT_MAIN_HEADER)
    painter.drawText(MARGIN_LEFT, MARGIN_TOP - 300, f"Læsseplan: {reference_name} (side {page_number}/{total_pages})")
    painter.restore()


def draw_truck_contents(truck, painter, page_rect, truck_number):
    truck_width = int(page_rect.width() * 0.4)
    truck_height = int(page_rect.height() * 0.4)
    truck_view = TruckView()
    truck_view.load_truck(truck)

    painter.save()
    painter.translate(MARGIN_LEFT, MARGIN_TOP)
    painter.setFont(FONT_TRUCK_HEADER)
    painter.setPen(QPen(QColor("black"), 10))
    painter.drawLine(0, 0, int(page_rect.width() - MARGIN_LEFT * 2), 0)
    painter.translate(0, 200)
    painter.drawText(MARGIN_LEFT * 2, 200, f"Bil {truck_number}:")
    painter.setFont(FONT_TRUCK_CONTENTS)
    start = 680
    distance = 300
    for i, description_line in enumerate(truck.description_lines):
        painter.drawText(MARGIN_LEFT * 2, start + distance * i, description_line)
    truck_view.draw_truck(painter, truck_width, truck_height, to_print=True)
    painter.restore()


def generate_pdf(trucks, loose_pallets, reference_name, filename: str):
    printer = QPrinter(QPrinter.PrinterMode.HighResolution)
    printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
    printer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
    printer.setOutputFileName(filename)
    page_rect = printer.pageRect(QPrinter.Unit.DevicePixel)
    painter = QPainter()
    painter.begin(printer)

    painter.save()
    total_pages = ceil((len(trucks) + int(loose_pallets != [])) / 2)
    page_number = 0
    for i, truck in enumerate(trucks):
        if i % 2 == 0:
            page_number += 1
            if page_number > 1:
                printer.newPage()
                painter.resetTransform()
            draw_main_header(painter, reference_name, page_number, total_pages)
            draw_truck_contents(trucks[i], painter, page_rect, i + 1)
        else:
            painter.translate(0, int(page_rect.height() * 0.4) + SPACE_BETWEEN_TRUCKS)
            draw_truck_contents(trucks[i], painter, page_rect, i + 1)
    painter.restore()

    painter.end()
