from arrangement_collection_abstract_class import ArrangementCollection


class Truck(ArrangementCollection):
    """Represents one truck, containing arrangements (tuples) and loose pallets (integers)."""
    def __init__(self) -> None:
        super().__init__()
