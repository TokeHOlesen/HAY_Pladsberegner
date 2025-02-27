from constants import DEFAULT_MAX_TRUCK_LDM, PALLET_LDM_VALUES
from truck_class import Truck


class AllTrucks:
    """Represents all the trucks necessary to transport all the pallets."""
    def __init__(self, max_ldm=DEFAULT_MAX_TRUCK_LDM) -> None:
        # Holds objects of the Truck class, containing all pallets, sorted into arrangements
        self.trucks: list[Truck] = []
        # A list of  loose leftover pallets, not assigned to any truck
        self.loose_pallets: list[int] = []
        # How many load meters may at most be loaded on this truck, * 100
        self.max_ldm: int = max_ldm

    @property
    def number_of_trucks(self) -> int:
        """Returns the total number of trucks."""
        return len(self.trucks)

    @property
    def number_of_loose_120(self) -> int:
        return sum(1 for 120 in self.loose_pallets)

    def distribute_120_pallets(self):
        """
        If there are any 120 pallets in the loose pallet pool, distributes them among the trucks.
        To make sure that arrangements can be formed, adds at least two pallets per truck, more if there's room.
        """
        for truck in self.trucks:
            # Checks if there's room for at least two 120 pallets
            if self.max_ldm >= truck.total_ldm + (PALLET_LDM_VALUES[120] * 2) and self.number_of_loose_120 >= 2:
                # Transfers 120 pallets from the general loose pallet pool to the truck's loose pallet pool,
                # until there's no room or pallets left
                while truck.total_ldm + PALLET_LDM_VALUES[120] <= self.max_ldm and self.number_of_loose_120 >= 1:
                    truck.add_pallet(120)
                    self.loose_pallets.remove(120)

