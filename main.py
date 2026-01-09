import sys
import constants
from load_calculator import calculate_load
from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QLineEdit, QLabel, QGridLayout
from PyQt6.QtCore import Qt
from truck_view_widget_class import TruckView
from pdf_generator import generate_pdf


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"HAY Pladsberegner {constants.VERSION}")
        self.setFixedSize(400, 668)

        calc_result = calculate_load([100, 100, 100, 100, 100, 100, 0])

        truck_view_widget = TruckView()
        loose_pallets_view_widget = TruckView()
        truck_view_widget.setFixedHeight(self.height() - 10)
        loose_pallets_view_widget.setFixedHeight(self.height() - 10)
        truck_view_widget.load_truck(calc_result.trucks[0])
        if calc_result.loose_pallets:
            loose_pallets_view_widget.load_loose_pallets(calc_result.loose_pallets)

        input_form_widget = QWidget()
        input_form_layout = QGridLayout(input_form_widget)
        input_form_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        input_form_layout.setVerticalSpacing(8)
        input_form_layout.setContentsMargins(0, 0, 10, 0)

        input_labels = [
            "60x80:",
            "120x80:",
            "145x80:",
            "130x115:",
            "170x80:",
            "170x90:",
            "220x90:"
        ]

        for row_index, label_text in enumerate(input_labels):
            label = QLabel(label_text)
            text_box = QLineEdit()
            text_box.setFixedWidth(50)
            input_form_layout.addWidget(label, row_index, 0, alignment=Qt.AlignmentFlag.AlignRight)
            input_form_layout.addWidget(text_box, row_index, 1)

        central_widget = QWidget()
        central_layout = QHBoxLayout(central_widget)

        central_layout.addWidget(input_form_widget)
        central_layout.addWidget(truck_view_widget)
        central_layout.addWidget(loose_pallets_view_widget)

        central_layout.setContentsMargins(10, 10, 10, 10)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

        generate_pdf(calc_result, "KID0012345", "test_pdf.pdf")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
