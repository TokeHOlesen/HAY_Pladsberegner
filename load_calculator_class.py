from grouping_processor_class import GroupingProcessor
from truck_processor_class import TruckProcessor


class LoadCalculator:
    """A wrapper/interface for GroupingCalculator and TruckCalculator to consolidate data in/out into a single point."""
    def __init__(self):
        self.grouping_processor = GroupingProcessor()
        self.truck_processor = TruckProcessor()
        self.trucks = []
        self.loose_pallets = []
        self.load_pallets = self.grouping_processor.load_pallets

    @property
    def number_of_pallets(self) -> int:
        return self.grouping_processor.number_of_pallets

    @property
    def number_of_trucks(self) -> int:
        return self.truck_processor.number_of_trucks

    @property
    def number_of_loose_pallets(self) -> int:
        return self.truck_processor.number_of_loose_pallets

    @property
    def ldm_of_loose_pallets(self) -> int:
        return self.truck_processor.ldm_of_loose_pallets

    def calculate_load(self):
        self.grouping_processor.process_groupings()
        chosen_grouping = self.grouping_processor.best_grouping
        self.truck_processor.load_grouping(chosen_grouping)
        self.truck_processor.process_trucks()
        self.trucks = self.truck_processor.trucks
        self.loose_pallets = self.truck_processor.loose_pallets
