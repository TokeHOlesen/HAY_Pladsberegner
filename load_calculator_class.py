from grouping_processor_class import GroupingProcessor
from truck_processor_class import TruckProcessor


class LoadCalculator:
    def __init__(self):
        self.grouping_processor = GroupingProcessor()
        self.truck_processor = TruckProcessor()
        self.result = []
        self.loose_pallets = []

    def process(self):
        self.grouping_processor.load_pallets(no_145=12, no_17090=4, no_120=40, no_130=0, no_60=0, no_17080=0)
        self.grouping_processor.process_groupings()
        chosen_grouping = self.grouping_processor.best_grouping
        self.truck_processor.load_grouping(chosen_grouping)
        self.truck_processor.process_trucks()
        self.result = self.truck_processor.trucks
        self.loose_pallets = self.truck_processor.loose_pallets
