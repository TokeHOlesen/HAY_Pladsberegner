from grouping_processor_class import GroupingProcessor
from truck_processor_class import TruckProcessor


class LoadCalculator:
    """A wrapper for GroupingCalculator and TruckCalculator to consolidate data in/out into a single point."""
    def __init__(self):
        self.grouping_processor = GroupingProcessor()
        self.truck_processor = TruckProcessor()
        self.trucks = []
        self.loose_pallets = []

    def process(self):
        self.grouping_processor.load_pallets(no_60=0, no_120=100, no_145=50, no_130=20, no_17080=0, no_17090=15)
        self.grouping_processor.process_groupings()
        chosen_grouping = self.grouping_processor.best_grouping
        self.truck_processor.load_grouping(chosen_grouping)
        self.truck_processor.process_trucks()
        self.trucks = self.truck_processor.trucks
        self.loose_pallets = self.truck_processor.loose_pallets
