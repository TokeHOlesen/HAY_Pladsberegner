from arrangement_collection_abstract_class import ArrangementCollection


class Grouping(ArrangementCollection):
    """
    Represents one grouping, containing all pallets, split into arrangements (tuples) and loose pallets (integers).
    """
    def __init__(self) -> None:
        super().__init__()

    @property
    def is_perfect(self) -> bool:
        """A grouping is considered perfect if it contains no loose pallets; it is an ideal solution."""
        return len(self.loose_pallets) == 0
