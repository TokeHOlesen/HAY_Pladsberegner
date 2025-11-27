from constants import DEFAULT_MAX_TRUCK_LDM, PALLET_LDM_VALUES, ARRANGEMENT_LDM_VALUES
from truck_class import Truck
from grouping_class import Grouping


class TruckProcessor:
    """
    Distributes the arrangements and loose pallets between trucks. A Grouping object must be passed to the constructor.
    """

    def __init__(self, max_ldm=DEFAULT_MAX_TRUCK_LDM) -> None:
        # Holds objects of the Truck class, containing all pallets, sorted into arrangements
        self.trucks: list[Truck] = []
        # A list of all arrangements to be distributed
        self.arrangements = []
        # A list of loose leftover pallets, not in arrangements
        self.loose_pallets: list[int] = []
        # How many load meters may at most be loaded on this truck, * 100
        self.max_ldm: int = max_ldm

    def load_grouping(self, grouping: Grouping) -> None:
        """Loads a grouping to be processed and resets the results of any previous calculations."""
        self.trucks: list[Truck] = []
        self.arrangements = grouping.arrangements
        self.loose_pallets = grouping.loose_pallets

    def add_truck(self) -> None:
        """Adds a new truck to self.trucks."""
        self.trucks.append(Truck(self.max_ldm))

    @property
    def number_of_trucks(self) -> int:
        """Returns the total number of trucks."""
        return len(self.trucks)

    @property
    def number_of_loose_120(self) -> int:
        """Returns the number of loose 120 pallets."""
        return self.loose_pallets.count(120)

    @property
    def number_of_loose_pallets(self) -> int:
        """Returns the number of all loose pallets."""
        return len(self.loose_pallets)

    @property
    def ldm_of_loose_pallets(self) -> int:
        """Returns the ldm value of remaining loose pallets."""
        return sum(PALLET_LDM_VALUES[pallet] for pallet in self.loose_pallets)

    @property
    def number_of_arrangements(self) -> int:
        """Returns the number of arrangements on this truck."""
        return len(self.arrangements)

    @property
    def last_truck(self) -> Truck:
        """Returns the last truck in self.trucks."""
        return self.trucks[-1]

    def distribute_arrangements(self) -> None:
        """
        Distributes arrangements between trucks, using the best-fit decreasing algorithm.
        If there is no room on any of the existing trucks, adds a new one and places the arrangement there.
        """
        for arrangement in sorted(self.arrangements,
                                  key=lambda x: ARRANGEMENT_LDM_VALUES[x],
                                  reverse=True):
            placed: bool = False
            # Sorts the trucks by free ldm, with the most full trucks first
            self.trucks.sort(key=lambda x: x.remaining_ldm)
            for truck in self.trucks:
                if truck.remaining_ldm >= ARRANGEMENT_LDM_VALUES[arrangement]:
                    truck.add_arrangement(arrangement)
                    placed = True
                    break
            if not placed:
                self.add_truck()
                self.last_truck.add_arrangement(arrangement)

    def distribute_120_pallets(self) -> None:
        """
        If there are any 120 pallets in the loose pallet pool, distributes them among the trucks.
        To make sure that arrangements can be formed, adds at least two pallets per truck, more if there's room.
        If there is not enough room on existing trucks for all the loose 120s, adds more trucks.
        """
        for truck in self.trucks:
            # Checks if there's room for at least two 120 pallets
            if self.max_ldm >= truck.total_ldm + (PALLET_LDM_VALUES[120] * 2) and self.number_of_loose_120 >= 2:
                # Transfers 120 pallets from the general loose pallet pool to the truck's loose pallet pool,
                # until there's no room or pallets left
                while (truck.total_ldm + PALLET_LDM_VALUES[120]) <= self.max_ldm and self.number_of_loose_120 >= 1:
                    truck.add_pallet(120)
                    self.loose_pallets.remove(120)
        # Add more trucks if all the 120 pallets can't fit on existing ones
        while self.number_of_loose_120 > 1:
            self.add_truck()
            number_to_add: int = min(33, self.number_of_loose_120)
            self.last_truck.add_pallet(120, number_to_add)
            for i in range(number_to_add):
                self.loose_pallets.remove(120)

    def add_trucks_for_loose_pallets(self) -> None:
        """If the remaining loose pallets can't fit on the last truck, adds a new truck(s)."""
        # If no arrangements can be formed, adds an empty truck
        if self.number_of_arrangements == 0 and self.number_of_loose_pallets != 0:
            self.add_truck()
        # If there's too many loose pallets to fit on the last truck, adds empty truck(s)
        loose_ldm_remaining: int = self.ldm_of_loose_pallets
        while loose_ldm_remaining > 0:
            # If there is no ldm left on the last truck, always adds a new one
            if self.last_truck.remaining_ldm == 0:
                self.add_truck()
                continue
            # Reduces loose_ldm_remaining by its own value or the free space on the last truck, whichever is smaller
            ldm_to_subtract = min(loose_ldm_remaining, self.last_truck.remaining_ldm)
            loose_ldm_remaining -= ldm_to_subtract
            # If there are still loose pallets, adds a truck
            if loose_ldm_remaining > 0:
                self.add_truck()

    def process_trucks(self) -> None:
        """
        Distributes arrangements between trucks, then distributes loose 120 pallets,
        forms arrangements out of them and sorts the arrangements on trucks according to ARRANGEMENT_ORDER.
        """
        self.distribute_arrangements()
        self.distribute_120_pallets()
        for truck in self.trucks:
            truck.form_120_arrangements()
            truck.sort_arrangements()
        self.add_trucks_for_loose_pallets()
