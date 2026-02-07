import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
import textwrap
import time
from PIL import ImageTk, Image
import services
from location_ids import Location
from locations_data import LOCATIONS
from objects_data import OBJECT_DEFS
from objects_builder import build_objects

class GameState:
    def __init__(self):
        # Location and game flow
        self.current_location = Location.CELL_1
        self.end_of_game = False
        self.playing = False

        # Object state flags
        self.object_flags = {
            "door_open": False,
            "safe_open": False,
            "trapdoor_open": False,
            "fire_lit": False,
            "benny_dead": False,
            "broom_destroyed": False,
            "fire_extinguished": False,
            "three_pieces_solved": False
        }

        # Refresh flags
        self.refresh_location = True
        self.refresh_objects_visible = True

        # Inventory
        self.inventory = []

        # Game objects
        self.objects = build_objects(OBJECT_DEFS)
        self.game_objects = list(self.objects.values())

    # Helper methods
    def get_object(self, name):
        """Return the object by name (case-insensitive)."""
        name = name.upper()
        for obj in self.game_objects:
            if obj.name.upper() == name:
                return obj
        return None

    def is_carried(self, obj):
        return getattr(obj, "carried", False)

    def set_flag(self, flag_name, value=True):
        if flag_name in self.object_flags:
            self.object_flags[flag_name] = value

    def get_flag(self, flag_name):
        return self.object_flags.get(flag_name, False)

    def add_to_inventory(self, obj):
        if obj not in self.inventory:
            self.inventory.append(obj)
            obj.carried = True
            obj.visible = False

    def remove_from_inventory(self, obj):
        if obj in self.inventory:
            self.inventory.remove(obj)
            obj.carried = False
            obj.visible = True

    def has_in_inventory(self, obj_or_name):
        if isinstance(obj_or_name, str):
            return any(o.name.upper() == obj_or_name.upper() for o in self.inventory)
        return obj_or_name in self.inventory

    # --- Object & Puzzle Logic ---

    def update_visibility(self):
        """Update object visibility based on carried items, puzzle progression, and flags."""

        # Puzzle piece chain progression
        if self.has_in_inventory("PUZZLE_PIECE_1") and self.get_object("puzzle").carried:
            self.get_object("hint1").visible = True
        if self.get_object("hint1").carried:
            self.get_object("clue1").visible = True
        if self.get_object("clue1").carried:
            self.get_object("clue11").visible = True
        if self.get_object("clue11").carried:
            self.get_object("clue2").visible = True

        # Safe logic: second puzzle piece appears after opening safe
        if self.get_flag("safe_open") and not self.get_object("puzzle_with_two_pieces_inserted").carried:
            self.get_object("puzzle_piece_2").visible = True

        # Glue fragments
        if all(self.has_in_inventory(f"hint_fragment_{i}") for i in range(1, 14)):
            self.get_object("glue_stick").visible = True

        # Magnifying glass reveals trapdoor
        if self.get_object("hint3").carried:
            self.get_object("magnifying_glass").visible = True
        if self.get_object("magnifying_glass").carried:
            self.get_object("trapdoor").visible = True

        # Trapdoor puzzle piece
        if self.get_flag("trapdoor_open") and not self.get_object("puzzle_with_three_pieces_inserted").carried:
            self.get_object("puzzle_piece_3").visible = True

        # Fire extinguished unlocks final piece
        if self.get_flag("fire_extinguished"):
            self.get_object("puzzle_piece_4").visible = True

    def handle_special_conditions(self):
        """Check for game-over conditions or winning."""
        cause_of_death = ""

        # Fire kills Benny if bucket not used
        if self.get_flag("fire_lit") and self.current_location == 22 and not self.has_in_inventory("BUCKET_FILLED"):
            cause_of_death = "a fire."
            self.set_flag("benny_dead", True)

        # Deaths
        if self.get_flag("benny_dead"):
            print_to_description("Benny has died due to " + cause_of_death)
            print_to_description("GAME OVER")
            self.end_of_game = True

        if self.get_flag("broom_destroyed") and not self.get_flag("three_pieces_solved"):
            print_to_description("Benny can't continue to escape, as he used the broom to make a fire before using it for something else.")
            print_to_description("GAME OVER")
            self.end_of_game = True

        # Win condition
        if self.current_location == 23:
            print_to_description("You successfully helped Benny escape the castle basement! Congratulations.")
            self.end_of_game = True

    def describe_visible_objects(self):
        """Update the description widget with objects visible in the current location."""
        if not description_widget:
            return

        visible_objs = [
            obj.name for obj in self.game_objects
            if obj.visible and not obj.carried and obj.location == self.current_location
        ]

        if visible_objs:
            print_to_description("You can see here: " + ", ".join(visible_objs))



PORTRAIT_LAYOUT = True

command_widget = None
image_label = None
description_widget = None
inventory_widget = None
north_button = None
south_button = None
east_button = None
west_button = None
root = None
button_frame = None

playing = False
MAX_TIME_ELAPSED = 15

def perform_command(verb, noun):

    if verb in ["GO", "N", "S", "E", "W", "A", "D", "NORTH", "SOUTH", "EAST", "WEST"]:
        perform_go_command(verb)
    elif verb in ["GET", "TAKE", "GRAB"]:
        perform_get_command(noun)
    elif verb in ["PUT", "DROP"]:
        perform_put_command(noun)
    elif verb in ["LOOK", "INVESTIGATE"]:
        perform_look_command(noun)
    elif verb == "READ":
        perform_read_command(noun)
    elif verb == "OPEN":
        perform_open_command(noun)
    elif verb == "HELP":
        perform_help_command(noun)
    elif verb == "SOLVE":
        perform_solve_command(noun)
    elif verb == "UNLOCK":
        perform_unlock_command(noun)
    elif verb == "DECIPHER":
        perform_decipher_command(noun)
    elif verb == "GLUE":
        perform_glue_command(noun)
    elif verb == "USE":
        perform_use_command(noun)
    elif verb == "FILL":
        perform_fill_command(noun)
    else:
        print_to_description("unknown command")

def perform_go_command(direction):
    mappings = {
        "N": get_location_to_north,
        "NORTH": get_location_to_north,
        "S": get_location_to_south,
        "SOUTH": get_location_to_south,
        "E": get_location_to_east,
        "EAST": get_location_to_east,
        "W": get_location_to_west,
        "WEST": get_location_to_west,
    }

    func = mappings.get(direction)
    if func:
        new_location = func(state.current_location)
        if new_location == 0:
            print_to_description("You can't go that way!")
        else:
            state.current_location = new_location
            state.refresh_location = True

def perform_get_command(obj_name):
    obj = state.get_object(obj_name)
    if not obj:
        print_to_description("You don't see one of those here!")
        return
    if obj.location != state.current_location or not obj.visible:
        print_to_description("You don't see one of those here!")
        return
    if not getattr(obj, "movable", False):
        print_to_description("You can't pick it up!")
        return
    if obj.carried:
        print_to_description("You are already carrying it")
        return
    state.add_to_inventory(obj)
    state.refresh_objects_visible = True

def perform_put_command(obj_name):
    obj = state.get_object(obj_name)
    if not obj:
        print_to_description("You are not carrying one of those!")
        return
    if not obj.carried:
        print_to_description("You are not carrying one of those!")
        return
    state.remove_from_inventory(obj)
    obj.location = state.current_location
    state.refresh_objects_visible = True

def perform_look_command(obj_name):
    obj = state.get_object(obj_name)
    if obj and (obj.carried or (obj.visible and obj.location == state.current_location)):
        print_to_description(obj.description)
    else:
        print_to_description("You can't see one of those!")

def perform_read_command(object_name):
    game_object = state.get_object(object_name)

    if game_object is None:
        print_to_description(f"I am not sure which {object_name} you are referring to")
        return

    if not getattr(game_object, "carried", False):
        print_to_description("You're not carrying anything readable")
        return

    if hasattr(game_object, "on_read") and callable(game_object.on_read):
        game_object.on_read()
    else:
        print_to_description("There's nothing readable about this.")


def perform_open_command(object_name):
    game_object = state.get_object(object_name)

    if not (game_object is None):
        safe = state.get_object("safe")
        trapdoor = state.get_object("trapdoor")
        broom = state.get_object("broom")

        if game_object == safe and (game_object.visible and game_object.location == state.current_location) and state.get_flag("safe_open"):
            print_to_description("Benny pulls on the handle and the safe opens!")
            set_current_image()
            game_object.description = "a small safe, with the door wide open"
        elif game_object == trapdoor and (game_object.visible and game_object.location == state.current_location) and broom.carried:
            print_to_description("Benny pushes on the trapdoor with the end of the broom and it opens, revealing a puzzle piece.")
            state.set_flag("trapdoor_open", True)
            state.refresh_objects_visible = True
        else:
            print_to_description("You can't open one of those.")
    else:
        print_to_description("You don't see one of those here.")

list_of_commands = ["GO", "N", "S", "E", "W", "NORTH", "SOUTH", "EAST", "WEST", "GET", "READ", "OPEN", "HELP"]

def perform_help_command(_):
    print_to_description("Available commands:")
    print_to_description(", ".join(list_of_commands))

def perform_solve_command(object_name):
    global refresh_objects_visible
    global three_pieces_solved
    game_object = get_game_object(object_name)
    piece_slot_message = "The piece slots into the puzzle, but you still haven't solved it."
    if not (game_object is None):
        if game_object.carried and game_object == puzzle:
            answer = simpledialog.askstring("Input", "What would you like to put in the puzzle first?", parent=root)
            if not puzzle_piece_1.carried:
                print_to_description("It looks like you don't have anything to put into the puzzle.")
            elif answer != "puzzle piece 1":
                print_to_description("Unfortunately, it looks like it doesn't fit in the puzzle.")
            else:
                puzzle_piece_inserted = False
                while not puzzle_piece_inserted:
                    slot = simpledialog.askinteger("Input", "Which slot would you like to put your piece in?",
                                                   parent=root)
                    if slot != 1:
                        print_to_description("The piece won't fit, no matter how you rotate it.")
                        answer = simpledialog.askstring("Input", "Would you like to try again?", parent=root)
                        if answer == "No":
                            break
                    else:
                        print_to_description(piece_slot_message)
                        puzzle_piece_inserted = True
                for item in [puzzle_piece_1, hint1, clue1, clue11, clue2, game_object]:
                    item.carried = False
                    item.visible = False
                puzzle_with_one_piece_inserted.carried = True
                list_of_commands.append("DECIPHER\n")
                list_of_commands.append("SOLVE\n")
                refresh_objects_visible = True
        elif game_object.carried and game_object == puzzle_with_one_piece_inserted:
            answer = simpledialog.askstring("Input", "What would you like to put in the puzzle next?", parent=root)
            if not puzzle_piece_2.carried:
                print_to_description("It looks like you don't have anything to put into the puzzle.")
            elif answer != "puzzle piece 2":
                print_to_description("Unfortunately, it looks like it doesn't fit in the puzzle.")
            else:
                puzzle_piece_inserted = False
                while not puzzle_piece_inserted:
                    slot = simpledialog.askinteger("Input", "Which slot would you like to put your piece in?",
                                                   parent=root)
                    if slot != 2:
                        print_to_description("The piece won't fit, no matter how you rotate it.")
                        answer = simpledialog.askstring("Input", "Would you like to try again?", parent=root)
                        if answer == "No":
                            break
                    else:
                        print_to_description(piece_slot_message)
                        puzzle_piece_inserted = True
                    for item in [puzzle_piece_2, game_object, gold_bar, bar_clue]:
                        item.carried = False
                        item.visible = False
                    puzzle_with_two_pieces_inserted.carried = True
                    list_of_commands.append("UNLOCK\n")
                    refresh_objects_visible = True
        elif game_object.carried and game_object == puzzle_with_two_pieces_inserted:
            answer = simpledialog.askstring("Input", "What would you like to put in the puzzle next?", parent=root)
            if not puzzle_piece_3.carried:
                print_to_description("It looks like you don't have anything to put into the puzzle.")
            elif answer != "puzzle piece 3":
                print_to_description("Unfortunately, it looks like it doesn't fit in the puzzle.")
            else:
                puzzle_piece_inserted = False
                while not puzzle_piece_inserted:
                    slot = simpledialog.askinteger("Input", "Which slot would you like to put your piece in?",
                                                   parent=root)
                    if slot != 3:
                        print_to_description("The piece won't fit, no matter how you rotate it.")
                        answer = simpledialog.askstring("Input", "Would you like to try again?", parent=root)
                        if answer == "No":
                            break
                    else:
                        print_to_description(piece_slot_message)
                        puzzle_piece_inserted = True
                    for item in [game_object, puzzle_piece_3, hint3, fragment_clue, magnifying_glass]:
                        item.carried = False
                        item.visible = False
                    puzzle_with_three_pieces_inserted.carried = True
                    three_pieces_solved = True
                    refresh_objects_visible = True
        elif game_object.carried and game_object == puzzle_with_three_pieces_inserted:
            answer = simpledialog.askstring("Input", "What would you like to put in the puzzle next?", parent=root)
            if not puzzle_piece_4.carried:
                print_to_description("It looks like you don't have anything to put into the puzzle.")
            elif answer != "puzzle piece 4":
                print_to_description("Unfortunately, it looks like it doesn't fit in the puzzle.")
            else:
                puzzle_piece_inserted = False
                while not puzzle_piece_inserted:
                    slot = simpledialog.askinteger("Input", "Which slot would you like to put your piece in?",
                                                   parent=root)
                    if slot != 4:
                        print_to_description("The piece won't fit, no matter how you rotate it.")
                        answer = simpledialog.askstring("Input", "Would you like to try again?", parent=root)
                        if answer == "No":
                            break
                    else:
                        print_to_description(piece_slot_message)
                        puzzle_piece_inserted = True
                for item in [game_object, puzzle_piece_4, bucket_filled, lighter]:
                    item.carried = False
                    item.visible = False
                print_to_description("Benny watches as the puzzle transforms into a key. He can finally escape!!!")
                key.carried = True
                refresh_objects_visible = True
        else:
            print_to_description("You're missing something.")
    else:
        print_to_description("You can't do that.")

def perform_glue_command(object_name):
    game_object = get_game_object(object_name)
    if not (game_object is None):
        if glue_stick.carried:
            if all(item.carried for item in [game_object, hint_fragment_1, hint_fragment_2, hint_fragment_3, hint_fragment_4, hint_fragment_5, hint_fragment_6, hint_fragment_7, hint_fragment_8, hint_fragment_9, hint_fragment_10, hint_fragment_11, hint_fragment_12, hint_fragment_13]) and game_object.glueable:
                print_to_description("Benny succeeds at gluing the fragments of this hint together. Maybe it will be a bit easier to decipher now?")
                for item in [game_object, hint_fragment_1, hint_fragment_2, hint_fragment_3, hint_fragment_4, hint_fragment_5, hint_fragment_6, hint_fragment_7, hint_fragment_8, hint_fragment_9, hint_fragment_10, hint_fragment_11, hint_fragment_12, hint_fragment_13]:
                    item.carried = False
                    item.visible = False
                hint3.carried = True
        else:
            print_to_description("You're missing something.")
    else:
        print_to_description("You can't do that.")

def perform_unlock_command(object_name):
    global safe_open
    global refresh_objects_visible
    global door_open
    game_object = get_game_object(object_name)
    if not (game_object is None):
        if game_object == safe and (game_object.visible and game_object.location == current_location):
            while not safe_open:
                code = simpledialog.askinteger("Code", "What is the code to the safe?", parent=root)
                encrypted_code = str(hex(code))
                if encrypted_code != "0x3ffa":
                    print_to_description("Benny tries your code, but the safe won't open.")
                    answer = simpledialog.askstring("Input", "Would you like to try again?", parent=root)
                    if answer == "No":
                        break
                else:
                    print_to_description("The code you provided Benny with worked! The safe is now unlocked.")
                    safe_open = True
            refresh_objects_visible = True
        if game_object == door and (game_object.visible and game_object.location == current_location):
            if key.carried:
                door_open = True
                set_current_image()
            else:
                "You don't have anything to unlock the door with."
    else:
        print_to_description("There's nothing to unlock.")

def perform_decipher_command(message):
    message = message.upper()
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    deciphered_message = ""

    key = simpledialog.askinteger("Key", "What would you like to use to decipher the message?", parent=root)

    for letter in message:
        if letter in alpha:  # if the letter is actually a letter
            # find the corresponding ciphertext letter in the alphabet
            letter_index = (alpha.find(letter) - key) % len(alpha)

            deciphered_message = deciphered_message + alpha[letter_index]
        else:
            deciphered_message = deciphered_message + letter

    print_to_description("Deciphered message:")
    print_to_description(deciphered_message)

def perform_fill_command(obj_name):
    obj = state.get_object(obj_name)
    if not obj:
        print_to_description("You can't fill that!")
        return

    bucket = state.get_object("bucket")
    bucket_filled = state.get_object("bucket_filled")
    water = state.get_object("water")

    if obj == bucket and state.current_location == 22:
        print_to_description("Benny dips the bucket into the water and fills it.")
        bucket.carried = False
        bucket.visible = False
        water.visible = False
        bucket_filled.carried = True
    else:
        print_to_description("You can't fill that here, there isn't any water to fill it.")

def perform_use_command(obj_name):
    obj = state.get_object(obj_name)
    if not obj:
        print_to_description("Invalid Object.")
        return

    if obj.name.upper() == "LIGHTER":
        if state.current_location == 22:
            broom = state.get_object("broom")
            if broom.visible and broom.location == state.current_location:
                print_to_description("Benny lights the broom with the lighter and watches it burn. If he doesn't extinguish it soon, he could perish!")
                state.set_flag("fire_lit", True)
                broom.visible = False
                state.remove_from_inventory(obj)  # lighter no longer carried
                state.set_flag("broom_destroyed", True)
            else:
                print_to_description("There's nothing to light on fire.")
        else:
            print_to_description("The fire won't do anything here.")
    elif obj.name.upper() == "BUCKET_FILLED":
        if state.current_location == 22 and state.get_flag("fire_lit"):
            print_to_description("Benny throws the water onto the fire and manages to put it out. A puzzle piece is now revealed!")
            state.set_flag("fire_lit", False)
            state.set_flag("fire_extinguished", True)
            state.remove_from_inventory(obj)
            state.add_to_inventory(state.get_object("bucket"))
        else:
            print_to_description("You can't use that here.")
    else:
        print_to_description("You can't use that.")

def describe_current_location(current_location):
    data = LOCATIONS.get(current_location)

    if data:
        print_to_description(data.name)
        print_to_description(data.desc)
    else:
        print_to_description(f"Unknown location: {current_location}")

def set_current_image():
    """Update the image_label based on the current location and relevant object flags."""
    loc = state.current_location

    # Predefined static images
    static_images = {
        1: 'cell_1.tiff',
        2: 'cell_2.tiff',
        3: 'cell_3.tiff',
        4: 'hallway.tiff',
        5: 'hallway.tiff',
        6: 'right_corner.tiff',
        7: 'hallway_one_door.tiff',
        8: 'vault-1.tiff',
        9: 'vault-2.tiff',
        12: 'left_corner.png',
        13: 'hallway.tiff',
        14: 'right_corner.tiff',
        15: 'hallway.tiff',
        16: 'hallway.tiff',
        17: 'hallway.tiff',
        18: 'hallway.tiff',
        19: 'left_corner.png',
        20: 'hallway_two_doors.tiff',
        21: 'room_21.tiff',
        22: 'room_22.tiff',
        23: 'stairs.tiff'
    }

    # Start with a static default if it exists
    image_file = static_images.get(loc, 'missing.png')

    # Dynamic images based on objects or flags
    if loc == 10:  # Safe room
        safe = state.get_object("safe")
        puzzle2 = state.get_object("puzzle_piece_2")
        puzzle_inserted = state.get_object("puzzle_with_two_pieces_inserted")

        if state.get_flag("safe_open") and puzzle2.visible:
            image_file = 'safe-open.tiff'
        elif puzzle2.carried and not puzzle_inserted.carried:
            image_file = 'open-safe-no-piece.tiff'
        else:
            image_file = 'safe-closed.tiff'

    elif loc == 11:  # Vault room
        gold_bar = state.get_object("gold_bar")
        scroll_hint = state.get_object("scroll_hint")

        if gold_bar.visible and scroll_hint.visible:
            image_file = 'vault-4.tiff'
        elif gold_bar.visible:
            image_file = 'vault-4-no-hint.tiff'
        elif scroll_hint.visible:
            image_file = 'vault-4-no-bar.tiff'
        else:
            image_file = 'vault-4-no-bar-no-hint.tiff'

    # Apply the image to the label
    image_label.img = ImageTk.PhotoImage(file=f'res/images/{image_file}')
    image_label.config(image=image_label.img)

def show_popup_image(image_file):
    popup = tkinter.Toplevel(root)

    img = PhotoImage(file=f"res/images/{image_file}")

    label = tkinter.Label(popup, image=img)
    label.image = img  # Keep a reference to the image to prevent garbage collection
    label.pack()

def get_location_to_north(current_location):
    north_mappings = {
        3: 2,
        2: 1,
        6: 7,
        7: 12,
        9: 10,
        15: 14,
        16: 15,
        17: 16,
        18: 17,
        19: 18,
    }

    if current_location == 20 and door_open:
        return 23

    return north_mappings.get(current_location, 0)

def get_location_to_south(current_location):
    south_mappings = {
        1: 2,
        2: 3,
        7: 6,
        10: 9,
        12: 7,
        14: 15,
        15: 16,
        16: 17,
        17: 18,
        18: 19,
        23: 20,
    }

    return south_mappings.get(current_location, 0)

def get_location_to_east(current_location):
    east_mappings = {
        3: 4,
        4: 5,
        5: 6,
        8: 7,
        9: 8,
        10: 11,
        12: 13,
        13: 14,
        20: 19,
        21: 20,
        22: 21,
    }

    return east_mappings.get(current_location, 0)

def get_location_to_west(current_location):
    west_mappings = {
        4: 3,
        5: 4,
        6: 5,
        7: 8,
        8: 9,
        11: 10,
        13: 12,
        14: 13,
        19: 20,
        20: 21,
        21: 22,
    }

    return west_mappings.get(current_location, 0)

def describe_current_inventory():
    """Show the player's current inventory in the inventory_widget."""
    if not inventory_widget:
        return  # in case the UI isn't built yet

    if not state.inventory:
        inventory_text = "You are carrying: nothing"
    else:
        inventory_text = "You are carrying: " + ", ".join(obj.name for obj in state.inventory)

    inventory_widget.config(state="normal")
    inventory_widget.delete(1.0, END)
    inventory_widget.insert(1.0, inventory_text)
    inventory_widget.config(state="disabled")


def build_interface():
    global command_widget
    global image_label
    global description_widget
    global inventory_widget
    global north_button
    global south_button
    global east_button
    global west_button
    global root
    global button_frame

    root = Tk()
    root.resizable(True, True)
    root.bind('<Configure>', on_window_resize)  # Call on_window_resize on window resize

    style = ttk.Style()
    style.configure("BW.TLabel", foreground="black", background="white")

    image_label = ttk.Label(root)
    if PORTRAIT_LAYOUT:
        image_label.grid(row=0, column=0, columnspan=3, padx=2, pady=2)
    else:
        image_label.grid(row=0, column=0, rowspan=3, columnspan=1, padx=2, pady=2)

    description_widget = Text(root, width=60, height=10, relief=GROOVE, wrap='word')
    description_widget.insert(1.0, """After the catastrophe that was the pandemic, Benny finds himself back in dreamland, but something seems wrong. It looks like Fala and Nodo have taken him prisoner! Now he has to use all of the knowledge he’s gathered throughout all of his various adventures in the past to escape.
    
Fala and Nodo have hidden various puzzles throughout the castle basement. Can you figure them out and help Benny escape before evil takes over the kingdom? You’re the kingdom’s only hope at rescuing the protector of Dreamland.
    """)
    description_widget.insert(END, "\n")
    description_widget.config(state="disabled")
    if PORTRAIT_LAYOUT:
        description_widget.grid(row=1, column=0, columnspan=3, sticky=W, padx=2, pady=2)
    else:
        description_widget.grid(row=0, column=1, rowspan=1, columnspan=2, padx=2, pady=2)

    command_widget = ttk.Entry(root, width=(25 if PORTRAIT_LAYOUT else 54), style="BW.TLabel")
    command_widget.bind('<Return>', return_key_enter)
    if PORTRAIT_LAYOUT:
        command_widget.grid(row=2, column=0, padx=2, pady=2)
    else:
        command_widget.grid(row=1, column=1, rowspan=1, columnspan=2)

    button_frame = ttk.Frame(root)
    button_frame.config(height=150, width=150, relief=GROOVE)
    if PORTRAIT_LAYOUT:
        button_frame.grid(row=3, column=0, columnspan=1, padx=2, pady=2)
    else:
        button_frame.grid(row=2, column=1, columnspan=1, padx=2, pady=2)

    north_button = ttk.Button(button_frame, text="N", width=5)
    north_button.grid(row=0, column=1, padx=2, pady=2)
    north_button.config(command=north_button_click)

    south_button = ttk.Button(button_frame, text="S", width=5)
    south_button.grid(row=2, column=1, padx=2, pady=2)
    south_button.config(command=south_button_click)

    east_button = ttk.Button(button_frame, text="E", width=5)
    east_button.grid(row=1, column=2, padx=2, pady=2)
    east_button.config(command=east_button_click)

    west_button = ttk.Button(button_frame, text="W", width=5)
    west_button.grid(row=1, column=0, padx=2, pady=2)
    west_button.config(command=west_button_click)

    inventory_widget = Text(root, width=(30 if PORTRAIT_LAYOUT else 38), height=(8 if PORTRAIT_LAYOUT else 6),
                            relief=GROOVE, state=DISABLED)
    if PORTRAIT_LAYOUT:
        inventory_widget.grid(row=2, column=2, rowspan=2, padx=2, pady=2, sticky=W)
    else:
        inventory_widget.grid(row=2, column=2, rowspan=2, padx=2, pady=2, sticky=W)

def on_window_resize(event):
    global button_frame

    # Update the elements upon window resize
    if PORTRAIT_LAYOUT:
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=1)

        description_widget.grid(row=1, column=0, columnspan=3, sticky="nsew")
        command_widget.grid(row=2, column=0, columnspan=3, sticky="ew")

        # Adjust the button frame to span all columns, align left
        button_frame.grid(row=3, column=0, columnspan=3, padx=2, pady=2, sticky="w")
    else:
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(0, weight=1)

        description_widget.grid(row=0, column=1, rowspan=1, columnspan=2, sticky="nsew")
        command_widget.grid(row=1, column=1, rowspan=1, columnspan=2, sticky="ew")

        # Place the button frame below the text and input elements, center horizontally
        button_frame.grid(row=2, column=1, columnspan=1, padx=2, pady=10, sticky="nsew")

def set_current_state():
    """Update all UI elements to match the current game state."""
    if state.refresh_location:
        describe_current_location(state.current_location)
        set_current_image()

    if state.refresh_location or state.refresh_objects_visible:
        set_current_image()
        state.describe_visible_objects()

    state.handle_special_conditions()
    set_directions_to_move()

    if not state.end_of_game:
        describe_current_inventory()

    # Reset refresh flags
    state.refresh_location = False
    state.refresh_objects_visible = False

    # Enable or disable command input based on game state
    command_widget.config(state=("disabled" if state.end_of_game else "normal"))

def north_button_click():
    print_to_description("N", True)
    perform_command("NORTH", "")
    set_current_state()

def south_button_click():
    print_to_description("S", True)
    perform_command("SOUTH", "")
    set_current_state()

def east_button_click():
    print_to_description("E", True)
    perform_command("EAST", "")
    set_current_state()

def west_button_click():
    print_to_description("WEST", True)
    perform_command("WEST", "")
    set_current_state()

def return_key_enter(event):
    if event.widget == command_widget:
        command_string = command_widget.get()
        print_to_description(command_string, True)

        command_widget.delete(0, END)
        words = command_string.split(' ', 1)
        verb = words[0]
        noun = (words[1] if (len(words) > 1) else "")
        perform_command(verb.upper(), noun.upper())

        set_current_state()

def set_directions_to_move():
    """Enable or disable movement buttons based on available directions and game state."""
    move_to_north = get_location_to_north(state.current_location) > 0 and not state.end_of_game
    move_to_south = get_location_to_south(state.current_location) > 0 and not state.end_of_game
    move_to_east = get_location_to_east(state.current_location) > 0 and not state.end_of_game
    move_to_west = get_location_to_west(state.current_location) > 0 and not state.end_of_game

    north_button.config(state="normal" if move_to_north else "disabled")
    south_button.config(state="normal" if move_to_south else "disabled")
    east_button.config(state="normal" if move_to_east else "disabled")
    west_button.config(state="normal" if move_to_west else "disabled")

def print_to_description(output, user_input=False):
    description_widget.config(state='normal')
    description_widget.insert(END, output + "\n")
    if user_input:
        description_widget.tag_add("blue_text", CURRENT + " linestart", END + "-1c")
        description_widget.tag_configure("blue_text", foreground='blue')
    description_widget.insert(END, '\n')
    description_widget.config(state='disabled')
    description_widget.see(END)

def play_audio(filename, asynchronous=True, loop=True):
    import platform
    operating_system = platform.system()

    if operating_system == 'Linux':
        from replit import audio
        sound = audio.play_file(filename)
        sound = audio.play_file('res/cold-moon.wav')
        sound.paused = False
        # according to documentation, setting .set_loop to -1 should create infinite loop in replit. Can't get it to work
        sound.set_loop(-1)
    elif operating_system == 'Windows':
        import winsound
        winsound.PlaySound(filename, winsound.SND_FILENAME +
                           (winsound.SND_ASYNC if asynchronous else 0) +
                           (winsound.SND_LOOP if loop else 0)
                           )
    elif operating_system == 'darwin':
        import os
        while playing:
            os.system('afplay res/audio/{}'.format(filename))
    else:
        print_to_description("unsupported platform")

def main():
    build_interface()

    services.register_ui(
        print_to_description,
        show_popup_image
    )
    set_current_state()
    root.mainloop()

state = GameState()
main()
