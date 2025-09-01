from itertools import permutations
from constants import PERMUTABLE_ARRANGEMENTS, NON_PERMUTABLE_ARRANGEMENTS, ARRANGEMENT_LDM_VALUES
from grouping_class import Grouping


class GroupingProcessor:
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
        # The grouping to be used as the final solution
        self.best_grouping: Grouping = Grouping()

    # Generates all possible groupings and appends them to self.groupings[]
    def calculate_groupings(self) -> None:
        """
        Calculates all possible permutations of items in PERMUTABLE_ARRANGEMENTS.
        Appends arrangements from NON_PERMUTABLE_ARRANGEMENTS to each permutation.
        Later, calculates all possible groupings.
        """
        all_permutations: tuple = tuple(
            permutation + NON_PERMUTABLE_ARRANGEMENTS
            for permutation in permutations(PERMUTABLE_ARRANGEMENTS, len(PERMUTABLE_ARRANGEMENTS))
        )

        no_of_permutations = len(all_permutations)

        for i, permutation in enumerate(all_permutations):
            # Updates the progress bar value
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
            for pallet in pallet_list_copy:
                new_grouping.add_pallet(pallet)
            if new_grouping.is_perfect:
                self.contains_perfect = True
                # TODO: stop as soon as a perfect grouping is found
            self.groupings.append(new_grouping)

    def prune_groupings(self):
        """
        If a perfect grouping exists, removes all imperfect groupings.
        Otherwise, keeps only the arrangements with the smallest loose pallet and arrangement ldm.
        """
        # TODO: stop as soon as one perfect solution is found
        # Removes all imperfect groupings if at least one perfect grouping exist
        if self.contains_perfect:
            self.groupings[:] = [grouping for grouping in self.groupings if grouping.is_perfect]
            return
        # Finds the lowest loose pallet ldm among the groupings and removes all groupings where it's higher
        lowest_loose_ldm = self.get_lowest_loose_ldm()
        self.groupings[:] = [grouping for grouping in self.groupings if grouping.loose_pallets_ldm == lowest_loose_ldm]
        # Finds the lowest arrangement ldm among the groupings and removes all groupings where it's higher
        lowest_arr_ldm = self.get_lowest_arrangement_ldm()
        self.groupings[:] = [grouping for grouping in self.groupings if grouping.arrangements_ldm == lowest_arr_ldm]

    def set_best_grouping(self) -> None:
        """
        Sets self.best_grouping to self.groupings[0].
        If used after pruning, the groupings that are left are equivalent, so the first one is used.
        """
        self.best_grouping = self.groupings[0]

    def sort_best_grouping(self) -> None:
        """Sorts the arrangements within self.best_grouping by size, in descending order."""
        self.best_grouping.arrangements = sorted(self.best_grouping.arrangements,
                                                 key=lambda x: ARRANGEMENT_LDM_VALUES[x],
                                                 reverse=True)

    def get_lowest_loose_ldm(self) -> int:
        """Checks the total ldm value of loose pallets in every grouping and returns the lowest one."""
        lowest_ldm = 65536
        for grouping in self.groupings:
            lowest_ldm = grouping.loose_pallets_ldm if grouping.loose_pallets_ldm < lowest_ldm else lowest_ldm
        return lowest_ldm

    def get_lowest_arrangement_ldm(self) -> int:
        """Checks the total ldm value of arrangements in every grouping and returns the lowest one."""
        lowest_ldm = 65536
        for grouping in self.groupings:
            lowest_ldm = grouping.arrangements_ldm if grouping.arrangements_ldm < lowest_ldm else lowest_ldm
        return lowest_ldm

    @staticmethod
    def arrangement_is_possible(checked_arrangement: tuple[int, ...], pallet_list: list[int]) -> bool:
        """Checks if a given arrangement can be formed within the current pool of pallets; returns True if yes."""
        temp_pallet_list = pallet_list.copy()
        for pallet in checked_arrangement:
            if pallet in temp_pallet_list:
                # Removes pallet from the working pallet list copy, so it can't be used twice
                temp_pallet_list.remove(pallet)
            else:
                return False
        return True

    def process_groupings(self) -> None:
        """Forms groupings, prunes them, chooses the best one and sorts the arrangements on it."""
        self.calculate_groupings()
        self.prune_groupings()
        self.set_best_grouping()
        self.sort_best_grouping()
