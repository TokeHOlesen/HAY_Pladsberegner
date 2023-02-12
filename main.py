# Optimized for Python 3.11
# ver. 0.9.0.2 / 11-feb-2023

from itertools import permutations
from math import ceil
from copy import deepcopy
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
from functools import partial
from threading import Thread
from os import path

# Largest load allowed on a truck (ldm * 100)
# 1350 is optimal, 1360 is risky, 1340 and less is safe but potentially wasteful
# This value can be changed by the user
max_truck_ldm = 1350

trucks = []
truck_to_draw = 0
brush_position = 0
number_of_trucks = 0
number_of_pallets_by_truck = []
ldm_by_truck = []
ldm_of_leftovers = 0
entry_focus = 0

# Pallet colours
color_60 = "#5555ff"
color_130 = "#55ff55"
color_145 = "#55ffff"
color_17090 = "#ff5555"
color_17080 = "#ff55ff"
color_120 = "#ffff55"

# An "arrangement" is defined as a group of pallets that end in a straight line, resulting in no wasted space between
# multiple arrangements. A set of arrangements that contains all pallets is defined as a "grouping".
# Pallets in a grouping that don't fit into any arrangement are defined as "leftovers".
# The grouping determined to be optimal (the least used space and the fewest leftovers) will be broken up into "trucks".

# A list will be created with all possible permutations of these arrangements, with the length of n!, where n is the
# number of elements of permutable_arrangements. 8 elements is optimal, 9 is the practical maximum.
permutable_arrangements = [
    (17090, 145, 145),
    (17090, 17090, 130, 130, 130),
    (17080, 17080, 120, 60),
    (17080, 120, 120, 60, 60),
    (120, 120),
    (120, 120, 60, 60),
    (17090, 60),
    (130, 120, 120)
]

# These will be appended to every permutation of permutable_arrangements in a fixed order.
non_permutable_arrangements = [
    (120, 60, 60, 60, 60),
    (17080, 60),
    (145, 145, 145),
    (130, 130),
    (17080, 17080, 17080),
    (60, 60, 60)
]

# How much space each arrangement takes up (ldm * 10)
arrangement_values = {
    (17090, 145, 145): 171,
    (17090, 17090, 130, 130, 130): 342,
    (17090, 60): 90,
    (130, 130): 140,
    (120, 120, 120): 120,
    (120, 120): 80,
    (145, 145, 145): 148,
    (17080, 17080, 17080): 170,
    (130, 120, 120): 160,
    (17080, 60): 80,
    (17080, 17080, 120, 60): 170,
    (17080, 120, 120, 60, 60): 170,
    (60, 60, 60): 60,
    (120, 120, 60, 60): 120,
    (120, 60, 60, 60, 60): 120
}

# Counter for arrangements of a given type
arrangement_counter = {
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
    (120, 60, 60, 60, 60): 0
}

# Used for text output - self-explanatory
arrangement_formatted_output = {
    (17090, 145, 145): "170x90, 145x80, 145x80",
    (17090, 17090, 130, 130, 130): "170x90, 170x90, 130x115, 130x115, 130x115",
    (17090, 60): "170x90, 60x80 (på tværs)",
    (130, 130): "130x115, 130x115",
    (120, 120, 120): "120x80, 120x80, 120x80",
    (120, 120): "120x80, 120x80 (på tværs)",
    (145, 145, 145): "145x80, 145x80, 145x80",
    (17080, 17080, 17080): "170x80, 170x80, 170x80",
    (130, 120, 120): "130x115, 120x80, 120x80",
    (17080, 60): "170x80, 60x80 (på tværs)",
    (17080, 17080, 120, 60): "170x80, 170x80, 120x80, 60x80",
    (17080, 120, 120, 60, 60): "170x80, 120x80, 120x80, 60x80, 60x80",
    (60, 60, 60): "60x80, 60x80, 60x80",
    (120, 120, 60, 60): "120x80, 120x80, 60x80, 60x80",
    (120, 60, 60, 60, 60): "120x80, 60x80, 60x80, 60x80, 60x80"
}

pallet_formatted_output = {
    60: "60x80",
    120: "120x80",
    145: "145x80",
    130: "130x115",
    17080: "170x80",
    17090: "170x90"
}

# How much space a single pallet of a given type takes up (ldm * 100)
pallet_values = {
    60: 20,
    120: 40,
    145: 50,
    130: 70,
    17080: 60,
    17090: 80
}

# Counts loose pallets
pallet_counter = {
    60: 0,
    120: 0,
    145: 0,
    130: 0,
    17080: 0,
    17090: 0
}

# The order in which arrangements will be shown on trucks

arrangement_order = [
    (17080, 17080, 17080),
    (17080, 17080, 120, 60),
    (17080, 120, 120, 60, 60),
    (17090, 145, 145),
    (17090, 17090, 130, 130, 130),
    (120, 120, 120),
    (120, 120),
    (120, 120, 60, 60),
    (120, 60, 60, 60, 60),
    (145, 145, 145),
    (130, 130),
    (17090, 60),
    (17080, 60),
    (60, 60, 60),
    (130, 120, 120)
]


# Moves focus to the next entry box or the Start button (runs when Enter is pressed)
def move_focus(event):
    global entry_focus

    if str(window.focus_get()) == ".!frame.!entry":
        entry_focus = 0
    else:
        entry_focus = int(str(window.focus_get())[-1]) - 1

    if entry_focus < 5:
        entry_focus += 1
        entry_boxes[entry_focus].focus_set()
    elif entry_focus == 5:
        entry_focus = 0
        start_button.focus_set()


# Resets global values
# When "full" is passed as a parameter, resets everything
# Otherwise leaves contents of entry boxes, max_target_ldm and text_output intact - useful when recalculating
def reset_all(mode):
    global pallet_counter
    global trucks
    global truck_to_draw
    global brush_position
    global number_of_trucks
    global number_of_pallets_by_truck
    global ldm_by_truck
    global max_truck_ldm
    global ldm_of_leftovers
    global entry_focus
    pallet_counter = pallet_counter.fromkeys(pallet_counter, 0)
    trucks = []
    truck_to_draw = 0
    brush_position = 0
    number_of_trucks = 0
    number_of_pallets_by_truck = []
    ldm_by_truck = []
    ldm_of_leftovers = 0
    entry_focus = 0

    truck_canvas.delete("all")
    draw_truck_rectangle(truck_canvas)
    leftovers_canvas.delete("all")
    draw_truck_rectangle(leftovers_canvas)

    label_truck.config(text="N/A")
    label_leftovers.config(text="N/A")
    label_pallets_ldm.config(text="N/A")
    label_leftovers_ldm.config(text="N/A")

    no_of_trucks_label.config(text=f"Biler i alt: {number_of_trucks}")

    start_button.config(state=NORMAL)
    next_button.config(state=DISABLED)
    previous_button.config(state=DISABLED)

    entry_boxes[entry_focus].focus_set()

    if mode == "full":
        for entry in entry_boxes:
            entry.delete(0, END)

        max_truck_ldm = 1350
        entry_ldm.delete(0, END)
        entry_ldm.insert(0, str(max_truck_ldm / 100))

        status_label.config(text="Klar.")

        text_output.config(state=NORMAL)
        text_output.delete('1.0', END)
        text_output.insert("end", "Klar.")
        text_output.config(state=DISABLED)


# Reads the contents of ldm_entry entry box and extracts a max_target_ldm value
# Corrects to 13.6 if the requested value is higher than 13.6, or to 3.5 if it's lower than 3.5
# Corrects to 13.5 if the value is not a valid number
def set_target_ldm(ldm_input):
    global max_truck_ldm
    ldm_input = ldm_input.replace(",", ".")
    ldm_control = ldm_input.replace(".", "")
    if ldm_control.isnumeric():
        max_truck_ldm = int(float(ldm_input) * 100)
        if max_truck_ldm > 1360:
            max_truck_ldm = 1360
            text_output.config(state=NORMAL)
            text_output.insert("end", "\nMax ldm højere end tilladt, rettes til 13,6.")
            text_output.config(state=DISABLED)
        elif max_truck_ldm < 350:
            max_truck_ldm = 350
            text_output.config(state=NORMAL)
            text_output.insert("end", "\nMax ldm lavere end tilladt, rettes til 3,5.")
            text_output.config(state=DISABLED)
    else:
        max_truck_ldm = 1350
    entry_ldm.delete(0, END)
    entry_ldm.insert(0, str(max_truck_ldm / 100))


# Runs the main function in a separate thread
# The thread is declared as a deamon to make sure it is terminated when the main window closes for any reason
def threaded_calculate_pallets(event):
    thread = Thread(target=calculate_pallets, daemon=True)
    thread.start()


# Main function
def calculate_pallets():
    global brush_position
    global trucks
    global number_of_trucks
    global number_of_pallets_by_truck
    global ldm_by_truck
    global ldm_of_leftovers

    # Checks if a given arrangement can be formed within the current pool of pallets; returns True if yes
    def arrangement_is_possible(current_arrangement):
        all_items = all_pallets[:]
        for item in current_arrangement:
            if item in all_items:
                all_items.remove(item)
            else:
                return False
        return True

    # Calculates ldm of leftovers pallets for a given grouping
    def leftovers_ldm(this_index):
        leftovers_ldm_result = 0
        for remaining_pallet in leftover_pallets_in_each_grouping[this_index]:
            remaining_pallet: int
            leftovers_ldm_result += pallet_values[remaining_pallet]
        return leftovers_ldm_result

    # Calculates ldm for a given grouping (sum of pallets in arrangements and leftovers)
    def total_ldm(this_index):
        total_ldm_result = 0
        for checked_grouping in all_possible_groupings[this_index]:
            total_ldm_result += arrangement_values[checked_grouping]
        total_ldm_result += leftovers_ldm(this_index)
        return total_ldm_result

    # Calculates the ldm of a truck
    def truck_ldm(this_truck):
        truck_ldm_result = 0
        for this_grouping in this_truck:
            truck_ldm_result += arrangement_values[this_grouping]
        return truck_ldm_result

    # Returns a list of the ldm values of all arrangements on a given truck, in ascending order
    def ldm_ascending_order(this_truck):
        ldm_ascending_list = []
        for this_grouping in this_truck:
            ldm_ascending_list.append(arrangement_values[this_grouping])
        ldm_ascending_list.sort()
        return ldm_ascending_list

    # Returns a list of the ldm values of all arrangements on a given truck, in descending order
    def ldm_descending_order(this_truck):
        ldm_descending_list = []
        for this_grouping in this_truck:
            ldm_descending_list.append(arrangement_values[this_grouping])
        ldm_descending_list.sort()
        ldm_descending_list.reverse()
        return ldm_descending_list

    # Sorts arrangements on a given truck according to the order of items in arrangement_order
    def sort_truck(truck_index):
        sorted_truck = []
        for current_arrangement in arrangement_order:
            while current_arrangement in trucks[truck_index]:
                sorted_truck.append(current_arrangement)
                trucks[truck_index].remove(current_arrangement)
        trucks[truck_index] = sorted_truck

    # Reorganizes 120s on each truck into the optimal proportion of 120x120x120 and 120x120 arrangements.
    # Moves individual pallets back if there is at least 0.4 ldm of free space on a given truck and at least
    # one other 120 pallet already present.

    def rearrange_120():
        trucks_before_rearrangement = deepcopy(trucks)
        # Calculates the ldm value for each truck and stores it in a list with indexes corresponding to trucks[]
        this_truck_ldm_120 = []
        for this_truck in trucks:
            this_truck_ldm_120.append(truck_ldm(this_truck))
        # Calculates how many individual 120 pallets there are on each truck
        number_of_120 = []
        for t in range(len(trucks)):
            if (120, 120) in trucks[t]:
                buffer_120 = 0
                for this_grouping in trucks[t]:
                    if this_grouping == (120, 120):
                        buffer_120 += 2
                # If there's room, transfers 120 pallets from the leftover pool
                while this_truck_ldm_120[t] <= (max_truck_ldm - 40) and 120 in leftover_pallets:
                    buffer_120 += 1
                    this_truck_ldm_120[t] += 4
                    leftover_pallets.remove(120)
                number_of_120.append(buffer_120)
            else:
                number_of_120.append(0)
        # If there's at least 0.4 ldm of free space and at least one 120 already present, moves pallets back
        for t in range(1, len(trucks)):
            for p in range(t):
                while number_of_120[p] >= 1 and number_of_120[t] > 0 and this_truck_ldm_120[p] <= (max_truck_ldm - 40):
                    number_of_120[p] += 1
                    this_truck_ldm_120[p] += 40
                    number_of_120[t] -= 1
                    this_truck_ldm_120[t] -= 40
        # Clears the existing groupings of 120 pallets on all trucks
        for this_truck in trucks:
            while (120, 120) in this_truck:
                this_truck.remove((120, 120))
        # Calculates the optimal distribution of 120 arrangements
        for t in range(len(trucks)):
            number_of_120_120 = 0
            while number_of_120[t] >= 2 and number_of_120[t] % 3 != 0:
                number_of_120[t] -= 2
                number_of_120_120 += 1
            if number_of_120[t] == 1:
                leftover_pallets.append(120)
            number_of_120_120_120 = number_of_120[t] // 3
            # Moves arrangements to their respective trucks
            for g in range(number_of_120_120):
                trucks[t].append((120, 120))
            for g in range(number_of_120_120_120):
                trucks[t].append((120, 120, 120))
        # Returns True if any work was done, or False if not
        # This is used to reset the optimization routine even if no optimization happened in the first pass
        # This is necessary because rearranging 120 pallets may change the pallet setup and make optimization possible
        if trucks_before_rearrangement == trucks:
            return False
        else:
            return True

    # If any data from a previous calculation exists, resets everything except the contens of entry boxes, text output
    # box and the value of max_truck_ldm
    if trucks or ldm_of_leftovers:
        reset_all("partial")

    # Collects number of pallets from entry boxes
    pallet_types = [
        60,
        120,
        145,
        130,
        17080,
        17090
    ]
    pallet_input = []

    for b in range(len(entry_boxes)):
        if entry_boxes[b].get().isnumeric() and int(entry_boxes[b].get()) > 0:
            for c in range(int(entry_boxes[b].get())):
                pallet_input.append(pallet_types[b])

    # Displays a warning messagebox if entry boxes are empty or not filled out properly
    if not pallet_input:
        messagebox.showwarning("Mangler input", "Indtast antal paller.")
        reset_all("full")
        return

    # Sets max ldm per truck
    set_target_ldm(entry_ldm.get())

    # Data processing begins here
    text_output.config(state=NORMAL)

    text_output.insert("end", "\nStarter op...")
    status_label.config(text="Starter op...")

    # Calculates all possible permutations of items in permutable_arrangements
    all_permutations = list(permutations(permutable_arrangements, len(permutable_arrangements)))

    # Combines all permutations of permutable_arrangements with non_permutable_arrangements (fixed order),
    # for a full list of possible permutations of arrangements

    possible_arrangements = []

    for i in range(len(all_permutations)):
        this_permutation = []
        for permutable_arrangement in all_permutations[i]:
            this_permutation.append(permutable_arrangement)
        for non_permutable_arrangement in non_permutable_arrangements:
            this_permutation.append(non_permutable_arrangement)
        possible_arrangements.append(this_permutation)

    text_output.insert("end", "\nBeregner mulige løsninger...")
    status_label.config(text="Beregner løsninger...")

    # Contains all possible groupings
    all_possible_groupings = []

    # For imperfect solutions, contains the leftover pallets for each grouping
    # Indexes for the two above lists match
    leftover_pallets_in_each_grouping = []

    # How much room each grouping requires
    total_ldm_in_each_grouping = []

    # Checks all possible arrangements for matches within the current item pool
    # If a match is found, the groupings are copied to all_possible_groupings
    # If any pallets remain ungrouped, they are copied to leftover_pallets_in_each_grouping
    current_progress = 0
    for i in range(len(possible_arrangements)):
        new_progress = i * 100 // len(possible_arrangements)
        if new_progress != current_progress:
            current_progress = new_progress
            progress_bar["value"] = current_progress
        arrangement_being_checked = possible_arrangements[i]
        current_grouping = []
        all_pallets = pallet_input[:]
        for x in range(len(arrangement_being_checked)):
            while arrangement_is_possible(arrangement_being_checked[x]):
                current_grouping.append(arrangement_being_checked[x])
                for pallet in arrangement_being_checked[x]:
                    all_pallets.remove(pallet)
        all_possible_groupings.append(current_grouping)
        leftover_pallets_in_each_grouping.append(all_pallets)
    progress_bar["value"] = 0

    text_output.insert("end", "\nFinder den optimale løsning...")
    status_label.config(text="Optimerer..")

    # Checks if perfect solutions exist (complete groupings with no leftovers)
    # If a perfect solution is found, purges all imperfect solutions
    for pallets_leftover in leftover_pallets_in_each_grouping:
        if not pallets_leftover:
            groupings_to_delete = []
            for i in range(len(all_possible_groupings) - 1, -1, -1):
                if leftover_pallets_in_each_grouping[i]:
                    groupings_to_delete.append(i)
            for index_to_delete in groupings_to_delete:
                del all_possible_groupings[index_to_delete]
                del leftover_pallets_in_each_grouping[index_to_delete]
            break

    # Calculates ldm value for every grouping
    for grouping_index in range(len(all_possible_groupings)):
        total_ldm_in_each_grouping.append(total_ldm(grouping_index))

    # Finds lowest ldm value for leftover items
    lowest_remaining_ldm = 65535
    for pallets_remaining in leftover_pallets_in_each_grouping:
        remaining_ldm = 0
        for pallet in pallets_remaining:
            remaining_ldm += pallet_values[pallet]
        if remaining_ldm < lowest_remaining_ldm:
            lowest_remaining_ldm = remaining_ldm

    # Deletes groupings where leftover ldm is higher than lowest found
    for ldm_index in range(len(leftover_pallets_in_each_grouping) - 1, -1, -1):
        if leftovers_ldm(ldm_index) > lowest_remaining_ldm:
            del all_possible_groupings[ldm_index]
            del leftover_pallets_in_each_grouping[ldm_index]
            del total_ldm_in_each_grouping[ldm_index]

    # Finds lowest ldm value for groupings
    lowest_ldm = 65535
    for checked_ldm in total_ldm_in_each_grouping:
        if checked_ldm < lowest_ldm:
            lowest_ldm = checked_ldm

    # Deletes groupings with ldm values higher than lowest found
    for ldm_index in range(len(all_possible_groupings) - 1, -1, -1):
        if total_ldm_in_each_grouping[ldm_index] > lowest_ldm:
            del all_possible_groupings[ldm_index]
            del leftover_pallets_in_each_grouping[ldm_index]
            del total_ldm_in_each_grouping[ldm_index]

    # Copies the first elements of the arrays into lists containing the final grouping
    final_grouping = all_possible_groupings[0]
    leftover_pallets = leftover_pallets_in_each_grouping[0]

    # If there are 2 or more (130, 120, 120) groups, reorganizes them into (130, 130) and (120, 120) groups.

    if (130, 120, 120) in final_grouping:
        number_of_130_120_120 = 0
        for arrangement in final_grouping:
            if arrangement == (130, 120, 120):
                number_of_130_120_120 += 1
        if number_of_130_120_120 >= 2:
            if number_of_130_120_120 % 2 != 0:
                number_to_reorganize = (number_of_130_120_120 - 1) // 2
            else:
                number_to_reorganize = number_of_130_120_120 // 2
            for i in range(number_to_reorganize):
                for x in range(2):
                    final_grouping.remove((130, 120, 120))
                    final_grouping.append((120, 120))
                final_grouping.append((130, 130))

    status_label.config(text="Færdig.")

    # Calculates how many trucks are needed and what goes on which

    # Copies all arrangements into a working space
    arrangements_not_yet_used = deepcopy(final_grouping)

    # Splits all arrangements into trucks;
    # Arrangements are added until ldm exceeds max_truck_ldm, the smallest arrangements are then subtracted
    # until it reaches 13.6 or less, then moves on to the next truck.

    while arrangements_not_yet_used:
        truck_buffer = []
        truck_buffer_ldm = []

        while sum(truck_buffer_ldm) < max_truck_ldm and arrangements_not_yet_used != []:
            for arrangement in arrangements_not_yet_used:
                truck_buffer.append(arrangement)
                truck_buffer_ldm.append(arrangement_values[arrangement])
                arrangements_not_yet_used.remove(arrangement)

        while sum(truck_buffer_ldm) > max_truck_ldm:
            arrangements_not_yet_used.append(truck_buffer.pop())
            truck_buffer_ldm.pop()

        trucks.append(truck_buffer)

    # Space optimization:
    # If there's more than one truck, checks if anything can be moved back to a previous truck
    # Then, checks if any smaller groupings can be swapped with bigger ones from the next truck

    # Optimization runs only if this flag is set to true
    # Set to true by default to make sure it runs at least once
    # Once started, it is reset to False and only set to True again if any changes have been made
    optimization_possible = True

    while optimization_possible:
        optimization_possible = False
        # Attempts to move whole arrangements back to a previous truck, if there is room
        if len(trucks) > 1:
            for i in range(1, len(trucks)):
                for arrangement in trucks[i]:
                    for x in range(i, 0, -1):
                        if truck_ldm(trucks[i - x]) + arrangement_values[arrangement] <= max_truck_ldm:
                            trucks[i - x].append(arrangement)
                            trucks[i].remove(arrangement)
                            optimization_possible = True
                            break
            # Swaps smaller arrangements for bigger ones to make optimal use of space
            for i in range(1, len(trucks)):
                for x in range(i):
                    for low_ldm in ldm_ascending_order(trucks[x]):
                        space_available = max_truck_ldm - truck_ldm(trucks[x])
                        if space_available:
                            for high_ldm in ldm_descending_order(trucks[i]):
                                if high_ldm - low_ldm <= space_available:
                                    if high_ldm > low_ldm:
                                        optimization_possible = True
                                        for high_arrangement in trucks[i]:
                                            if arrangement_values[high_arrangement] == high_ldm:
                                                trucks[i].remove(high_arrangement)
                                                trucks[x].append(high_arrangement)
                                                break
                                        for low_arrangement in trucks[x]:
                                            if arrangement_values[low_arrangement] == low_ldm:
                                                trucks[x].remove(low_arrangement)
                                                trucks[i].append(low_arrangement)
                                                break
                                        break

        # If possible, rearranges 120 pallets into optimal groups
        # If anything has been rearranged, makes the optimization routine run again
        optimization_possible = optimization_possible or rearrange_120()

    # Sometimes after optimization, the last trucks end up empty
    # Checks and removes them if that's the case
    while len(trucks) > 0 and not trucks[-1]:
        trucks.pop()

    # Sorts items on all trucks
    for i in range(len(trucks)):
        sort_truck(i)

    # Counts the remaining (ungroupable) items and calculates their total ldm
    for pallet in leftover_pallets:
        pallet_counter[pallet] += 1

    if leftover_pallets:
        for pallet in pallet_counter:
            if pallet_counter[pallet] != 0:
                ldm_of_leftovers += pallet_values[pallet] * pallet_counter[pallet]

    # Increases the number of trucks needed if there's not enough room for leftovers after
    # the groupable items have been assigned to their trucks.
    if len(trucks) > 0:
        number_of_trucks = len(trucks)
        if truck_ldm(trucks[len(trucks) - 1]) + ldm_of_leftovers > max_truck_ldm:
            additional_trucks_needed = ceil(ldm_of_leftovers / max_truck_ldm)
            for i in range(additional_trucks_needed):
                trucks.append([])
            number_of_trucks += additional_trucks_needed
    else:
        if leftover_pallets:
            additional_trucks_needed = ceil(ldm_of_leftovers / max_truck_ldm)
            number_of_trucks = additional_trucks_needed
            for i in range(additional_trucks_needed):
                trucks.append([])
        else:
            number_of_trucks = 0

    # Text output of truck contents

    truck_number = 0
    pallets_total = 0

    for truck in trucks:
        pallets_on_truck = 0
        truck_number += 1

        for pallet in arrangement_counter:
            arrangement_counter[pallet] = 0

        for arrangement in truck:
            arrangement_counter[arrangement] += 1
            pallets_on_truck += len(arrangement)

        number_of_pallets_by_truck.append(pallets_on_truck)
        pallets_total += pallets_on_truck

        text_output.insert("end", f"\n\nBil {truck_number}:")
        if not truck:
            text_output.insert("end", "\nRester.")
        else:
            current_truck_ldm = 0
            for arrangement in arrangement_counter:
                if arrangement_counter[arrangement] != 0:
                    this_truck_ldm = arrangement_values[arrangement] * arrangement_counter[arrangement]
                    text_output.insert(
                        "end", f"\n{arrangement_formatted_output[arrangement]} x {arrangement_counter[arrangement]} "
                               f"({arrangement_values[arrangement] / 100} * {arrangement_counter[arrangement]} = "
                               f"{this_truck_ldm / 100} ldm)")
                    current_truck_ldm += this_truck_ldm

            ldm_by_truck.append(current_truck_ldm)
            text_output.insert("end", f"\n{current_truck_ldm / 100} ldm i grupper ({pallets_on_truck} paller).")

    # Text output of remaining pallets

    text_output.insert("end", "\n\nRest:")
    if leftover_pallets:
        for pallet in pallet_counter:
            if pallet_counter[pallet] != 0:
                text_output.insert("end", f"\n{pallet_formatted_output[pallet]}: x {pallet_counter[pallet]}")
        text_output.insert("end", f"\nI alt rester: {ldm_of_leftovers / 100} ldm.")
        pallets_total += len(leftover_pallets)
    else:
        text_output.insert("end", "\nIngen.")

    # Text summary
    ldm_of_groupable_items = 0
    for truck in trucks:
        ldm_of_groupable_items += truck_ldm(truck)

    paller = "paller"
    if pallets_total == 1:
        paller = "palle"

    biler = "biler"
    if number_of_trucks == 1:
        biler = "bil"

    text_output.insert(
        "end", f"\n\nI alt: {ldm_of_groupable_items / 100} ldm i grupper + "
               f"{ldm_of_leftovers / 100} ldm rest = "
               f"{(ldm_of_groupable_items + ldm_of_leftovers) / 100} ldm ({pallets_total} {paller}).")
    text_output.insert("end", f"\nSkal hentes af {number_of_trucks} {biler}.")

    text_output.insert("end", "\n\nFærdig.")
    text_output.see("end")
    text_output.config(state=DISABLED)

    # Draws truck contents and leftovers; adjusts UI elements
    if len(trucks) > 0:
        draw_truck(truck_to_draw)

    if len(trucks) > 1:
        next_button.config(state=NORMAL)

    if leftover_pallets:
        brush_position = 20
        unique_leftover_pallets = [*set(leftover_pallets)]
        unique_leftover_pallets.sort()
        for pallet in unique_leftover_pallets:
            draw_leftovers(pallet, leftovers_canvas, "normal")
        label_leftovers_ldm.config(text=f"{len(leftover_pallets)} pll, ~{round(ldm_of_leftovers / 100, 1)} ldm")
    else:
        draw_leftovers("", leftovers_canvas, "none")

    no_of_trucks_label.config(text=f"Biler i alt: {number_of_trucks}")

    if number_of_pallets_by_truck and ldm_by_truck:
        label_pallets_ldm.config(text=f"{number_of_pallets_by_truck[0]} pll, {round(ldm_by_truck[0] / 100, 1)} ldm")

    entry_boxes[0].focus_set()


# Draws an empty white rectangle for use as a background for truck contents or leftovers
def draw_truck_rectangle(canvas):
    canvas.create_rectangle(0, 0, 98, 538, fill="#ffffff")


# Draws the contents of a given truck on truck_canvas
def draw_truck(truck_to_be_drawn):
    if trucks[truck_to_be_drawn]:
        for this_arrangement in trucks[truck_to_be_drawn]:
            draw_arrangement(this_arrangement, truck_canvas)
    else:
        truck_canvas.create_text(48, 255, text="Rester", font=("", "13"))
    label_truck.config(text=f"Bil {truck_to_be_drawn + 1}")


# Draws the contents of the next or the previous truck, depending on which button has been pressed
def draw_another_truck(direction):
    global truck_to_draw
    global brush_position
    brush_position = 0

    truck_canvas.delete("all")
    draw_truck_rectangle(truck_canvas)

    if direction == "Next":
        if len(trucks) - 1 > truck_to_draw:
            truck_to_draw += 1
        draw_truck(truck_to_draw)
        if truck_to_draw > 0:
            previous_button.config(state=NORMAL)
        if len(trucks) - 1 == truck_to_draw:
            next_button.config(state=DISABLED)

    elif direction == "Previous":
        if not truck_to_draw == 0:
            truck_to_draw -= 1
        draw_truck(truck_to_draw)
        if truck_to_draw == 0:
            previous_button.config(state=DISABLED)
        if len(trucks) - 1 > truck_to_draw:
            next_button.config(state=NORMAL)

    if trucks[truck_to_draw]:
        label_pallets_ldm.config(
            text=f"{number_of_pallets_by_truck[truck_to_draw]} pll, {round(ldm_by_truck[truck_to_draw] / 100, 1)} ldm")
    else:
        label_pallets_ldm.config(text="N/A")


# Draws an arrangement and its description at brush_position on truck_canvas
def draw_arrangement(arrangement, canvas):
    global brush_position
    y = brush_position

    def draw_bracket(yy, yy2):
        canvas.create_line(103, yy + 4, 107, yy + 4)
        canvas.create_line(107, yy + 4, 107, yy2 - 2)
        canvas.create_line(103, yy2 - 2, 107, yy2 - 2)

    def draw_description(yy, text):
        canvas.create_text(115, y + yy, text=text, font=("", "8"), anchor="w")

    if arrangement == (120, 120, 120):
        y2 = y + 48
        canvas.create_rectangle(0 + 2, y + 2, 32, y2 - 1, fill=color_120)
        canvas.create_rectangle(32 + 2, y + 2, 64, y2 - 1, fill=color_120)
        canvas.create_rectangle(64 + 2, y + 2, 96, y2 - 1, fill=color_120)
        draw_bracket(y, y2)
        draw_description(16, "120x80 x 3")
        draw_description(31, "1,2 ldm")
        brush_position += 48 - 1
    elif arrangement == (120, 120):
        y2 = y + 32
        canvas.create_rectangle(0 + 2, y + 2, 48, y2 - 1, fill=color_120)
        canvas.create_rectangle(48 + 2, y + 2, 96, y2 - 1, fill=color_120)
        draw_bracket(y, y2)
        draw_description(17, "120x80 x 2, 0,8 ldm")
        brush_position += 32 - 1
    elif arrangement == (145, 145, 145):
        y2 = y + 59
        canvas.create_rectangle(0 + 2, y + 2, 32, y2 - 1, fill=color_145)
        canvas.create_rectangle(32 + 2, y + 2, 64, y2 - 1, fill=color_145)
        canvas.create_rectangle(64 + 2, y + 2, 96, y2 - 1, fill=color_145)
        draw_bracket(y, y2)
        draw_description(22, "145x80 x 3")
        draw_description(37, "1,5 ldm")
        brush_position += 59 - 1
    elif arrangement == (17080, 17080, 17080):
        y2 = y + 68
        canvas.create_rectangle(0 + 2, y + 2, 32, y2 - 1, fill=color_17080)
        canvas.create_rectangle(32 + 2, y + 2, 64, y2 - 1, fill=color_17080)
        canvas.create_rectangle(64 + 2, y + 2, 96, y2 - 1, fill=color_17080)
        draw_bracket(y, y2)
        draw_description(24, "170x80 x 3")
        draw_description(39, "1,7 ldm")
        brush_position += 68 - 1
    elif arrangement == (130, 130):
        y2 = y + 56
        canvas.create_rectangle(0 + 2, y + 2, 48, y2 - 1, fill=color_130)
        canvas.create_rectangle(48 + 2, y + 2, 96, y2 - 1, fill=color_130)
        draw_bracket(y, y2)
        draw_description(20, "130x115 x 2")
        draw_description(35, "1,4 ldm")
        brush_position += 56 - 1
    elif arrangement == (60, 60, 60):
        y2 = y + 24
        canvas.create_rectangle(0 + 2, y + 2, 32, y2 - 1, fill=color_60)
        canvas.create_rectangle(32 + 2, y + 2, 64, y2 - 1, fill=color_60)
        canvas.create_rectangle(64 + 2, y + 2, 96, y2 - 1, fill=color_60)
        draw_bracket(y, y2)
        draw_description(13, "60x80 x 3, 0,6 ldm")
        brush_position += 24 - 1
    elif arrangement == (120, 120, 60, 60):
        y2 = y + 48
        canvas.create_rectangle(0 + 2, y + 2, 32, y2 - 1, fill=color_120)
        canvas.create_rectangle(32 + 2, y + 2, 64, y2 - 1, fill=color_120)
        canvas.create_rectangle(64 + 2, y + 2, 96, y2 - 24 - 1, fill=color_60)
        canvas.create_rectangle(64 + 2, y + 24 + 1, 96, y2 - 1, fill=color_60)
        draw_bracket(y, y2)
        draw_description(10, "120x80 x 2")
        draw_description(25, "60x80 x 2")
        draw_description(40, "1,2 ldm")
        brush_position += 48 - 1
    elif arrangement == (120, 60, 60, 60, 60):
        y2 = y + 48
        canvas.create_rectangle(0 + 2, y + 2, 32, y2 - 1, fill=color_120)
        canvas.create_rectangle(32 + 2, y + 2, 64, y2 - 24 - 1, fill=color_60)
        canvas.create_rectangle(32 + 2, y + 24 + 1, 64, y2 - 1, fill=color_60)
        canvas.create_rectangle(64 + 2, y + 2, 96, y2 - 24 - 1, fill=color_60)
        canvas.create_rectangle(64 + 2, y + 24 + 1, 96, y2 - 1, fill=color_60)
        draw_bracket(y, y2)
        draw_description(10, "120x80 x 1")
        draw_description(25, "60x80 x 4")
        draw_description(40, "1,2 ldm")
        brush_position += 48 - 1
    elif arrangement == (17090, 145, 145):
        y2 = y + 68
        canvas.create_rectangle(0 + 2, y + 2, 36, y2 - 1, fill=color_17090)
        canvas.create_rectangle(36 + 2, y + 2, 96, y2 - 36 - 1, fill=color_145)
        canvas.create_rectangle(36 + 2, y + 32 + 1, 96, y2 - 4 - 1, fill=color_145)
        draw_bracket(y, y2)
        draw_description(18, "170x90 x 1")
        draw_description(33, "145x80 x 2")
        draw_description(48, "1,7 ldm")
        brush_position += 68 - 1
    elif arrangement == (17090, 17090, 130, 130, 130):
        y2 = y + 68
        y3 = y + 45
        canvas.create_rectangle(0 + 2, y + 2, 36, y2 - 1, fill=color_17090)
        canvas.create_rectangle(0 + 2, y + 68 + 1, 36, y2 + 67 - 1, fill=color_17090)
        canvas.create_rectangle(36 + 2, y + 2, 96, y3, fill=color_130)
        canvas.create_rectangle(36 + 2, y + 45 + 2, 96, y3 + 45 - 1, fill=color_130)
        canvas.create_rectangle(36 + 2, y + 90 + 1, 96, y3 + 90 - 1, fill=color_130)
        draw_bracket(y, y2 + 67)
        draw_description(50, "170x90 x 2")
        draw_description(65, "130x115 x 3")
        draw_description(80, "3,4 ldm")
        brush_position += 135 - 1
    elif arrangement == (17080, 17080, 120, 60):
        y2 = y + 68
        canvas.create_rectangle(0 + 2, y + 2, 32, y2 - 1, fill=color_17080)
        canvas.create_rectangle(32 + 2, y + 2, 64, y2 - 1, fill=color_17080)
        canvas.create_rectangle(64 + 2, y + 2, 96, y2 - 24 - 1, fill=color_120)
        canvas.create_rectangle(64 + 2, y + 44 + 1, 96, y2 - 1, fill=color_60)
        draw_bracket(y, y2)
        draw_description(12, "170x80 x 2")
        draw_description(27, "120x80 x 1")
        draw_description(42, "60x80 x 1")
        draw_description(57, "1,7 ldm")
        brush_position += 68 - 1
    elif arrangement == (17080, 120, 120, 60, 60):
        y2 = y + 68
        canvas.create_rectangle(0 + 2, y + 2, 32, y2 - 1, fill=color_17080)
        canvas.create_rectangle(32 + 2, y + 2, 64, y2 - 24 - 1, fill=color_120)
        canvas.create_rectangle(64 + 2, y + 2, 96, y2 - 24 - 1, fill=color_120)
        canvas.create_rectangle(32 + 2, y + 44 + 1, 64, y2 - 1, fill=color_60)
        canvas.create_rectangle(64 + 2, y + 44 + 1, 96, y2 - 1, fill=color_60)
        draw_bracket(y, y2)
        draw_description(12, "170x80 x 2")
        draw_description(27, "120x80 x 3")
        draw_description(42, "60x80 x 3")
        draw_description(57, "1,7 ldm")
        brush_position += 68 - 1
    elif arrangement == (17080, 60):
        y2 = y + 32
        canvas.create_rectangle(0 + 2, y + 2, 68, y2 - 1, fill=color_17080)
        canvas.create_rectangle(69 + 2, y + 2, 94, y2 - 1, fill=color_60)
        draw_bracket(y, y2)
        draw_description(10, "170x80 x 1, 60x80 x 1")
        draw_description(25, "0,8 ldm")
        brush_position += 32 - 1
    elif arrangement == (17090, 60):
        y2 = y + 36
        canvas.create_rectangle(0 + 2, y + 2, 68, y2 - 1, fill=color_17090)
        canvas.create_rectangle(69 + 2, y + 2, 94, y2 - 4 - 1, fill=color_60)
        draw_bracket(y, y2)
        draw_description(10, "170x90 x 1, 60x80 x 1")
        draw_description(25, "0,9 ldm")
        brush_position += 36 - 1
    elif arrangement == (130, 120, 120):
        y2 = y + 64
        canvas.create_rectangle(0 + 2, y + 2, 48, y2 - 8 - 1, fill=color_130)
        canvas.create_rectangle(48 + 2, y + 2, 96, y2 - 32 - 1, fill=color_120)
        canvas.create_rectangle(48 + 2, y + 32 + 1, 96, y2 - 1, fill=color_120)
        draw_bracket(y, y2)
        draw_description(16, "130x115 x 1")
        draw_description(31, "120x80 x 2")
        draw_description(46, "1,6 ldm")
        brush_position += 64 - 1


# Draws a representation of leftover pallets and their description on leftover_canvas
# If the "mode" parameter equals "normal", draws pallets; if "none", draws a message that there's nothing to show
def draw_leftovers(pallet, canvas, mode):
    global brush_position

    if mode == "normal":
        label_leftovers.config(text=f"Rester")
        y = brush_position

        def draw_number_of_leftovers(yy, pallet_type):
            canvas.create_text(70, y + yy, text=f"x{pallet_counter[pallet_type]}", font=("", "13"), anchor="w")

        def draw_description(yy, text, pallet_type):
            canvas.create_text(115, y + yy, text=text, font=("", "8"), anchor="w")
            canvas.create_text(115, y + yy + 15, text=f"{pallet_counter[pallet_type]} stk", font=("", "8"), anchor="w")

        if pallet == 60:
            y2 = y + 24
            canvas.create_rectangle(12 + 2, y + 2, 44, y2 - 1, fill=color_60)
            draw_number_of_leftovers(12, 60)
            draw_description(5, "60x80", 60)
            brush_position += 54 - 1
        elif pallet == 120:
            y2 = y + 48
            canvas.create_rectangle(12 + 2, y + 2, 44, y2 - 1, fill=color_120)
            draw_number_of_leftovers(24, 120)
            draw_description(18, "120x80", 120)
            brush_position += 78 - 1
        elif pallet == 145:
            y2 = y + 60
            canvas.create_rectangle(12 + 2, y + 2, 44, y2 - 1, fill=color_145)
            draw_number_of_leftovers(30, 145)
            draw_description(22, "145x80", 145)
            brush_position += 90 - 1
        elif pallet == 130:
            y2 = y + 56
            canvas.create_rectangle(12 + 2, y + 2, 60, y2 - 1, fill=color_130)
            draw_number_of_leftovers(28, 130)
            draw_description(21, "130x115", 130)
            brush_position += 86 - 1
        elif pallet == 17080:
            y2 = y + 68
            canvas.create_rectangle(12 + 2, y + 2, 44, y2 - 1, fill=color_17080)
            draw_number_of_leftovers(34, 17080)
            draw_description(28, "170x80", 17080)
            brush_position += 98 - 1
        elif pallet == 17090:
            y2 = y + 68
            canvas.create_rectangle(12 + 2, y + 2, 48, y2 - 1, fill=color_17090)
            draw_number_of_leftovers(34, 17090)
            draw_description(28, "170x90", 17090)
            brush_position += 98 - 1
    elif mode == "none":
        canvas.create_text(48, 255, text="Ingen rest", font=("", "13"))


# GUI starts here

window = Tk()
window.title("HAY pladsberegner")
window.geometry("572x788")
window.resizable(False, False)

if path.isfile("truck_ico.ico"):
    window.iconbitmap("truck_ico.ico")

# Declaration of GUI elements

# This frame holds the entry boxes for inputting pallet numbers and the corresponding labels
entry_frame = Frame(window)

entry_label_text = [
    "60x80:    ",
    "120x80:    ",
    "145x80:    ",
    "130x115:    ",
    "170x80:    ",
    "170x90:    ",
]

entry_labels = []

for k in range(6):
    entry_label = Label(entry_frame, width=10, anchor="e", text=entry_label_text[k])
    entry_labels.append(entry_label)

for k in range(6):
    entry_labels[k].grid(row=k, column=0, pady=2)

entry_boxes = []

for e in range(6):
    entry_box = Entry(entry_frame, width=7, justify=RIGHT)
    entry_boxes.append(entry_box)
    entry_boxes[e].bind("<Return>", move_focus)

for e in range(6):
    entry_boxes[e].grid(row=e, column=1, pady=2)

# Other GUI elements - self-explanatory

start_button = Button(window, text="Start", width=10, command=partial(threaded_calculate_pallets, "Null"))
start_button.bind("<Return>", threaded_calculate_pallets)

progress_bar = ttk.Progressbar(window, length=116)

status_label = Label(window, text="Klar.")

target_ldm_frame = Frame(window)

enter_ldm_label = Label(target_ldm_frame, width=10, anchor="e", text="Max ldm:  ")
enter_ldm_label.grid(row=0, column=0, pady=2)

entry_ldm = Entry(target_ldm_frame, width=7, justify=RIGHT)
entry_ldm.insert(0, str(max_truck_ldm / 100))
entry_ldm.grid(row=0, column=1, pady=2)

reset_button = Button(window, text="Nulstil alt", width=10, command=partial(reset_all, "full"))
reset_button.bind("<Return>", lambda event: reset_all("full"))

no_of_trucks_label = Label(window, text=f"Biler i alt: 0")

next_button = Button(window, text="Næste bil", width=15, command=partial(draw_another_truck, "Next"), state=DISABLED)
next_button.bind("<Return>", lambda event: draw_another_truck("Next"))
previous_button = Button(window, text="Forrige bil", width=15,
                         command=partial(draw_another_truck, "Previous"), state=DISABLED)
previous_button.bind("<Return>", lambda event: draw_another_truck("Previous"))

truck_canvas = Canvas(window, width=230, height=539, highlightthickness=0)
leftovers_canvas = Canvas(window, width=158, height=539, highlightthickness=0)

label_truck = Label(window, text="N/A", width=13, font=("", "13"))
label_leftovers = Label(window, text="N/A", width=13, font=("", "13"))

label_pallets_ldm = Label(window, text="N/A", width=13)
label_leftovers_ldm = Label(window, text="N/A", width=13)

text_output = scrolledtext.ScrolledText(window, width=74, height=11, font=("Courier", "9"))
text_output.insert("end", "Klar.")
text_output.config(state=DISABLED)

# Placement of GUI elements

entry_frame.place(x=4, y=32)
start_button.place(x=34, y=201)
progress_bar.place(x=16, y=244)
status_label.place(x=16, y=274)
target_ldm_frame.place(x=4, y=320)
reset_button.place(x=34, y=385)
no_of_trucks_label.place(x=16, y=468)
next_button.place(x=16, y=508)
previous_button.place(x=16, y=548)

label_truck.place(x=136, y=8)
label_leftovers.place(x=378, y=8)
truck_canvas.place(x=148, y=34)
leftovers_canvas.place(x=390, y=34)
label_pallets_ldm.place(x=148, y=575)
label_leftovers_ldm.place(x=392, y=575)

text_output.place(x=16, y=602)

# Draws empty truck rectangles
draw_truck_rectangle(truck_canvas)
draw_truck_rectangle(leftovers_canvas)

# Sets initial focus to the first entry box
entry_boxes[entry_focus].focus_set()

window.mainloop()
