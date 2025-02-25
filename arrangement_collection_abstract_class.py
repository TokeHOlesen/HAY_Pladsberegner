from sys import exit
from constants import ARRANGEMENT_LDM_VALUES, PALLET_LDM_VALUES


class ArrangementCollection:
    """An abstract base class for the Grouping and Truck classes."""
    def __init__(self) -> None:
        # A list of all arrangements in this grouping. Each arrangement is a tuple of integers
        self.arrangements = []
        # A list of all loose pallets in this grouping. Each pallet is represented by an integer
        self.loose_pallets = []

    @property
    def arrangements_ldm(self) -> int:
        """Returns the total ldm for all arrangements in this grouping."""
        ldm_sum: int = 0
        for checked_arrangement in self.arrangements:
            ldm_sum += ARRANGEMENT_LDM_VALUES[checked_arrangement]
        return ldm_sum

    @property
    def loose_pallets_ldm(self) -> int:
        """Returns the total ldm for all loose pallets in this grouping."""
        ldm_sum: int = 0
        for checked_pallet in self.loose_pallets:
            ldm_sum += PALLET_LDM_VALUES[checked_pallet]
        return ldm_sum

    @property
    def total_ldm(self) -> int:
        """Returns total ldm for this grouping (arrangements + loose pallets)"""
        return self.arrangements_ldm + self.loose_pallets_ldm

    def add_arrangement(self, arrangement: tuple) -> None:
        """Appends an arrangement to the "self.arrangements" list."""
        self.arrangements.append(arrangement)

    def remove_arrangement(self, arrangement: tuple) -> None:
        """Removes an arrangement from the "self.arrangements" list."""
        try:
            self.arrangements.remove(arrangement)
        except ValueError:
            exit(f"Error: this arrangement collection does not contain the arrangement '{arrangement}'.")

    def add_pallet(self, pallet: int) -> None:
        """Appends a pallet to the "self.loose_pallets" list."""
        self.loose_pallets.append(pallet)

    def remove_pallet(self, pallet: int) -> None:
        """Removes a pallet from the "self.loose_pallets" list."""
        try:
            self.loose_pallets.remove(pallet)
        except ValueError:
            exit(f"Error: this arrangement collection does not contain the loose pallet '{pallet}'.")
