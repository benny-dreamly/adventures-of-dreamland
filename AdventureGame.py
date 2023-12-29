import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from PIL import ImageTk, Image
import GameObject
import locations

PORTRAIT_LAYOUT = True

list_of_locations = locations.load_locations()
location_names = locations.load_location_names()
location_descriptions = locations.load_location_descriptions()
location_subtitles = locations.load_location_subtitles()

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

refresh_location = True
refresh_objects_visible = True

current_location = list_of_locations[0]
end_of_game = False

playing = False

list_of_commands = locations.load_commands()

puzzle_piece_1 = GameObject.GameObject("puzzle piece", list_of_locations[0], True, True, False, "puzzle piece 1")
hint1 = GameObject.GameObject("hint 1", list_of_locations[0], True, False, False, "hint #1")
clue1 = GameObject.GameObject("clue 1", list_of_locations[1], True, False, False, "clue #1")
clue2 = GameObject.GameObject("clue 2", list_of_locations[2], True, False, False, "clue #2 (ONLY READ ONCE HINT 1 IS SOLVED)")
puzzle = GameObject.GameObject("puzzle", list_of_locations[2], True, True, False, "puzzle")
puzzle_with_one_piece_inserted = GameObject.GameObject("puzzle (1/9)", puzzle, True, False, False, "puzzle")
puzzle_with_two_pieces_inserted = GameObject.GameObject("puzzle (2/9)", puzzle_with_one_piece_inserted, True, False, False, "puzzle")
kp1 = GameObject.GameObject("key piece A", list_of_locations[0], True, False, False, "I wonder what you do with me?", True)
kp2 = GameObject.GameObject("key piece B", list_of_locations[0], True, False, False, "I wonder what you do with me?", True)
kp3 = GameObject.GameObject("key piece C", list_of_locations[0], True, False, False, "I wonder what you do with me?", True)
kp4 = GameObject.GameObject("key piece D", list_of_locations[0], True, False, False, "I wonder what you do with me?", True)
kp5 = GameObject.GameObject("key piece E", list_of_locations[0], True, False, False, "I wonder what you do with me?", True)
kp6 = GameObject.GameObject("key piece F", list_of_locations[0], True, False, False, "I wonder what you do with me?", True)
kp7 = GameObject.GameObject("key piece G", list_of_locations[0], True, False, False, "I wonder what you do with me?", True)
key = GameObject.GameObject("key", list_of_locations[0], True, False, False, "a golden key")
scroll = GameObject.GameObject("scroll", list_of_locations[0], True, True, False, "an ancient papyrus scroll")
scroll_hint = GameObject.GameObject("hint", list_of_locations[10], True, True, False, "huh")
safe = GameObject.GameObject("safe", list_of_locations[9], False, True, False, "a small safe")
gold_bar = GameObject.GameObject("gold bar", list_of_locations[10], True, True, False, "a gold bar with an engraving in it")
bar_clue = GameObject.GameObject("clue", list_of_locations[10], True, False, False, "clue")
puzzle_piece_2 = GameObject.GameObject("puzzle piece", list_of_locations[10], True, False, False, "puzzle piece 2")
game_objects = [puzzle_piece_1, puzzle_piece_2, hint1, scroll_hint, clue1, clue2, puzzle, puzzle_with_one_piece_inserted, puzzle_with_two_pieces_inserted, kp1, kp2, kp3, kp4, kp5, kp6, kp7, key, scroll, safe, gold_bar, bar_clue]

def perform_command(verb, noun):
    
    if (verb == "GO"):
        perform_go_command(noun)
    elif ((verb == "N") or (verb == "S") or (verb == "E") or (verb == "W") or (verb == "A") or (verb == "D")):
        perform_go_command(verb)        
    elif ((verb == "NORTH") or (verb == "SOUTH") or (verb == "EAST") or (verb == "WEST")):
        perform_go_command(verb)        
    elif (verb == "GET"):
        perform_get_command(noun)
    elif (verb == "PUT"):
        perform_put_command(noun)
    elif (verb == "LOOK"):
        perform_look_command(noun)
    elif (verb == "READ"):
        perform_read_command(noun)        
    elif (verb == "OPEN"):
        perform_open_command(noun)
    elif (verb == "HELP"):
        perform_help_command(noun)
    elif (verb == "SOLVE"):
        perform_solve_command(noun)
    elif (verb == "UNLOCK"):
        perform_unlock_command(noun)
    else:
        print_to_description("unknown command")
        
def perform_go_command(direction):

    global current_location
    global refresh_location
    
    if (direction == "N" or direction == "NORTH" or direction == "W"):
        new_location = get_location_to_north(current_location)
    elif (direction == "S" or direction == "SOUTH"):
        new_location = get_location_to_south(current_location)
    elif (direction == "E" or direction == "EAST" or direction == "D"):
        new_location = get_location_to_east(current_location)
    elif (direction == "W" or direction == "WEST" or direction == "A"):
        new_location = get_location_to_west(current_location)
    else:
        new_location = 0
        
    if (new_location == 0):
        print_to_description("You can't go that way!")
    else:
        current_location = new_location
        refresh_location = True

def perform_get_command(object_name):
    global refresh_objects_visible
    game_object = get_game_object(object_name)
    if not (game_object is None):
        if (game_object.location != current_location or game_object.visible == False) and (special_flag != True):
            print_to_description("You don't see one of those here!")
        elif (game_object.movable == False):
            print_to_description("You can't pick it up!")
        elif (game_object.carried == True):
            print_to_description("You are already carrying it")
        else:
            #handle special conditions
            if (False):
                print_to_description("special condition")
            else:
                #pick up the object
                game_object.carried = True
                game_object.visible = False
                refresh_objects_visible = True
    else:
        print_to_description("You don't see one of those here!")

def perform_put_command(object_name):

    global refresh_objects_visible
    game_object = get_game_object(object_name)
    
    if not (game_object is None):
        if (game_object.carried == False):
            print_to_description("You are not carrying one of those.")
        else:
            #put down the object
            game_object.location = current_location
            game_object.carried = False
            game_object.visible = True
            refresh_objects_visible = True
    else:
        print_to_description("You are not carrying one of those!")

def perform_look_command(object_name):

    global sword_found
    global refresh_location
    global refresh_objects_visible
    
    game_object = get_game_object(object_name)
 
    if not (game_object is None):

        if ((game_object.carried == True) or (game_object.visible and game_object.location == current_location)):
            print_to_description(game_object.description)
        else:
            #recognized but not visible
            print_to_description("You can't see one of those!")
 
        #special cases - when certain objects are looked at, others are revealed!
        if game_object == safe and safe_open:
            print_to_description("Benny sees a puzzle piece in the safe. Maybe he can grab it?")
            global refresh_objects_visible
            refresh_objects_visible = True

    else:
        if (object_name == ""):
            #generic LOOK
            refresh_location = True
            refresh_objects_visible = True
        else:
            #not visible recognized
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
                show_scroll_image()
        elif game_object == scroll_hint:
            if scroll_hint.carried:
                show_scroll_hint_image()
        elif game_object == gold_bar:
            if gold_bar.carried:
                print_to_description("Coins, Minerals, Gold, Silver")
        else:
            print_to_description("You're not carrying anything readable")
    else:
        print_to_description("I am not sure which " + object_name + "you are referring to")

def perform_open_command(object_name):

    global door_open
    global safe_open
    game_object = get_game_object(object_name)

    if not (game_object is None):
        if game_object == safe and (game_object.visible and game_object.location == current_location) and safe_open:
            print_to_description("Benny pulls on the handle and the safe opens!")
            set_current_image()
            game_object.description = "a small safe, with the door wide open"
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
    game_object = get_game_object(object_name)
    piece_slot_message = "The piece slots into the puzzle, but you still haven't solved it."
    if not (game_object is None):
        if game_object.carried and game_object == puzzle:
            answer = simpledialog.askstring("Input", "What would you like to put in the puzzle first?", parent=root)
            if not puzzle_piece_1.carried:
                print_to_description("It looks like you don't have anything to put into the puzzle.")
            elif (answer != "puzzle piece"):
                print_to_description("Unfortunately, it looks like it doesn't fit in the puzzle.")
            else:
                puzzle_piece_inserted = False
                while not puzzle_piece_inserted:
                    slot = simpledialog.askinteger("Input", "Which slot would you like to put your piece in?", parent=root)
                    if slot != 1:
                        print_to_description("The piece won't fit, no matter how you rotate it.")
                        answer = simpledialog.askstring("Input", "Would you like to try again?", parent=root)
                        if answer == "No":
                            break
                    else:
                        print_to_description(piece_slot_message)
                        puzzle_piece_inserted = True
                puzzle_piece_1.carried = False
                game_object.carried = False
                puzzle_with_one_piece_inserted.carried = True
                refresh_objects_visible = True
        if game_object.carried and game_object == puzzle_with_one_piece_inserted:
            answer = simpledialog.askstring("Input", "What would you like to put in the puzzle next?", parent=root)
            if not puzzle_piece_2.carried:
                print_to_description("It looks like you don't have anything to put into the puzzle.")
            elif (answer != "puzzle piece"):
                print_to_description("Unfortunately, it looks like it doesn't fit in the puzzle.")
            else:
                puzzle_piece_inserted = False
                while not puzzle_piece_inserted:
                    slot = simpledialog.askinteger("Input", "Which slot would you like to put your piece in?", parent=root)
                    if slot != 2:
                        print_to_description("The piece won't fit, no matter how you rotate it.")
                        answer = simpledialog.askstring("Input", "Would you like to try again?", parent=root)
                        if answer == "No":
                            break
                    else:
                        print_to_description(piece_slot_message)
                        puzzle_piece_inserted = True
                    puzzle_piece_2.carried = False
                    game_object.carried = False
                    puzzle_with_two_pieces_inserted.carried = True
                    refresh_objects_visible = True
            #print_to_description("the puzzle collapses into a key piece for you.")
            #kp1.carried = True
        else:
            print_to_description("You're missing something.")
    else:
        print_to_description("You can't do that.")

def perform_fuse_command(object_name):
    game_object = get_game_object(object_name)
    if not (game_object is None):
        if game_object.carried and game_object == kp1 and kp2.carried and kp3.carried and kp4.carried and kp5.carried and kp6.carried and kp7.carried and game_object.fuseable:
            print_to_description("The key pieces start glowing, as if you've awakened their ancient powers. One by one, they slowly start forming an actual key.")
            game_object.carried = False
            kp2.carried = False
            kp3.carried = False
            kp4.carried = False
            kp5.carried = False
            kp6.carried = False
            kp7.carried = False
            key.visible = True
            key.location = current_location
            perform_command("GET", "KEY")
        else:
            print_to_description("You're missing something.")
    else:
        print_to_description("You can't do that.")

def perform_unlock_command(object_name):
    global safe_open
    game_object = get_game_object(object_name)
    if not (game_object is None):
        if game_object == safe and (game_object.visible and game_object.location == current_location):
            while not safe_open:
                code = simpledialog.askinteger("Code", "What is the code to the safe?", parent=root)
                if code != 16378:
                    print_to_description("Benny tries your code, but the safe won't open.")
                    answer = simpledialog.askstring("Input", "Would you like to try again?", parent=root)
                    if answer == "No":
                        break
                else:
                    print_to_description("The code you provided Benny with worked! The safe is now unlocked.")
                    safe_open = True
        else:
            print_to_description("You can't unlock that!")
    else:
        print_to_description("There's nothing to unlock.")
def show_scroll_image():

    popup = tkinter.Toplevel(root)

    img = PhotoImage(file="res/images/scroll_scaled.png")

    label = tkinter.Label(popup, image=img)
    label.image = img  # Keep a reference to the image to prevent garbage collection
    label.pack()

def show_scroll_hint_image():

    popup = tkinter.Toplevel(root)

    img = PhotoImage(file="res/images/scroll_key.png")

    label = tkinter.Label(popup, image=img)
    label.image = img  # Keep a reference to the image to prevent garbage collection
    label.pack()

def describe_current_location(current_location):
    if (current_location == 1):
        print_to_description(location_names[0])
        print_to_description(location_descriptions[0])
    elif (current_location == 2):
        print_to_description(location_names[1])
        print_to_description(location_descriptions[1])
    elif (current_location == 3):
        print_to_description(location_names[2])
        print_to_description(location_descriptions[2])
    elif (current_location == 4):
        print_to_description(location_names[3])
        print_to_description(location_descriptions[3])
    elif (current_location == 5):
        print_to_description(location_names[4])
        print_to_description(location_descriptions[4])
    elif (current_location == 6):
        print_to_description(location_names[5])
        print_to_description(location_descriptions[5])
    elif (current_location == 7):
        print_to_description(location_names[6])
        print_to_description(location_descriptions[6])
    elif (current_location == 8):
        print_to_description(location_names[7])
        print_to_description(location_descriptions[7])
    elif (current_location == 9):
        print_to_description(location_names[8])
        print_to_description(location_descriptions[8])
    elif (current_location == 10):
        print_to_description(location_names[9])
        print_to_description(location_descriptions[9])
    elif (current_location == 11):
        print_to_description(location_names[10])
        print_to_description(location_descriptions[10])
    elif (current_location == 12):
        print_to_description(location_names[11])
        print_to_description(location_descriptions[11])
    elif (current_location == 13):
        print_to_description(location_names[12])
    elif (current_location == 14):
        print_to_description(location_names[13])
    elif (current_location == 15):
        print_to_description(location_names[14])
    elif (current_location == 16):
        print_to_description(location_names[15])
    elif (current_location == 17):
        print_to_description(location_names[16])
    elif (current_location == 18):
        print_to_description(location_names[17])
    elif (current_location == 19):
        print_to_description(location_names[18])
    elif (current_location == 20):
        print_to_description(location_names[19])
    else:
        print_to_description("unknown location:" + current_location)

def set_current_image():
    
    if (current_location == 1):
        image_label.img = PhotoImage(file ='res/images/blank-1.gif')
    elif (current_location == 2):
        image_label.img = PhotoImage(file ='res/images/blank-2.gif')
    elif (current_location == 3):
        image_label.img = PhotoImage(file ='res/images/blank-3.gif')
    elif (current_location == 4 or current_location == 5 or current_location == 13 or current_location == 15 or current_location == 16 or current_location == 17 or current_location == 18):
        image_label.img = ImageTk.PhotoImage(file ='res/images/hallway.tiff')
    elif (current_location == 6 or current_location == 14):
        image_label.img = ImageTk.PhotoImage(file='res/images/right_corner.tiff')
    elif (current_location == 12 or current_location == 19):
        image_label.img = ImageTk.PhotoImage(file ='res/images/left_corner.png')
    elif current_location == 10 and not safe_open:
        image_label.img = ImageTk.PhotoImage(file ='res/images/safe-closed.tiff')
    elif safe_open and current_location == 10:
        image_label.img = ImageTk.PhotoImage(file ='res/images/safe-open.tiff')
    else:
        image_label.img = PhotoImage(file ='res/images/missing.png')
        
    image_label.config(image = image_label.img)

def get_location_to_north(current_location, door_open=False):
    if (current_location == 3):
        return 2
    elif (current_location == 2):
        return 1
    elif (current_location == 6):
        return 7
    elif (current_location == 7):
        return 12
    elif (current_location == 8):
        return 11
    elif (current_location == 9):
        return 10
    elif (current_location == 15):
        return 14
    elif (current_location == 16):
        return 15
    elif (current_location == 17):
        return 16
    elif (current_location == 18):
        return 17
    elif (current_location == 19):
        return 18
    elif (current_location == 20):
        return 23
    elif (current_location == 24):
        return 25
    elif (current_location == 25):
        return 26
    elif (current_location == 27):
        return 28
    elif (current_location == 30):
        return 29
    elif (current_location == 31):
        return 32
    elif (current_location == 34):
        return 33
    elif (current_location == 35):
        return 34
    else:
        return 0

def get_location_to_south(current_location, door_open=False):
    if (current_location == 1):
        return 2
    elif (current_location == 2):
        return 3
    elif (current_location == 7):
        return 6
    elif (current_location == 11):
        return 8
    elif (current_location == 10):
        return 9
    elif (current_location == 12):
        return 7
    elif (current_location == 14):
        return 15
    elif (current_location == 15):
        return 16
    elif (current_location == 16):
        return 17
    elif (current_location == 17):
        return 18
    elif (current_location == 18):
        return 19
    elif (current_location == 23):
        return 20
    elif (current_location == 24):
        return 23
    elif (current_location == 25):
        return 24
    elif (current_location == 26):
        return 25
    elif (current_location == 28):
        return 27
    elif (current_location == 29):
        return 30
    elif (current_location == 32):
        return 31
    elif (current_location == 33):
        return 34
    elif (current_location == 31 and door_open == True):
        return 35
    else:
        return 0


def get_location_to_east(current_location, door_open=False):
    if (current_location == 3):
        return 4
    elif (current_location == 4):
        return 5
    elif (current_location == 5):
        return 6
    elif (current_location == 8):
        return 7
    elif (current_location == 9):
        return 8
    elif (current_location == 10):
        return 11
    elif (current_location == 12):
        return 13
    elif (current_location == 13):
        return 14
    elif (current_location == 20):
        return 19
    elif (current_location == 21):
        return 20
    elif (current_location == 22):
        return 21
    elif (current_location == 27):
        return 23
    elif (current_location == 28):
        return 24
    elif (current_location == 29):
        return 28
    elif (current_location == 31):
        return 30
    elif (current_location == 34):
        return 32
    elif (current_location == 33):
        return 31
    elif (current_location == 36):
        return 35
    else:
        return 0


def get_location_to_west(current_location, door_open=False):
    if (current_location == 4):
        return 3
    elif (current_location == 5):
        return 4
    elif (current_location == 6):
        return 5
    elif (current_location == 7):
        return 8
    elif (current_location == 8):
        return 9
    elif (current_location == 11):
        return 10
    elif (current_location == 13):
        return 12
    elif (current_location == 14):
        return 13
    elif (current_location == 19):
        return 20
    elif (current_location == 20):
        return 21
    elif (current_location == 21):
        return 22
    elif (current_location == 23):
        return 27
    elif (current_location == 24):
        return 28
    elif (current_location == 28):
        return 29
    elif (current_location == 30):
        return 31
    elif (current_location == 31):
        return 34
    elif (current_location == 32):
        return 33
    elif (current_location == 35):
        return 36
    else:
        return 0

def describe_current_inventory():
    
    object_count = 0
    object_list = ""

    for current_object in game_objects:
        if (current_object.carried):
            object_list = object_list + ("," if object_count > 0 else "") + current_object.name
            object_count = object_count + 1
    
    inventory = "You are carrying: " + (object_list if object_count > 0 else "nothing")
    
    inventory_widget.config(state = "normal")
    inventory_widget.delete(1.0, END)
    inventory_widget.insert(1.0, inventory)
    inventory_widget.config(state = "disabled")

def handle_special_condition():
    
    global end_of_game
    
    if (False):
        print_to_description("GAME OVER")
        end_of_game = True

def get_game_object(object_name):
    sought_object = None
    for current_object in game_objects:
        if (current_object.name.upper() == object_name):
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
        clue2.visible = True

    if gold_bar.carried:
        bar_clue.visible = True

    if safe_open:
        puzzle_piece_2.visible = True

    for current_object in game_objects:
        if ((current_object.location == current_location) and (current_object.visible == True) and (
                current_object.carried == False)):
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
    if (PORTRAIT_LAYOUT):
        image_label.grid(row=0, column=0, columnspan =3,padx = 2, pady = 2)
    else:
        image_label.grid(row=0, column=0, rowspan=3, columnspan=1,padx = 2, pady = 2)

    description_widget = Text(root, width =60, height = 10, relief = GROOVE, wrap = 'word')
    description_widget.insert(1.0, "After the catastrophe that was the pandemic, Benny finds himself back in dreamland, but something seems wrong. It looks like Fala and Nodo have taken him prisoner! Now he has to use all of the knowledge he’s gathered throughout all of his various adventures in the past to escape. \n\nFala and Nodo have hidden various puzzles throughout the castle basement. Can you figure them out and help Benny escape before evil takes over the kingdom? You’re the kingdom’s only hope at rescuing the protector of Dreamland.\n\n")
    description_widget.config(state = "disabled")
    if (PORTRAIT_LAYOUT):
        description_widget.grid(row=1, column=0, columnspan=3, sticky=W, padx=2, pady =2)
    else:
        description_widget.grid(row=0, column=1, rowspan=1, columnspan=2, padx=2, pady =2)

    command_widget = ttk.Entry(root, width = (25 if PORTRAIT_LAYOUT else 54), style="BW.TLabel")
    command_widget.bind('<Return>', return_key_enter)
    if (PORTRAIT_LAYOUT):
        command_widget.grid(row=2, column=0, padx = 2, pady = 2)
    else:
        command_widget.grid(row=1, column=1, rowspan=1, columnspan=2)
    
    button_frame = ttk.Frame(root)
    button_frame.config(height = 150, width = 150, relief = GROOVE)
    if (PORTRAIT_LAYOUT):
        button_frame.grid(row=3, column=0, columnspan =1, padx = 2, pady = 2)
    else:
        button_frame.grid(row=2, column=1, columnspan =1, padx = 2, pady = 2)

    north_button = ttk.Button(button_frame, text = "N", width = 5)
    north_button.grid(row=0, column=1, padx = 2, pady = 2)
    north_button.config(command = north_button_click)
    
    south_button = ttk.Button(button_frame, text = "S", width = 5)
    south_button.grid(row=2, column=1, padx = 2, pady = 2)
    south_button.config(command = south_button_click)

    east_button = ttk.Button(button_frame, text = "E", width = 5)
    east_button.grid(row=1, column=2, padx = 2, pady = 2)
    east_button.config(command = east_button_click)

    west_button = ttk.Button(button_frame, text = "W", width = 5)
    west_button.grid(row=1, column=0, padx = 2, pady = 2)
    west_button.config(command = west_button_click)
    
    inventory_widget = Text(root, width = (30 if PORTRAIT_LAYOUT else 38), height = (8 if PORTRAIT_LAYOUT else 6), relief = GROOVE , state=DISABLED )
    if (PORTRAIT_LAYOUT):
        inventory_widget.grid(row=2, column=2, rowspan = 2, padx = 2, pady = 2,sticky=W)
    else:
        inventory_widget.grid(row=2, column=2, rowspan = 2, padx = 2, pady = 2,sticky=W)


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

    if (refresh_location):
        describe_current_location(current_location)
        set_current_image()
    
    if (refresh_location or refresh_objects_visible):
        describe_current_visible_objects()

    handle_special_condition()
    set_directions_to_move()            

    if (end_of_game == False):
        describe_current_inventory()
    
    refresh_location = False
    refresh_objects_visible = False
    
    command_widget.config(state = ("disabled" if end_of_game else "normal"))

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
    if( event.widget == command_widget):
        command_string = command_widget.get()
        print_to_description(command_string, True)

        command_widget.delete(0, END)
        words = command_string.split(' ', 1)
        verb = words[0]
        noun = (words[1] if (len(words) > 1) else "")
        perform_command(verb.upper(), noun.upper())
        
        set_current_state()

def set_directions_to_move():

    move_to_north = (get_location_to_north(current_location) > 0) and (end_of_game == False)
    move_to_south = (get_location_to_south(current_location) > 0) and (end_of_game == False)
    move_to_east = (get_location_to_east(current_location) > 0) and (end_of_game == False)
    move_to_west = (get_location_to_west(current_location) > 0) and (end_of_game == False)
    
    north_button.config(state = ("normal" if move_to_north else "disabled"))
    south_button.config(state = ("normal" if move_to_south else "disabled"))
    east_button.config(state = ("normal" if move_to_east else "disabled"))
    west_button.config(state = ("normal" if move_to_west else "disabled"))

def print_to_description(output, user_input=False):
    description_widget.config(state = 'normal')
    description_widget.insert(END, output)
    if (user_input):
        description_widget.tag_add("blue_text", CURRENT + " linestart", END + "-1c")
        description_widget.tag_configure("blue_text", foreground = 'blue')
    description_widget.insert(END, '\n')
    description_widget.config(state = 'disabled')
    description_widget.see(END)

def play_audio(filename, asynchronous = True, loop = True):

    import platform
    operating_system = platform.system()

    if (operating_system == 'Linux'):
        from replit import audio
        sound = audio.play_file(filename)
        sound = audio.play_file('res/cold-moon.wav')
        sound.paused = False
        #according to documentation, setting .set_loop to -1 should create infinite loop in replit. Can't get it to work
        sound.set_loop(-1)
    elif (operating_system == 'Windows'):  
        import winsound
        winsound.PlaySound(filename,winsound.SND_FILENAME + \
                           (winsound.SND_ASYNC if asynchronous else 0)  + \
                           (winsound.SND_LOOP if loop else 0)
                           )
    elif (operating_system == 'darwin'):
        import os
        while playing:
            os.system('afplay res/audio/{}'.format(filename))


def main():
    
    build_interface()
    set_current_state()
    root.mainloop()
        
main()
