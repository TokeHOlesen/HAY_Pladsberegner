import sys
from load_calculator_class import LoadCalculator
from PyQt6.QtWidgets import QApplication, QMainWindow
from truck_view_widget_class import TruckView
from pdf_generator import generate_pdf


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HAY Pladsberegner")

        load_calculator = LoadCalculator()
        load_calculator.load_pallets(*[2, 33, 45, 17, 7, 6, 2])
        load_calculator.calculate_load()
        trucks = load_calculator.trucks
        loose_pallets = load_calculator.loose_pallets

        print(f"{load_calculator.number_of_pallets} pallets, {load_calculator.number_of_trucks} trucks.")

        for i, truck in enumerate(trucks):
            print(f"\nTruck {i + 1} ({truck.number_of_pallets} pallets, {truck.total_ldm / 100} ldm):")
            for content_line in truck.description_lines:
                print(content_line)

        print(f"\nLoose pallets ({load_calculator.number_of_loose_pallets} pallets, {load_calculator.ldm_of_loose_pallets / 100} ldm):")
        for pallet in loose_pallets:
            print(pallet)

        truck_view_widget = TruckView()
        truck_view_widget.load_truck(trucks[0])
        generate_pdf(trucks, loose_pallets, "KID0029876", "test_pdf.pdf")
        self.setCentralWidget(truck_view_widget)
        self.resize(200, 600)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
