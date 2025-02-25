from constants import PERMUTABLE_ARRANGEMENTS, NON_PERMUTABLE_ARRANGEMENTS


class GroupingCalculator:
    def __init__(self,
                 no_of_60: int = 0,
                 no_of_120: int = 0,
                 no_of_145: int = 0,
                 no_of_130: int = 0,
                 no_of_17080: int = 0,
                 no_of_17090: int = 0,
                 no_of_120104: int = 0,
                 no_of_120114: int = 0,
                 ):
        # Contains an element for each pallet, represented by an integer (fx. [120, 120, 17090])
        self.pallet_list = []
        # Populates the pallet list
        for count, value in [
            (no_of_60, 60),
            (no_of_120, 120),
            (no_of_145, 145),
            (no_of_130, 130),
            (no_of_17080, 17080),
            (no_of_17090, 17090),
            (no_of_120104, 120104),
            (no_of_120114, 120114)
        ]:
            self.pallet_list.extend([value] * count)
        # A list holding all the calculated Grouping objects
        self.groupings = []
        # Current calculation progress, in %
        self.progress: int = 0

    # Checks if a given arrangement can be formed within the current pool of pallets; returns True if yes
    def arrangement_is_possible(self, checked_arrangement: tuple) -> bool:
        # Makes a working copy of the pallet list
        all_pallets: list = self.pallet_list[:]
        for pallet in checked_arrangement:
            if pallet in all_pallets:
                # Removes pallet from the working pallet list copy, so it can't be used twice
                all_pallets.remove(pallet)
            else:
                return False
        return True
