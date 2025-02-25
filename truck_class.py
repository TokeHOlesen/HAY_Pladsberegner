from arrangement_collection_abstract_class import ArrangementCollection
from constants import ARRANGEMENT_LDM_VALUES, ARRANGEMENT_ORDER


class Truck(ArrangementCollection):
    """Represents one truck, containing arrangements (tuples) and loose pallets (integers)."""
    def __init__(self) -> None:
        super().__init__()

    @property
    def ldm_ascending_order(self) -> list:
        """Returns a list of the ldm values for all arrangements on this truck, in ascending order."""
        ldm_ascending_list = []
        for arrangement in self.arrangements:
            ldm_ascending_list.append(ARRANGEMENT_LDM_VALUES[arrangement])
        ldm_ascending_list.sort()
        return ldm_ascending_list

    @property
    def ldm_descending_order(self) -> list:
        """Returns a list of the ldm values for all arrangements on this truck, in descending order."""
        return self.ldm_ascending_order[::-1]

    def sort_arrangements(self):
        """Sorts arrangements on this truck according to the order defined in ARRANGEMENT_ORDER."""
        sorted_arrangements = []
        for arrangement in ARRANGEMENT_ORDER:
            while arrangement in self.arrangements:
                sorted_arrangements.append(arrangement)
                self.arrangements.remove(arrangement)
        self.arrangements = sorted_arrangements
