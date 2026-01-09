from dataclasses import dataclass
from grouping_processor_class import GroupingProcessor
from truck_processor_class import TruckProcessor
from truck_class import Truck


@dataclass
class LoadCalculationResult:
    """A data class containing all the relevant calculation results."""
    trucks: list[Truck]
    loose_pallets: list[int]
    number_of_pallets: int
    number_of_trucks: int
    number_of_loose_pallets: int
    loose_pallets_ldm: int


def calculate_load(pallets: list[int]) -> LoadCalculationResult:
    """
    Takes a list of 7 ints as an argument, corresponding to the number of the 7 pallet types.
    Returns a LoadCalculationResult object, containing all the relevant results.
    """
    grouping_processor = GroupingProcessor()
    truck_processor = TruckProcessor()
    grouping_processor.load_pallets(*pallets)
    grouping_processor.process_groupings()
    chosen_grouping = grouping_processor.best_grouping
    truck_processor.load_grouping(chosen_grouping)
    truck_processor.process_trucks()
    return LoadCalculationResult(trucks=truck_processor.trucks,
                                 loose_pallets=truck_processor.loose_pallets,
                                 number_of_pallets=grouping_processor.number_of_pallets,
                                 number_of_trucks=truck_processor.number_of_trucks,
                                 number_of_loose_pallets=truck_processor.number_of_loose_pallets,
                                 loose_pallets_ldm=truck_processor.ldm_of_loose_pallets)
