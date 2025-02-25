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
        # A list will be created with all possible permutations of these arrangements, with the length of n!,
        # where n is the number of elements of permutable_arrangements. 8 elements is optimal, 9 is the practical
        # maximum.
        self.permutable_arrangements = (
            (17090, 145, 145),
            (17090, 17090, 130, 130, 130),
            (17080, 17080, 120, 60),
            (17080, 120, 120, 60, 60),
            (120, 120),
            (120, 120, 60, 60),
            (17090, 60),
            (130, 120, 120)
        )
        # These will be appended to every permutation of permutable_arrangements in a fixed order.
        self.non_permutable_arrangements = (
            (17080, 17080, 17080),
            (120, 60, 60, 60, 60),
            (17080, 60),
            (145, 145, 145),
            (130, 130),
            (120114, 120114),
            (120104, 120104),
            (60, 60, 60)
        )
        # Current calculation progress, in %
        self.progress: int = 0

    # Checks if a given arrangement can be formed within the current pool of pallets; returns True if yes
    def arrangement_is_possible(self, checked_arrangement: tuple) -> bool:
        # Makes a working copy of the pallet list
        all_items: list = self.pallet_list[:]
        for item in checked_arrangement:
            if item in all_items:
                # Removes pallet from the working pallet list copy, so it can't be used twice
                all_items.remove(item)
            else:
                return False
        return True
