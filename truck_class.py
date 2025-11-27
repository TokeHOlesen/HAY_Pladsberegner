from collections import Counter
from arrangement_collection_abstract_class import ArrangementCollection
from constants import ARRANGEMENT_ORDER, ARRANGEMENT_FORMATTED_OUTPUT, ARRANGEMENT_LDM_VALUES, PALLET_FORMATTED_OUTPUT


class Truck(ArrangementCollection):
    """Represents one truck, containing arrangements (tuples) and loose pallets (integers)."""
    def __init__(self, max_ldm: int) -> None:
        super().__init__()
        self.max_ldm: int = max_ldm

    @property
    def number_of_pallets(self) -> int:
        pallet_sum: int = 0
        for arrangement in self.arrangements:
            for pallet in arrangement:
                pallet_sum += 1
        return pallet_sum

    @property
    def remaining_ldm(self) -> int:
        """Returns how much ldm is free on this truck."""
        return self.max_ldm - self.total_ldm

    @property
    def number_of_loose_120(self) -> int:
        """Returns the number of 120 pallets in 'self.loose_pallets'."""
        return len(self.loose_pallets)

    @property
    def description_lines(self) -> list[str]:
        """Returns a list of strings, representing the contents of this truck."""
        description_lines: list[str] = []
        arrangement_count: Counter = Counter(self.arrangements)

        for arrangement in arrangement_count:
            count: int = arrangement_count[arrangement]
            description: str = ARRANGEMENT_FORMATTED_OUTPUT[arrangement]
            arrangement_ldm: float = round(ARRANGEMENT_LDM_VALUES[arrangement] / 100, 2)
            description_lines.append(f"{count} x {description} ({arrangement_ldm} ldm x {count})")

        return description_lines

    @property
    def pallet_count_lines(self) -> list[str]:
        """Returns a list of strings, representing the amount of each pallet type on this truck."""
        all_pallets: list[int] = []
        pallet_count_lines: list[str] = []
        for arrangement in self.arrangements:
            for pallet in arrangement:
                all_pallets.append(pallet)
        pallet_count = Counter(all_pallets)
        for pallet in PALLET_FORMATTED_OUTPUT:
            if pallet in pallet_count:
                pallet_count_lines.append(f"{PALLET_FORMATTED_OUTPUT[pallet]}: {pallet_count[pallet]} stk.")

        return pallet_count_lines

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
