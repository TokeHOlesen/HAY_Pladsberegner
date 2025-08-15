from arrangement_collection_abstract_class import ArrangementCollection


class Grouping(ArrangementCollection):
    """
    Represents one grouping, containing all pallets, split into arrangements (tuples) and loose pallets (integers).
    """
    def __init__(self) -> None:
        super().__init__()

    @property
    def is_perfect(self) -> bool:
        """
        A grouping is considered perfect if it contains no loose pallets; it is an ideal solution.
        Since any amount of 120 pallets >1 can form arrangements, and because 120 pallets are distributed among trucks
        after other arrangements have been formed, any grouping that only contains at least 2 120 pallets is also
        considered perfect.
        """
        # Perfect if there are no loose pallets
        if len(self.loose_pallets) == 0:
            return True
        # Always imperfect if there is only one loose pallet, regardless of type
        elif len(self.loose_pallets) == 1:
            return False

        # Perfect if the only type in the loose pool is 120
        for pallet in self.loose_pallets:
            if pallet != 120:
                return False
        return True
