class Grouping:
    def __init__(self):
        # How many arrangements of a given type have been constructed in total
        self.arrangement_count = {
            (17090, 145, 145): 0,
            (17090, 17090, 130, 130, 130): 0,
            (17090, 60): 0,
            (130, 130): 0,
            (120, 120, 120): 0,
            (120, 120): 0,
            (145, 145, 145): 0,
            (17080, 17080, 17080): 0,
            (130, 120, 120): 0,
            (17080, 60): 0,
            (17080, 17080, 120, 60): 0,
            (17080, 120, 120, 60, 60): 0,
            (60, 60, 60): 0,
            (120, 120, 60, 60): 0,
            (120, 60, 60, 60, 60): 0,
            (120114, 120114): 0,
            (120104, 120104): 0,
            (120114, 120104): 0,
            (17080, 120114): 0,
            (17080, 120104): 0,
            (120114,): 0,
            (120104,): 0,
            (17080,): 0
        }
        # How many loose pallets (not fitting into any arrangements) there are of a given type
        self.loose_pallet_count = {
            60: 0,
            120: 0,
            145: 0,
            130: 0,
            17080: 0,
            17090: 0,
            120114: 0,
            120104: 0
        }

    def add_arrangement(self, arrangement) -> None:
        self.arrangement_count[arrangement] += 1
