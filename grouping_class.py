from arrangement_collection_abstract_class import ArrangementCollection


class Grouping(ArrangementCollection):
    """
    Represents one grouping, containing all pallets, split into arrangements (tuples) and loose pallets (integers).
    """
    def __init__(self) -> None:
        super().__init__()
