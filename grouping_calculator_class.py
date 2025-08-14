from itertools import permutations
from constants import PERMUTABLE_ARRANGEMENTS, NON_PERMUTABLE_ARRANGEMENTS
from grouping_class import Grouping


class GroupingCalculator:
    """
    Accepts the total number of pallets at init and calculates all possible groupings.
    Use self.progress for current progress during calculation.
    """
    def __init__(self,
                 no_of_60: int = 0,
                 no_of_120: int = 0,
                 no_of_145: int = 0,
                 no_of_130: int = 0,
                 no_of_17080: int = 0,
                 no_of_17090: int = 0,
                 no_of_23090: int = 0
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
            (no_of_23090, 23090)
        ]:
            self.pallet_list.extend([value] * count)
        # A list holding all the calculated Grouping objects
        self.groupings = []
        # True if self.groupings contains at least one perfect grouping
        self.contains_perfect = False
        # Current calculation progress, in %
        self.progress: int = 0

    # Generates all possible groupings and appends them to self.groupings[]
    def calculate_groupings(self):
        """
        Calculates all possible permutations of items in permutable_arrangements.
        Appends arrangements from NON_PERMUTABLE_ARRANGEMENTS to each permutation.
        Later, calculates all possible groupings.
        """
        all_permutations = tuple(
            perm + NON_PERMUTABLE_ARRANGEMENTS
            for perm in permutations(PERMUTABLE_ARRANGEMENTS, len(PERMUTABLE_ARRANGEMENTS))
        )

        no_of_permutations = len(all_permutations)

        for i, permutation in enumerate(all_permutations):
            # Updates the progress bar
            self.progress: int = (i + 1) * 100 // no_of_permutations
            # Creates a new Grouping object
            new_grouping: Grouping = Grouping()
            # Makes a working copy of the pallet list
            pallet_list_copy: list[int] = self.pallet_list.copy()
            # Checks each arrangement in this permutation
            # If the arrangement can be formed, adds it to self.groupings and removes pallets from the working copy
            for arrangement in permutation:
                while self.arrangement_is_possible(arrangement, pallet_list_copy):
                    new_grouping.add_arrangement(arrangement)
                    for pallet in arrangement:
                        pallet_list_copy.remove(pallet)
            # If there are any remaining loose pallets, adds them to the grouping's loose pallets list
            if len(pallet_list_copy) == 0:
                self.contains_perfect = True
                # TODO: stop as soon as a perfect grouping is found
            else:
                for pallet in pallet_list_copy:
                    new_grouping.add_pallet(pallet)
            self.groupings.append(new_grouping)

    def prune_groupings(self):
        """Removes all imperfect groupings. Call only if at least one perfect grouping is known to exist."""
        # TODO: Temporary solution. Eventually it might make sense to stop as soon as one perfect solution is found
        if self.contains_perfect:
            self.groupings[:] = [grouping for grouping in self.groupings if grouping.is_perfect]

    @staticmethod
    def arrangement_is_possible(checked_arrangement: tuple[int, ...], pallet_list: list[int]) -> bool:
        """
        Checks if a given arrangement can be formed within the current pool of pallets; returns True if yes.
        """
        temp_pallet_list = pallet_list.copy()
        for pallet in checked_arrangement:
            if pallet in temp_pallet_list:
                # Removes pallet from the working pallet list copy, so it can't be used twice
                temp_pallet_list.remove(pallet)
            else:
                return False
        return True
