from arrangement_collection_abstract_class import ArrangementCollection
from constants import ARRANGEMENT_ORDER


class Truck(ArrangementCollection):
    """Represents one truck, containing arrangements (tuples) and loose pallets (integers)."""
    def __init__(self, max_ldm: int) -> None:
        super().__init__()
        self.max_ldm: int = max_ldm

    @property
    def remaining_ldm(self) -> int:
        """Returns how much ldm is free on this truck."""
        return self.max_ldm - self.total_ldm

    @property
    def number_of_loose_120(self) -> int:
        """Returns the number of 120 pallets in 'self.loose_pallets'."""
        return len(self.loose_pallets)

    def form_120_arrangements(self) -> None:
        """Forms (120, 120, 120) and (120, 120) arrangements from the loose 120 pallet pool."""
        # Forms (120, 120) arrangements until the number left is divisible by 3
        while self.number_of_loose_120 >= 2 and self.number_of_loose_120 % 3 != 0:
            self.add_arrangement((120, 120))
            self.remove_pallet(120, count=2)
        # Forms (120, 120, 120) arrangements
        if self.number_of_loose_120 >= 3:
            self.add_arrangement((120, 120, 120), count=self.number_of_loose_120 // 3)
            self.remove_pallet(120, count=self.number_of_loose_120)

    def sort_arrangements(self) -> None:
        """Sorts arrangements on this truck according to the order defined in ARRANGEMENT_ORDER."""
        sorted_arrangements = []
        for arrangement in ARRANGEMENT_ORDER:
            while arrangement in self.arrangements:
                sorted_arrangements.append(arrangement)
                self.arrangements.remove(arrangement)
        self.arrangements = sorted_arrangements
