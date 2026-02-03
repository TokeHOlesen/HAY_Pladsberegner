# Optimized for Python 3.11
# ver. 0.9.1.9b / 06-sep-2023

import sys
from tkinter import *
from tkinter import ttk, scrolledtext, messagebox
from tkinter.filedialog import asksaveasfile
from functools import partial
from threading import Thread
from os import path, startfile, remove
from PyQt6.QtWidgets import QApplication

from constants import *
from load_calculator import calculate_load
from pdf_generator import generate_pdf


max_truck_ldm = DEFAULT_MAX_TRUCK_LDM

calc_result = None
trucks = []
truck_to_draw = 0
brush_position = 0
number_of_trucks = 0
number_of_pallets_by_truck = []
ldm_by_truck = []
ldm_of_leftovers = 0
entry_focus = 0
loose_pallet_count = 0


# Moves focus to the next entry box or the Start button (runs when Enter is pressed)
def move_focus(key):
    global entry_focus

    if str(window.focus_get()) == ".!frame.!entry":
        entry_focus = 0
    else:
        entry_focus = int(str(window.focus_get())[-1]) - 1

    if key == "Return" or key == "DownArrow":
        if entry_focus < len(entry_boxes) - 1:
            entry_focus += 1
            entry_boxes[entry_focus].focus_set()
        elif entry_focus == len(entry_boxes) - 1 and key == "Return":
            entry_focus = 0
            start_button.focus_set()
    elif key == "UpArrow":
        if entry_focus > 0:
            entry_focus -= 1
            entry_boxes[entry_focus].focus_set()


# Resets global values
# When "full" is passed as a parameter, resets everything
# Otherwise leaves contents of entry boxes, max_target_ldm and text_output intact - useful when recalculating
def reset_all(mode):
    global loose_pallet_count
    global trucks
    global truck_to_draw
    global brush_position
    global number_of_trucks
    global number_of_pallets_by_truck
    global ldm_by_truck
    global max_truck_ldm
    global ldm_of_leftovers
    global entry_focus
    loose_pallet_count = 0
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

    text_output.config(state=NORMAL)
    text_output.delete('1.0', END)
    text_output.insert("end", "Klar.")
    text_output.config(state=DISABLED)

    copy_text_button.config(state=DISABLED)
    print_text_button.config(state=DISABLED)
    save_text_button.config(state=DISABLED)
    save_pdf_button.config(state=DISABLED)

    if mode == "full":
        for entry in entry_boxes:
            entry.delete(0, END)

        reset_button.config(state=DISABLED)

        max_truck_ldm = DEFAULT_MAX_TRUCK_LDM
        entry_ldm.delete(0, END)
        entry_ldm.insert(0, str(max_truck_ldm / 100))

        status_label.config(text="Klar.")


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
        max_truck_ldm = DEFAULT_MAX_TRUCK_LDM
    entry_ldm.delete(0, END)
    entry_ldm.insert(0, str(max_truck_ldm / 100))


# Runs the main function in a separate thread
# The thread is declared as a daemon to make sure it is terminated when the main window closes for any reason
def threaded_calculate_pallets(_):  # CHECK - Irrelevant
    thread = Thread(target=calculate_pallets, daemon=True)
    thread.start()


# Main function
def calculate_pallets():
    global truck_to_draw
    global calc_result
    global brush_position

    if calc_result is not None:
        if calc_result.number_of_trucks > 0 or calc_result.number_of_loose_pallets > 0:
            reset_all("partial")

    # COLLECT INPUT START

    # Collects number of pallets from entry boxes
    pallet_input = [0, 0, 0, 0, 0, 0, 0]

    for b in range(len(entry_boxes)):
        if entry_boxes[b].get() != "":
            if entry_boxes[b].get().isnumeric() and int(entry_boxes[b].get()) >= 0:
                pallet_input[b] = int(entry_boxes[b].get())
            else:
                messagebox.showwarning("Fejl", "Ugyldigt antal.")
                return

    # Displays a warning messagebox if entry boxes are empty or not filled out properly
    # If show_empty_warning is False, shows a message that the data is incorrect instead
    if pallet_input == [0, 0, 0, 0, 0, 0, 0]:
        messagebox.showwarning("Mangler input", "Indtast antal paller.")
        return

    # SET TARGET LDM START
    # Sets max ldm per truck
    set_target_ldm(entry_ldm.get())

    status_label.config(text="Arbejder...")
    calc_result = calculate_load(pallet_input, max_ldm=max_truck_ldm)
    status_label.config(text="Færdig.")

    # Data processing begins here
    start_button.config(state=DISABLED)
    text_output.config(state=NORMAL)


    # Text output of truck contents

    for tr_no, truck in enumerate(calc_result.trucks):
        text_output.insert("end", f"\n\nBil {tr_no + 1}:\n")
        if truck.description_lines:
            for line in truck.description_lines:
                text_output.insert("end", line)
                text_output.insert("end", "\n")
            text_output.insert("end", f"{truck.arrangements_ldm / 100} ldm i grupper ({truck.number_of_pallets} paller).")
        else:
            text_output.insert("end", "Rester.")

    # Text output of remaining pallets

    text_output.insert("end", "\n\nRest:")
    if calc_result.number_of_loose_pallets > 0:
        for pallet in calc_result.loose_pallet_count:
            text_output.insert("end", f"\n{PALLET_FORMATTED_OUTPUT[pallet]}: x {calc_result.loose_pallet_count[pallet]}")
        text_output.insert("end", f"\nI alt rester: {calc_result.loose_pallets_ldm / 100} ldm.")
    else:
        text_output.insert("end", "\nIngen.")

    # Text summary
    text_output.insert(
        "end", f"\n\nI alt: {calc_result.arrangements_ldm / 100} ldm i grupper + "
               f"{calc_result.loose_pallets_ldm / 100} ldm rest = "
               f"{(calc_result.arrangements_ldm + calc_result.loose_pallets_ldm) / 100} ldm ({calc_result.number_of_pallets + calc_result.number_of_loose_pallets} paller).")
    text_output.insert("end", f"\nSkal hentes af {calc_result.number_of_trucks} biler.")

    text_output.insert("end", "\n\nFærdig.")
    text_output.see("end")
    text_output.config(state=DISABLED)

    # Draws truck contents and leftovers; adjusts UI elements
    if calc_result.number_of_trucks > 0:
        draw_truck(calc_result.trucks[truck_to_draw])

    if calc_result.number_of_trucks > 1:
        next_button.config(state=NORMAL)

    copy_text_button.config(state=NORMAL)
    print_text_button.config(state=NORMAL)
    save_text_button.config(state=NORMAL)
    save_pdf_button.config(state=NORMAL)

    if calc_result.number_of_loose_pallets > 0:
        brush_position = 20
        unique_leftover_pallets = [*set(calc_result.loose_pallets)]
        unique_leftover_pallets.sort()
        for pallet in unique_leftover_pallets:
            draw_leftovers(pallet, leftovers_canvas, "normal")
        label_leftovers_ldm.config(text=f"{calc_result.number_of_loose_pallets} pll, ~{round(calc_result.loose_pallets_ldm / 100, 1)} ldm")
    else:
        draw_leftovers("", leftovers_canvas, "none")

    no_of_trucks_label.config(text=f"Biler i alt: {calc_result.number_of_trucks}")

    if calc_result.number_of_trucks > 0:
        label_pallets_ldm.config(text=f"{calc_result.trucks[truck_to_draw].number_of_pallets} pll, {round(calc_result.trucks[truck_to_draw].arrangements_ldm / 100, 1)} ldm")

    start_button.config(state=NORMAL)
    reset_button.config(state=NORMAL)
    entry_boxes[0].focus_set()


# Draws an empty white rectangle for use as a background for truck contents or leftovers
def draw_truck_rectangle(canvas):
    canvas.create_rectangle(0, 0, 98, 538, fill="#ffffff")


# Draws the contents of a given truck on truck_canvas
def draw_truck(truck_to_be_drawn):
    if truck_to_be_drawn.arrangements_ldm > 0:
        for this_arrangement in truck_to_be_drawn.arrangements:
            draw_arrangement(this_arrangement, truck_canvas)
        label_truck.config(text=f"Bil {truck_to_draw + 1}")
    else:
        label_truck.config(text=f"Bil {truck_to_draw + 1}")
        truck_canvas.create_text(48, 255, text="Rester", font=("", "13"))


# Draws the contents of the next or the previous truck, depending on which button has been pressed
def draw_another_truck(direction):
    global truck_to_draw
    global brush_position
    brush_position = 0

    truck_canvas.delete("all")
    draw_truck_rectangle(truck_canvas)

    if direction == "Next":
        if len(calc_result.trucks) - 1 > truck_to_draw:
            truck_to_draw += 1
        draw_truck(calc_result.trucks[truck_to_draw])
        if truck_to_draw > 0:
            previous_button.config(state=NORMAL)
        if len(calc_result.trucks) - 1 == truck_to_draw:
            next_button.config(state=DISABLED)

    elif direction == "Previous":
        if not truck_to_draw == 0:
            truck_to_draw -= 1
        draw_truck(calc_result.trucks[truck_to_draw])
        if truck_to_draw == 0:
            previous_button.config(state=DISABLED)
        if len(calc_result.trucks) - 1 > truck_to_draw:
            next_button.config(state=NORMAL)

    if calc_result.trucks[truck_to_draw]:
        label_pallets_ldm.config(
            text=f"{calc_result.trucks[truck_to_draw].number_of_pallets} pll, {round(calc_result.trucks[truck_to_draw].arrangements_ldm / 100, 1)} ldm")
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
        canvas.create_rectangle(0 + 2, y + 2, 32, y2 - 1, fill=PALLET_COLORS["120"])
        canvas.create_rectangle(32 + 2, y + 2, 64, y2 - 1, fill=PALLET_COLORS["120"])
        canvas.create_rectangle(64 + 2, y + 2, 96, y2 - 1, fill=PALLET_COLORS["120"])
        draw_bracket(y, y2)
        draw_description(16, "120x80 x 3")
        draw_description(31, "1,2 ldm")
        brush_position += 48 - 1
    elif arrangement == (120, 120):
        y2 = y + 32
        canvas.create_rectangle(0 + 2, y + 2, 48, y2 - 1, fill=PALLET_COLORS["120"])
        canvas.create_rectangle(48 + 2, y + 2, 96, y2 - 1, fill=PALLET_COLORS["120"])
        draw_bracket(y, y2)
        draw_description(17, "120x80 x 2, 0,8 ldm")
        brush_position += 32 - 1
    elif arrangement == (145, 145, 145):
        y2 = y + 59
        canvas.create_rectangle(0 + 2, y + 2, 32, y2 - 1, fill=PALLET_COLORS["145"])
        canvas.create_rectangle(32 + 2, y + 2, 64, y2 - 1, fill=PALLET_COLORS["145"])
        canvas.create_rectangle(64 + 2, y + 2, 96, y2 - 1, fill=PALLET_COLORS["145"])
        draw_bracket(y, y2)
        draw_description(22, "145x80 x 3")
        draw_description(37, "1,5 ldm")
        brush_position += 59 - 1
    elif arrangement == (17080, 17080, 17080):
        y2 = y + 68
        canvas.create_rectangle(0 + 2, y + 2, 32, y2 - 1, fill=PALLET_COLORS["17080"])
        canvas.create_rectangle(32 + 2, y + 2, 64, y2 - 1, fill=PALLET_COLORS["17080"])
        canvas.create_rectangle(64 + 2, y + 2, 96, y2 - 1, fill=PALLET_COLORS["17080"])
        draw_bracket(y, y2)
        draw_description(24, "170x80 x 3")
        draw_description(39, "1,7 ldm")
        brush_position += 68 - 1
    elif arrangement == (130, 130):
        y2 = y + 56
        canvas.create_rectangle(0 + 2, y + 2, 48, y2 - 1, fill=PALLET_COLORS["130"])
        canvas.create_rectangle(48 + 2, y + 2, 96, y2 - 1, fill=PALLET_COLORS["130"])
        draw_bracket(y, y2)
        draw_description(20, "130x115 x 2")
        draw_description(35, "1,4 ldm")
        brush_position += 56 - 1
    elif arrangement == (60, 60, 60):
        y2 = y + 24
        canvas.create_rectangle(0 + 2, y + 2, 32, y2 - 1, fill=PALLET_COLORS["60"])
        canvas.create_rectangle(32 + 2, y + 2, 64, y2 - 1, fill=PALLET_COLORS["60"])
        canvas.create_rectangle(64 + 2, y + 2, 96, y2 - 1, fill=PALLET_COLORS["60"])
        draw_bracket(y, y2)
        draw_description(13, "60x80 x 3, 0,6 ldm")
        brush_position += 24 - 1
    elif arrangement == (120, 120, 60, 60):
        y2 = y + 48
        canvas.create_rectangle(0 + 2, y + 2, 32, y2 - 1, fill=PALLET_COLORS["120"])
        canvas.create_rectangle(32 + 2, y + 2, 64, y2 - 1, fill=PALLET_COLORS["120"])
        canvas.create_rectangle(64 + 2, y + 2, 96, y2 - 24 - 1, fill=PALLET_COLORS["60"])
        canvas.create_rectangle(64 + 2, y + 24 + 1, 96, y2 - 1, fill=PALLET_COLORS["60"])
        draw_bracket(y, y2)
        draw_description(10, "120x80 x 2")
        draw_description(25, "60x80 x 2")
        draw_description(40, "1,2 ldm")
        brush_position += 48 - 1
    elif arrangement == (120, 60, 60, 60, 60):
        y2 = y + 48
        canvas.create_rectangle(0 + 2, y + 2, 32, y2 - 1, fill=PALLET_COLORS["120"])
        canvas.create_rectangle(32 + 2, y + 2, 64, y2 - 24 - 1, fill=PALLET_COLORS["60"])
        canvas.create_rectangle(32 + 2, y + 24 + 1, 64, y2 - 1, fill=PALLET_COLORS["60"])
        canvas.create_rectangle(64 + 2, y + 2, 96, y2 - 24 - 1, fill=PALLET_COLORS["60"])
        canvas.create_rectangle(64 + 2, y + 24 + 1, 96, y2 - 1, fill=PALLET_COLORS["60"])
        draw_bracket(y, y2)
        draw_description(10, "120x80 x 1")
        draw_description(25, "60x80 x 4")
        draw_description(40, "1,2 ldm")
        brush_position += 48 - 1
    elif arrangement == (17090, 145, 145):
        y2 = y + 68
        canvas.create_rectangle(0 + 2, y + 2, 36, y2 - 1, fill=PALLET_COLORS["17090"])
        canvas.create_rectangle(36 + 2, y + 2, 96, y2 - 36 - 1, fill=PALLET_COLORS["145"])
        canvas.create_rectangle(36 + 2, y + 32 + 1, 96, y2 - 4 - 1, fill=PALLET_COLORS["145"])
        draw_bracket(y, y2)
        draw_description(18, "170x90 x 1")
        draw_description(33, "145x80 x 2")
        draw_description(48, "1,7 ldm")
        brush_position += 68 - 1
    elif arrangement == (17090, 17090, 130, 130, 130):
        y2 = y + 68
        y3 = y + 45
        canvas.create_rectangle(0 + 2, y + 2, 36, y2 - 1, fill=PALLET_COLORS["17090"])
        canvas.create_rectangle(0 + 2, y + 68 + 1, 36, y2 + 67 - 1, fill=PALLET_COLORS["17090"])
        canvas.create_rectangle(36 + 2, y + 2, 96, y3, fill=PALLET_COLORS["130"])
        canvas.create_rectangle(36 + 2, y + 45 + 2, 96, y3 + 45 - 1, fill=PALLET_COLORS["130"])
        canvas.create_rectangle(36 + 2, y + 90 + 1, 96, y3 + 90 - 1, fill=PALLET_COLORS["130"])
        draw_bracket(y, y2 + 67)
        draw_description(50, "170x90 x 2")
        draw_description(65, "130x115 x 3")
        draw_description(80, "3,4 ldm")
        brush_position += 135 - 1
    elif arrangement == (17080, 17080, 120, 60):
        y2 = y + 68
        canvas.create_rectangle(0 + 2, y + 2, 32, y2 - 1, fill=PALLET_COLORS["17080"])
        canvas.create_rectangle(32 + 2, y + 2, 64, y2 - 1, fill=PALLET_COLORS["17080"])
        canvas.create_rectangle(64 + 2, y + 2, 96, y2 - 24 - 1, fill=PALLET_COLORS["120"])
        canvas.create_rectangle(64 + 2, y + 44 + 1, 96, y2 - 1, fill=PALLET_COLORS["60"])
        draw_bracket(y, y2)
        draw_description(12, "170x80 x 2")
        draw_description(27, "120x80 x 1")
        draw_description(42, "60x80 x 1")
        draw_description(57, "1,7 ldm")
        brush_position += 68 - 1
    elif arrangement == (17080, 120, 120, 60, 60):
        y2 = y + 68
        canvas.create_rectangle(0 + 2, y + 2, 32, y2 - 1, fill=PALLET_COLORS["17080"])
        canvas.create_rectangle(32 + 2, y + 2, 64, y2 - 24 - 1, fill=PALLET_COLORS["120"])
        canvas.create_rectangle(64 + 2, y + 2, 96, y2 - 24 - 1, fill=PALLET_COLORS["120"])
        canvas.create_rectangle(32 + 2, y + 44 + 1, 64, y2 - 1, fill=PALLET_COLORS["60"])
        canvas.create_rectangle(64 + 2, y + 44 + 1, 96, y2 - 1, fill=PALLET_COLORS["60"])
        draw_bracket(y, y2)
        draw_description(12, "170x80 x 2")
        draw_description(27, "120x80 x 3")
        draw_description(42, "60x80 x 3")
        draw_description(57, "1,7 ldm")
        brush_position += 68 - 1
    elif arrangement == (17080, 60):
        y2 = y + 32
        canvas.create_rectangle(0 + 2, y + 2, 68, y2 - 1, fill=PALLET_COLORS["17080"])
        canvas.create_rectangle(69 + 2, y + 2, 94, y2 - 1, fill=PALLET_COLORS["60"])
        draw_bracket(y, y2)
        draw_description(10, "170x80 x 1, 60x80 x 1")
        draw_description(25, "0,8 ldm")
        brush_position += 32 - 1
    elif arrangement == (17090, 60):
        y2 = y + 36
        canvas.create_rectangle(0 + 2, y + 2, 68, y2 - 1, fill=PALLET_COLORS["17090"])
        canvas.create_rectangle(69 + 2, y + 2, 94, y2 - 4 - 1, fill=PALLET_COLORS["60"])
        draw_bracket(y, y2)
        draw_description(10, "170x90 x 1, 60x80 x 1")
        draw_description(25, "0,9 ldm")
        brush_position += 36 - 1
    elif arrangement == (130, 120, 120):
        y2 = y + 64
        canvas.create_rectangle(0 + 2, y + 2, 48, y2 - 8 - 1, fill=PALLET_COLORS["130"])
        canvas.create_rectangle(48 + 2, y + 2, 96, y2 - 32 - 1, fill=PALLET_COLORS["120"])
        canvas.create_rectangle(48 + 2, y + 32 + 1, 96, y2 - 1, fill=PALLET_COLORS["120"])
        draw_bracket(y, y2)
        draw_description(16, "130x115 x 1")
        draw_description(31, "120x80 x 2")
        draw_description(46, "1,6 ldm")
        brush_position += 64 - 1
    elif arrangement == (23090,):
        y2 = y + 36
        canvas.create_rectangle(0 + 2, y + 2, 96, y2 - 1, fill=PALLET_COLORS["23090"])
        draw_bracket(y, y2)
        draw_description(10, "230x90 x 1")
        draw_description(25, "0,9 ldm")
        brush_position += 36 - 1


# Draws a representation of leftover pallets and their description on leftover_canvas
# If the "mode" parameter equals "normal", draws pallets; if "none", draws a message that there's nothing to show
def draw_leftovers(pallet, canvas, mode):
    global brush_position

    if mode == "normal":
        label_leftovers.config(text=f"Rester")
        y = brush_position

        def draw_number_of_leftovers(yy, pallet_type):
            canvas.create_text(70, y + yy, text=f"x{calc_result.loose_pallet_count[pallet_type]}", font=("", "13"), anchor="w")

        def draw_description(yy, text, pallet_type):
            canvas.create_text(115, y + yy, text=text, font=("", "8"), anchor="w")
            canvas.create_text(115, y + yy + 15, text=f"{calc_result.loose_pallet_count[pallet_type]} stk", font=("", "8"), anchor="w")

        if pallet == 60:
            y2 = y + 24
            canvas.create_rectangle(12 + 2, y + 2, 44, y2 - 1, fill=PALLET_COLORS["60"])
            draw_number_of_leftovers(12, 60)
            draw_description(5, "60x80", 60)
            brush_position += 54 - 1
        elif pallet == 120:
            y2 = y + 48
            canvas.create_rectangle(12 + 2, y + 2, 44, y2 - 1, fill=PALLET_COLORS["120"])
            draw_number_of_leftovers(24, 120)
            draw_description(18, "120x80", 120)
            brush_position += 78 - 1
        elif pallet == 145:
            y2 = y + 60
            canvas.create_rectangle(12 + 2, y + 2, 44, y2 - 1, fill=PALLET_COLORS["145"])
            draw_number_of_leftovers(30, 145)
            draw_description(22, "145x80", 145)
            brush_position += 90 - 1
        elif pallet == 130:
            y2 = y + 56
            canvas.create_rectangle(12 + 2, y + 2, 60, y2 - 1, fill=PALLET_COLORS["130"])
            draw_number_of_leftovers(28, 130)
            draw_description(21, "130x115", 130)
            brush_position += 86 - 1
        elif pallet == 17080:
            y2 = y + 68
            canvas.create_rectangle(12 + 2, y + 2, 44, y2 - 1, fill=PALLET_COLORS["17080"])
            draw_number_of_leftovers(34, 17080)
            draw_description(28, "170x80", 17080)
            brush_position += 98 - 1
        elif pallet == 17090:
            y2 = y + 68
            canvas.create_rectangle(12 + 2, y + 2, 48, y2 - 1, fill=PALLET_COLORS["17090"])
            draw_number_of_leftovers(34, 17090)
            draw_description(28, "170x90", 17090)
            brush_position += 98 - 1
    elif mode == "none":
        canvas.create_text(48, 255, text="Ingen rest", font=("", "13"))


def copy_text_output():
    window.clipboard_clear()
    window.clipboard_append(text_output.get(6.0, "end-10c"))
    window.update()


def print_text_output():
    if path.isfile("HAY Pladsberegner.txt"):
        remove("HAY Pladsberegner.txt")

    temp_text_file = open("HAY Pladsberegner.txt", "x")
    temp_text_file.write(text_output.get(6.0, "end-10c"))
    temp_text_file.close()
    startfile(temp_text_file.name, "print")


def save_text_output():
    text_file = asksaveasfile(defaultextension=".txt", filetypes=[("Tekstdokumenter", "*.txt"), ("Alle filer", "*.*")])
    if text_file is None:
        return
    with open(text_file.name, "w") as t_f:
        t_f.write(text_output.get(6.0, "end-10c"))


def save_pdf_file():
    pdf_path = asksaveasfile(defaultextension=".pdf", filetypes=[("Portable Document Format", "*.pdf"), ("Alle filer", "*.*")])
    pdf_title = pdf_path.name.split("/")[-1][:-4]
    dummy_app = QApplication(sys.argv)
    generate_pdf(calc_result, pdf_title, pdf_path.name)


def ask_if_really_quit():
    quit_response = messagebox.askyesno("HAY Pladsberegner", "Skal programmet lukkes?")
    if quit_response:
        window.destroy()


# GUI starts here

window = Tk()
window.title("HAY Pladsberegner 0.9.1.9b")
window.geometry("572x820+256+64")
window.resizable(False, False)
window.protocol('WM_DELETE_WINDOW', ask_if_really_quit)

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
    "230x90:    "
]

entry_labels = []

for k in range(7):
    entry_label = Label(entry_frame, width=10, anchor="e", text=entry_label_text[k])
    entry_labels.append(entry_label)

for k in range(7):
    entry_labels[k].grid(row=k, column=0, pady=2)

entry_boxes = []

for e in range(7):
    entry_box = Entry(entry_frame, width=7, justify=RIGHT)
    entry_boxes.append(entry_box)
    entry_boxes[e].bind("<Return>", lambda event: move_focus("Return"))
    entry_boxes[e].bind("<Up>", lambda event: move_focus("UpArrow"))
    entry_boxes[e].bind("<Down>", lambda event: move_focus("DownArrow"))

for e in range(7):
    entry_boxes[e].grid(row=e, column=1, pady=2)

# Other GUI elements - self-explanatory

start_button = Button(window, text="Start", width=10, command=partial(threaded_calculate_pallets, "Null"))
start_button.bind("<Return>", threaded_calculate_pallets)

status_label = Label(window, text="Klar.")

target_ldm_frame = Frame(window)

enter_ldm_label = Label(target_ldm_frame, width=10, anchor="e", text="Max ldm:  ")
enter_ldm_label.grid(row=0, column=0, pady=2)

entry_ldm = Entry(target_ldm_frame, width=7, justify=RIGHT)
entry_ldm.insert(0, str(max_truck_ldm / 100))
entry_ldm.grid(row=0, column=1, pady=2)

reset_button = Button(window, text="Nulstil alt", width=10, command=partial(reset_all, "full"), state=DISABLED)
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

copy_text_button = Button(window, text="Kopiér", width=10, state=DISABLED, command=copy_text_output)
print_text_button = Button(window, text="Print", width=10, state=DISABLED, command=print_text_output)
save_text_button = Button(window, text="Gem", width=10, state=DISABLED, command=save_text_output)
save_pdf_button = Button(window, text="Gem PDF", width=10, state=DISABLED, command=save_pdf_file)

# Placement of GUI elements

entry_frame.place(x=4, y=32)
start_button.place(x=34, y=232)
status_label.place(x=16, y=280)
target_ldm_frame.place(x=4, y=355)
reset_button.place(x=34, y=405)
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

copy_text_button.place(x=16, y=782)
print_text_button.place(x=108, y=782)
save_text_button.place(x=200, y=782)
save_pdf_button.place(x=292, y=782)

# Draws empty truck rectangles
draw_truck_rectangle(truck_canvas)
draw_truck_rectangle(leftovers_canvas)

# Sets initial focus to the first entry box
entry_boxes[entry_focus].focus_set()

window.mainloop()
