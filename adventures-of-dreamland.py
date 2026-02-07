import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
import textwrap
import time
from PIL import ImageTk, Image
import GameObject
from location_ids import Location

PORTRAIT_LAYOUT = True

location_names = [
    "Cell (Room 1)\n",
    "Cell (Room 2)\n",
    "Cell (Room 3)\n",
    "Hallway (Room 1)\n",
    "Hallway (Room 2)\n",
    "Hallway (Room 3)\n",
    "Hallway (Room 4)\n",
    "Vault (Room 1)\n",
    "Vault (Room 2)\n",
    "Vault (Room 3)\n",
    "Vault (Room 4)\n",
    "Hallway (Room 5)\n",
    "Hallway (Room 6)\n",
    "Hallway (Room 7)\n",
    "Hallway (Room 8)\n",
    "Hallway (Room 9)\n",
    "Hallway (Room 10)\n",
    "Hallway (Room 11)\n",
    "Hallway (Room 12)\n",
    "Hallway (Room 13)\n",
    "Supply Closet (Room 1)",
    "Supply Closet (Room 2)",
    "Stairwell",
]
location_descriptions = [
    "Benny wakes up in a dark room. He realizes that Fala and Nodo have locked him in the castle jail. Unfortunately, it seems like the great evil has possessed them and decided to lock him up for good. Luckily for him, the guards may have forgotten to lock the cell door behind them!\nThe room looks dilapidated, like nobody’s bothered to maintain it since there hasn’t been any prisoners for years. Cobwebs are scattered around the room, and it looks like the cell is bigger than he thought. There’s a table in the corner, with an old looking scroll that might be made from papyrus. Under the table, he can see a puzzle piece. It seems like the hidden puzzles he heard about when he was being transported into the cell were real. He might have a shot at escaping.\n",
    "Unfortunately for Benny, in the next room he can’t see anything obvious. He thinks he might have to come back later in case there’s something hidden in the room that he can’t see right now. It feels like there might be something hidden in this room.\n",
    "Benny realizes that this cell he’s in right now is really big. It still looks about the same as the other two rooms, lots of cobwebs and some various scattered furniture pieces. This room seems special, though. There’s a pedestal in the middle with a puzzle on it? Yep. Looks like a puzzle. Maybe this will help him escape?\n",
    "Benny finds himself in a hallway, that doesn’t quite seem to have an end to it. He thinks nothing of it, as it appears just to be a hallway.\n",
    "Still looks like a hallway.\n",
    "At last, Benny finds a turn in the corridor. Maybe he’ll find something hidden in the next room?\n",
    "Benny is still in a hallway, but it looks like he’s finally getting somewhere. He can see a room to his left. Maybe he should investigate it?\n",
    "Benny finds himself in another room. It looks like it could be one of the vaults? Nope, just seems to look like some storage. Possibly an office? Nevermind, it really does look like one of the castle vaults. The dark and dingy brick hallways have been replaced with nice wood floors and well kept bricks instead. There’s a small counter in the room, which looks like it could have been used by someone that was keeping track of the items in the vault. It seems that there’s also some space behind the counter that seems to lead into another room.\n",
    "Benny finds a little room with some shelves behind the counter, with a small box one of the shelves. There seems to be a room beside this one that looks to be the actual vault with all of the important valuables in it. No locked door or anything on the actual vault area either. Super strange when you consider there’s probably lots of fairly expensive items in it.\n",
    "Benny finds himself in the actual heart of the vault. It looks like there’s lots of shelves with various precious minerals and lots of coins on the floor. He sees a small safe on one of the shelves, and it looks like he can open it. Unfortunately for him, he doesn’t yet have the combination for the safe. Maybe it will show itself in the next room?\n",
    "There seems to be lots of gold and silver in this room too, but the Dream Diamond and lots of the kingdom’s valuables he’s recovered in the past are also in this part of the vault. Maybe there’s something important in here?\n\nOh look at that, he’s found a small engraving on one of the gold bars. Maybe he can grab it? There also seems to be a little piece of paper in the corner.\n",
    "Benny finds himself at another corner, this time it’s a right turn. There sure is a very long hallway in this castle basement.\n",
    "Benny is still in a straight hallway, how long even is this?\n",
    "How can there be such a long hallway? It feels impractical.\n",
    "It's yet another straight hallway... Why?\n",
    "This hallway feels endless. When will it end?\n",
    "SERIOUSLY!?!? MORE HALLWAY!?!?\n",
    "WHAT THE HECK? THIS HALLWAY WILL NEVER END...\n",
    "Benny has finally arrived at yet another corner, this time it's another right turn... maybe this is the end of the hallway?\n",
    "At last, there seems to be a fork in the road, Benny can keep going straight into another room, or go right into yet another room, after unlocking the door which seems to be in the way. How is he going to get a key to open this door?\n",
    "Benny seems to have found a supply closet. There's a broom leaning on one of the walls, an empty bucket on the floor and a lighter also on the floor. It seems like there's some sort of puzzle in here? Possibly some kind of magic ritual? Benny is still slightly confused on how to solve this. The closet does seem to be a bit bigger though, so he'll probably be able to get a better picture of what he has to do.\n",
    "The closet seems to have a small tub of water in it. Maybe that will somehow be helpful?\n",
    "At last, Benny finds himself at the stairwell. He can escape now, thanks to you.\n"
]

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

door_open = False
safe_open = False
trapdoor_open = False
fire_lit = False
benny_dead = False
broom_destroyed = False
fire_extinguished = False
three_pieces_solved = False

MAX_TIME_ELAPSED = 15

refresh_location = True
refresh_objects_visible = True

current_location = Location.CELL_1
end_of_game = False

playing = False

list_of_commands = ["GO", "N", "S", "E", "W", "NORTH", "SOUTH", "EAST", "WEST", "GET", "READ", "OPEN", "HELP"]

puzzle_piece_1 = GameObject.GameObject("puzzle piece 1", Location.CELL_1, True, True, False, "puzzle piece 1")
hint1 = GameObject.GameObject("hint 1", Location.CELL_1, True, False, False, "hint #1")
clue1 = GameObject.GameObject("clue 1", Location.CELL_2, True, False, False, "clue #1")
clue11 = GameObject.GameObject("clue 1-2", Location.CELL_1, True, False, False, "clue #1.5")
clue2 = GameObject.GameObject("clue 2", Location.CELL_3, True, False, False,
                              "clue #2 (ONLY READ ONCE HINT 1 IS SOLVED)")
puzzle = GameObject.GameObject("puzzle", Location.CELL_3, True, True, False, "puzzle")
puzzle_with_one_piece_inserted = GameObject.GameObject("puzzle (1/4)", puzzle, True, False, False, "puzzle")
puzzle_with_two_pieces_inserted = GameObject.GameObject("puzzle (2/4)", puzzle_with_one_piece_inserted, True, False,
                                                        False, "puzzle")
scroll = GameObject.GameObject("scroll", Location.CELL_1, True, True, False, "an ancient papyrus scroll")
scroll_hint = GameObject.GameObject("hint", Location.VAULT_4, True, True, False, "huh")
safe = GameObject.GameObject("safe", Location.VAULT_3, False, True, False, "a small safe")
gold_bar = GameObject.GameObject("gold bar", Location.VAULT_4, True, True, False,
                                 "a gold bar with an engraving in it")
bar_clue = GameObject.GameObject("clue", Location.VAULT_4, True, False, False, "clue")
puzzle_piece_2 = GameObject.GameObject("puzzle piece 2", Location.VAULT_3, True, False, False, "puzzle piece 2")
hint_fragment_1 = GameObject.GameObject("hint A", Location.HALLWAY_1, True, True, False, "a small piece of ripped paper, it looks like it has some writing on it.", True)
hint_fragment_2 = GameObject.GameObject("hint B", Location.HALLWAY_2, True, False, False, "a small piece of ripped paper, it looks like it has some writing on it.", True)
hint_fragment_3 = GameObject.GameObject("hint C", Location.HALLWAY_3, True, False, False, "a small piece of ripped paper, it looks like it has some writing on it.", True)
hint_fragment_4 = GameObject.GameObject("hint D", Location.HALLWAY_4, True, False, False, "a small piece of ripped paper, it looks like it has some writing on it.", True)
hint_fragment_5 = GameObject.GameObject("hint E", Location.HALLWAY_5, True, False, False, "a small piece of ripped paper, it looks like it has some writing on it.", True)
hint_fragment_6 = GameObject.GameObject("hint F", Location.HALLWAY_6, True, False, False, "a small piece of ripped paper, it looks like it has some writing on it.", True)
hint_fragment_7 = GameObject.GameObject("hint G", Location.HALLWAY_7, True, False, False, "a small piece of ripped paper, it looks like it has some writing on it.", True)
hint_fragment_8 = GameObject.GameObject("hint H", Location.HALLWAY_8, True, False, False, "a small piece of ripped paper, it looks like it has some writing on it.", True)
hint_fragment_9 = GameObject.GameObject("hint I", Location.HALLWAY_9, True, False, False, "a small piece of ripped paper, it looks like it has some writing on it.", True)
hint_fragment_10 = GameObject.GameObject("hint J", Location.HALLWAY_10, True, False, False, "a small piece of ripped paper, it looks like it has some writing on it.", True)
hint_fragment_11 = GameObject.GameObject("hint K", Location.HALLWAY_11, True, False, False, "a small piece of ripped paper, it looks like it has some writing on it.", True)
hint_fragment_12 = GameObject.GameObject("hint L", Location.HALLWAY_12, True, False, False, "a small piece of ripped paper, it looks like it has some writing on it.", True)
hint_fragment_13 = GameObject.GameObject("hint M", Location.HALLWAY_13, True, False, False, "a small piece of ripped paper, it looks like it has some writing on it.", True)
fragment_clue = GameObject.GameObject("cluee", Location.HALLWAY_13, True, True, False, "more ripped looking paper...")
puzzle_piece_3 = GameObject.GameObject("puzzle piece 3", Location.HALLWAY_10, True, False, False, "another puzzle piece woo")
puzzle_with_three_pieces_inserted = GameObject.GameObject("puzzle (3/4)", puzzle_with_two_pieces_inserted, True, False, False, "puzzle (3/4)")
glue_stick = GameObject.GameObject("glue stick", Location.SUPPLY_1, True, False, False, "a glue stick")
hint3 = GameObject.GameObject("hint 3", None, True, False, False, "hint 3")
door = GameObject.GameObject("door", Location.HALLWAY_13, False, True, False, "a large door...")
finished_puzzle = GameObject.GameObject("puzzle (4/4)", puzzle_with_three_pieces_inserted, True, False, False, "a finished puzzle, what does it do?")
puzzle_piece_4 = GameObject.GameObject("puzzle piece 4", Location.SUPPLY_2, True, False, False, "another puzzle piece...")
key = GameObject.GameObject("key", finished_puzzle, True, False, False, "a golden key")
magnifying_glass = GameObject.GameObject("magnifying glass", Location.HALLWAY_13, True, False, False, "a magnifying glass")
broom = GameObject.GameObject("broom", Location.SUPPLY_2, True, True, False, "a broom")
bucket = GameObject.GameObject("bucket", Location.SUPPLY_2, True, True, False, "an empty bucket")
bucket_filled = GameObject.GameObject("water bucket", bucket, True, False, False, "a bucket filled with water")
trapdoor = GameObject.GameObject("trapdoor", Location.HALLWAY_10, False, False, False, "a trapdoor")
water = GameObject.GameObject("water", Location.SUPPLY_2, False, True, False, "water")
lighter = GameObject.GameObject("lighter", Location.SUPPLY_2, True, True, False, "a lighter, maybe you could light a fire with this?")
game_objects = [puzzle_piece_1, puzzle_piece_2, hint1, scroll_hint, clue1, clue11, clue2, puzzle, puzzle_with_one_piece_inserted, puzzle_with_two_pieces_inserted, key, scroll, safe, gold_bar, bar_clue, hint_fragment_1, hint_fragment_2, hint_fragment_3, hint_fragment_4, hint_fragment_5, hint_fragment_6, hint_fragment_7, hint_fragment_8, hint_fragment_9, hint_fragment_10, hint_fragment_11, hint_fragment_12, hint_fragment_13, fragment_clue, puzzle_piece_3, puzzle_with_three_pieces_inserted, glue_stick, hint3, door, finished_puzzle, magnifying_glass, broom, bucket, bucket_filled, trapdoor, lighter, water, puzzle_piece_4]

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
    global current_location
    global refresh_location

    if direction in ["N", "NORTH", "W"]:
        new_location = get_location_to_north(current_location)
    elif direction in ["S", "SOUTH"]:
        new_location = get_location_to_south(current_location)
    elif direction in ["E", "EAST", "D"]:
        new_location = get_location_to_east(current_location)
    elif direction in ["W", "WEST", "A"]:
        new_location = get_location_to_west(current_location)
    else:
        new_location = 0

    if new_location == 0:
        print_to_description("You can't go that way!")
    else:
        current_location = new_location
        refresh_location = True

def perform_get_command(object_name):
    global refresh_objects_visible
    game_object = get_game_object(object_name)
    if not (game_object is None):
        if game_object.location != current_location or not game_object.visible:
            print_to_description("You don't see one of those here!")
        elif not game_object.movable:
            print_to_description("You can't pick it up!")
        elif game_object.carried:
            print_to_description("You are already carrying it")
        else:
            # handle special conditions
            if False:
                print_to_description("special condition")
            else:
                # pick up the object
                game_object.carried = True
                game_object.visible = False
                refresh_objects_visible = True
    else:
        print_to_description("You don't see one of those here!")

def perform_put_command(object_name):
    global refresh_objects_visible
    game_object = get_game_object(object_name)

    if not (game_object is None):
        if not game_object.carried:
            print_to_description("You are not carrying one of those.")
        else:
            # put down the object
            game_object.location = current_location
            game_object.carried = False
            game_object.visible = True
            refresh_objects_visible = True
    else:
        print_to_description("You are not carrying one of those!")

def perform_look_command(object_name):
    global refresh_location
    global refresh_objects_visible

    game_object = get_game_object(object_name)

    if not (game_object is None):

        if game_object.carried or game_object.visible and game_object.location == current_location:
            print_to_description(game_object.description)
        else:
            # recognized but not visible
            print_to_description("You can't see one of those!")

        # special cases - when certain objects are looked at, others are revealed!
        if game_object == safe and safe_open:
            print_to_description("Benny sees a puzzle piece in the safe. Maybe he can grab it?")
            global refresh_objects_visible
            refresh_objects_visible = True

    else:
        if object_name == "":
            # generic LOOK
            refresh_location = True
            refresh_objects_visible = True
        else:
            # not visible recognized
            print_to_description("You can't see one of those!")

def perform_read_command(object_name):
    game_object = get_game_object(object_name)

    if not (game_object is None):
        if game_object == hint1:
            if hint1.carried:
                print_to_description("hint #1:")
                print_to_description("Bw xcb bpm xchhtm xqmkm qv bpm xchhtm, gwc vmml bw xcb qb qv bpm xchhtm. Gwc uig ias: Pwe lw Q xcb bpm xqmkm qv bpm xchhtm? Zmil pqvb 2 bw nqoczm wcb pwe bw xcb bpm xchhtm xqmkm qv bpm nqzab xchhtm.")
        elif game_object == clue1:
            if clue1.carried:
                print_to_description("clue #1:")
                print_to_description("In order to read the hint, you need to know how to decipher it. Your clue is 8 salad.")
        elif game_object == clue2:
            if clue2.carried:
                print_to_description("clue #2:")
                print_to_description("Still confused after deciphering the first hint? I don't blame you. To progress, you need to SOLVE the puzzle.")
        elif game_object == scroll:
            if scroll.carried:
                show_popup_image("scroll.png")
        elif game_object == scroll_hint:
            if scroll_hint.carried:
                show_popup_image("scroll_key.png")
        elif game_object == gold_bar:
            if gold_bar.carried:
                print_to_description("Coins, Minerals, Gold, Silver")
        elif game_object == bar_clue:
            if bar_clue.carried:
                print_to_description("sounds like you've found a code!")
        elif game_object == clue11:
            if clue11.carried:
                print_to_description("clue #1.5:")
                print_to_description("Still having trouble figuring out how to decipher the hint? I don't blame you, it would require some knowledge that only super nerdy people have. Luckily for you, there exists a way to do it for you. Your clue is the word decipher.")
        elif game_object == hint_fragment_1:
            if hint_fragment_1.carried:
                print_to_description("49 6E 20 6F 72 64 65 72 20 74 6F 20 66")
        elif game_object == hint_fragment_2:
            if hint_fragment_2.carried:
                print_to_description("69 6E 64 20 77 68 61 74 20 79 6F 75 20")
        elif game_object == hint_fragment_3:
            if hint_fragment_3.carried:
                print_to_description("6D 61 79 20 62 65 20 6C 6F 6F 6B 69 6E")
        elif game_object == hint_fragment_4:
            if hint_fragment_4.carried:
                print_to_description("67 20 66 6F 72 2C 20 69 74 20 6D 61 79")
        elif game_object == hint_fragment_5:
            if hint_fragment_5.carried:
                print_to_description("20 62 65 20 68 69 64 69 6E 67 20 69 6E")
        elif game_object == hint_fragment_6:
            if hint_fragment_6.carried:
                print_to_description("20 70 6C 61 69 6E 20 73 69 67 68 74 2E")
        elif game_object == hint_fragment_7:
            if hint_fragment_7.carried:
                print_to_description("20 50 65 72 68 61 70 73 20 61 6C 6C 20")
        elif game_object == hint_fragment_8:
            if hint_fragment_8.carried:
                print_to_description("74 68 6F 73 65 20 65 6D 70 74 79 20 68")
        elif game_object == hint_fragment_9:
            if hint_fragment_9.carried:
                print_to_description("61 6C 6C 77 61 79 73 20 79 6F 75 20 77")
        elif game_object == hint_fragment_10:
            if hint_fragment_10.carried:
                print_to_description("65 6E 74 20 70 61 73 74 20 77 65 72 65")
        elif game_object == hint_fragment_11:
            if hint_fragment_11.carried:
                print_to_description("6E 27 74 20 73 6F 20 69 6E 73 69 67 6E")
        elif game_object == hint_fragment_12:
            if hint_fragment_12.carried:
                print_to_description("69 66 69 63 61 6E 74 20 61 74 20 61 6C")
        elif game_object == hint_fragment_13:
            if hint_fragment_13.carried:
                print_to_description("6C 3F")
        elif game_object == fragment_clue:
            if fragment_clue.carried:
                print_to_description("Confused by all the random letters and numbers strewn around the hallway that you've picked up? Can't blame you, but I can... this is how your computer stores the text in a text document. (more specifically a .txt file)")
        elif game_object == hint3:
            if hint3.carried:
                print_to_description("49 6E 20 6F 72 64 65 72 20 74 6F 20 66 69 6E 64 20 77 68 61 74 20 79 6F 75 20 6D 61 79 20 62 65 20 6C 6F 6F 6B 69 6E 67 20 66 6F 72 2C 20 69 74 20 6D 61 79 20 62 65 20 68 69 64 69 6E 67 20 69 6E 20 70 6C 61 69 6E 20 73 69 67 68 74 2E 20 50 65 72 68 61 70 73 20 61 6C 6C 20 74 68 6F 73 65 20 65 6D 70 74 79 20 68 61 6C 6C 77 61 79 73 20 79 6F 75 20 77 65 6E 74 20 70 61 73 74 20 77 65 72 65 6E 27 74 20 73 6F 20 69 6E 73 69 67 6E 69 66 69 63 61 6E 74 20 61 74 20 61 6C 6C 3F")
        else:
            print_to_description("You're not carrying anything readable")
    else:
        print_to_description("I am not sure which " + object_name + "you are referring to")

def perform_open_command(object_name):
    global door_open
    global safe_open
    global trapdoor_open
    global refresh_objects_visible
    game_object = get_game_object(object_name)

    if not (game_object is None):
        if game_object == safe and (game_object.visible and game_object.location == current_location) and safe_open:
            print_to_description("Benny pulls on the handle and the safe opens!")
            set_current_image()
            game_object.description = "a small safe, with the door wide open"
        if game_object == trapdoor and (game_object.visible and game_object.location == current_location) and broom.carried:
            print_to_description("Benny pushes on the trapdoor with the end of the broom and it opens, revealing a puzzle piece.")
            trapdoor_open = True
            refresh_objects_visible = True
        else:
            print_to_description("You can't open one of those.")
    else:
        print_to_description("You don't see one of those here.")

def perform_help_command(verb):
    print_to_description("here are the commands for the game:")
    for command in list_of_commands:
        print_to_description(command)

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

def perform_fill_command(object_name):
    game_object = get_game_object(object_name)
    if not (game_object is None):
        if game_object == bucket:
            if current_location == 22:
                print_to_description("Benny dips the bucket into the water and picks it all up, now his bucket is filled.")
                bucket.carried = False
                for item in [bucket, water]:
                    item.visible = False
                bucket_filled.carried = True
            else:
                print_to_description("You can't fill that here, there isn't any water to fill it.")
        else:
            print_to_description("You can't fill that!")

def perform_use_command(object_name):
    game_object = get_game_object(object_name)
    global fire_lit
    global fire_extinguished
    global broom_destroyed
    global refresh_objects_visible
    if not (game_object is None):
        if game_object == lighter:
            if current_location == 22:
                if broom.visible and broom.location == current_location:
                    print_to_description("Benny lights the broom with the lighter and watches it burn. It seems to be burning quite quickly, and if he doesn't extinguish it soon, he will likely perish if he doesn't escape.")
                    fire_lit = True
                    broom.visible = False
                    lighter.carried = False
                    lighter.visible = False
                    broom_destroyed = True
                else:
                    print_to_description("There's nothing to light on fire.")
            else:
                print_to_description("The fire won't do anything here.")
        elif game_object == bucket_filled:
            if current_location == 22 and fire_lit:
                print_to_description("Benny throws the water onto the fire and manages to put it out. It seems like he has been rewarded for this, as he has managed to reveal another puzzle piece!")
                fire_lit = False
                fire_extinguished = True
                bucket_filled.carried = False
                bucket.carried = True
                puzzle_piece_4.visible = True
                refresh_objects_visible = True
        else:
            print_to_description("You can't use that.")
    else:
        print_to_description("Invalid Object.")

def describe_current_location(current_location):
    index = current_location - 1  # Adjust for 0-based indexing in Python lists
    if 0 <= index < len(location_names):
        print_to_description(location_names[index])
        print_to_description(location_descriptions[index])
    else:
        print_to_description("unknown location: " + str(current_location))

def set_current_image():
    image_mapping = {
        4: 'hallway.tiff',
        5: 'hallway.tiff',
        13: 'hallway.tiff',
        15: 'hallway.tiff',
        18: 'hallway.tiff',
        6: 'right_corner.tiff',
        14: 'right_corner.tiff',
        12: 'left_corner.png',
        19: 'left_corner.png',
        8: 'vault-1.tiff',
        9: 'vault-2.tiff',
        17: 'hallway.tiff',
        1: 'cell_1.tiff',
        2: 'cell_2.tiff',
        3: 'cell_3.tiff',
        16: 'hallway.tiff',
        10: 'safe-open.tiff' if safe_open and puzzle_piece_2.visible else 'open-safe-no-piece.tiff' if puzzle_piece_2.carried and not puzzle_with_two_pieces_inserted.carried else 'safe-closed.tiff',
        11: 'vault-4.tiff' if gold_bar.visible and scroll_hint.visible else 'vault-4-no-hint.tiff' if gold_bar.visible and not scroll_hint.visible else 'vault-4-no-bar.tiff' if scroll_hint.visible and not gold_bar.visible else 'vault-4-no-bar-no-hint.tiff',
        7: 'hallway_one_door.tiff',
        20: 'hallway_two_doors.tiff',
        21: 'room_21.tiff',
        22: 'room_22.tiff',
        23: 'stairs.tiff'
    }

    image_file = image_mapping.get(current_location, 'missing.png')
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
    object_count = 0
    object_list = ""

    for current_object in game_objects:
        if current_object.carried:
            object_list = object_list + ("," if object_count > 0 else "") + current_object.name
            object_count = object_count + 1

    inventory = "You are carrying: " + (object_list if object_count > 0 else "nothing")

    inventory_widget.config(state="normal")
    inventory_widget.delete(1.0, END)
    inventory_widget.insert(1.0, inventory)
    inventory_widget.config(state="disabled")

def handle_special_condition():
    global end_of_game
    global fire_lit
    global benny_dead

    cause_of_death = ""

    if fire_lit and current_location == 22:
        if not bucket_filled.carried:
            cause_of_death = "a fire."
            benny_dead = True

    if benny_dead:
        print_to_description("Benny has died due to " + cause_of_death)
        print_to_description("GAME OVER")
        end_of_game = True

    if broom_destroyed and not three_pieces_solved:
        print_to_description("Benny can't continue to escape, as he used the broom to make a fire before using it for something else.")
        print_to_description("GAME OVER")
        end_of_game = True

    if current_location == 23:
        print_to_description("You successfully helped Benny escape the castle basement! Congratulations.")
        end_of_game = True

def get_game_object(object_name):
    sought_object = None
    for current_object in game_objects:
        if current_object.name.upper() == object_name:
            sought_object = current_object
            break
    return sought_object

def describe_current_visible_objects():
    object_count = 0
    object_list = ""

    if puzzle_piece_1.carried and puzzle.carried:
        hint1.visible = True

    if hint1.carried:
        clue1.visible = True

    if clue1.carried:
        clue11.visible = True

    if clue11.carried:
        clue2.visible = True

    if gold_bar.carried:
        bar_clue.visible = True

    if safe_open and not puzzle_with_two_pieces_inserted.carried:
        puzzle_piece_2.visible = True

    if hint_fragment_1.carried:
        hint_fragment_2.visible = True

    if hint_fragment_2.carried:
        hint_fragment_3.visible = True

    if hint_fragment_3.carried:
        hint_fragment_4.visible = True

    if hint_fragment_4.carried:
        hint_fragment_5.visible = True

    if hint_fragment_5.carried:
        hint_fragment_6.visible = True

    if hint_fragment_6.carried:
        hint_fragment_7.visible = True

    if hint_fragment_7.carried:
        hint_fragment_8.visible = True

    if hint_fragment_8.carried:
        hint_fragment_9.visible = True

    if hint_fragment_9.carried:
        hint_fragment_10.visible = True

    if hint_fragment_10.carried:
        hint_fragment_11.visible = True

    if hint_fragment_11.carried:
        hint_fragment_12.visible = True

    if hint_fragment_12.carried:
        hint_fragment_13.visible = True

    if hint_fragment_13.carried:
        fragment_clue.visible = True

    if fragment_clue.carried:
        glue_stick.visible = True

    if hint3.carried:
        magnifying_glass.visible = True

    if magnifying_glass.carried:
        trapdoor.visible = True

    if trapdoor_open and not puzzle_with_three_pieces_inserted.carried:
        puzzle_piece_3.visible = True

    if fire_extinguished:
        puzzle_piece_4.visible = True

    for current_object in game_objects:
        if (current_object.location == current_location) and current_object.visible and not current_object.carried:
            object_list = object_list + (" and " if object_count > 0 else "") + current_object.name
            object_count = object_count + 1

    print_to_description("Benny sees " + (object_list + "." if object_count > 0 else "nothing special."))

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
    description_widget.insert(1.0, "After the catastrophe that was the pandemic, Benny finds himself back in dreamland, but something seems wrong. It looks like Fala and Nodo have taken him prisoner! Now he has to use all of the knowledge he’s gathered throughout all of his various adventures in the past to escape.\nFala and Nodo have hidden various puzzles throughout the castle basement. Can you figure them out and help Benny escape before evil takes over the kingdom? You’re the kingdom’s only hope at rescuing the protector of Dreamland.\n")
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
    global refresh_location
    global refresh_objects_visible

    if refresh_location:
        describe_current_location(current_location)
        set_current_image()

    if refresh_location or refresh_objects_visible:
        set_current_image()
        describe_current_visible_objects()

    handle_special_condition()
    set_directions_to_move()

    if not end_of_game:
        describe_current_inventory()

    refresh_location = False
    refresh_objects_visible = False

    command_widget.config(state=("disabled" if end_of_game else "normal"))

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
    move_to_north = (get_location_to_north(current_location) > 0) and not end_of_game
    move_to_south = (get_location_to_south(current_location) > 0) and not end_of_game
    move_to_east = (get_location_to_east(current_location) > 0) and not end_of_game
    move_to_west = (get_location_to_west(current_location) > 0) and not end_of_game

    north_button.config(state=("normal" if move_to_north else "disabled"))
    south_button.config(state=("normal" if move_to_south else "disabled"))
    east_button.config(state=("normal" if move_to_east else "disabled"))
    west_button.config(state=("normal" if move_to_west else "disabled"))

def print_to_description(output, user_input=False):
    description_widget.config(state='normal')
    description_widget.insert(END, output)
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
    set_current_state()
    root.mainloop()

main()
