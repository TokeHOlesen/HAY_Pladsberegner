from truck_class import Truck


class AllTrucks:
    """Represents all the trucks necessary to transport all the pallets."""
    def __init__(self) -> None:
        # Holds objects of the Truck class, containing all pallets, sorted into arrangements and loose pallets
        self.trucks = []
