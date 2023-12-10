from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
import json
import locations
import objects
import desc_print

PORTRAIT_LAYOUT = True

list_of_locations = locations.list_of_locations

command_widget = None
image_label = None
description_widget = desc_print.description_widget
inventory_widget = None
north_button = None
south_button = None
east_button = None
west_button = None
root = None

refresh_location = True
refresh_objects_visible = True

current_location = locations.list_of_locations[0]
end_of_game = False

import movement

with open('json/commands.json') as commands_file:
    list_of_commands = json.load(commands_file)

game_objects = objects.game_objects

def perform_command(verb, noun):
    
    if (verb == "GO"):
        perform_go_command(noun)
    elif ((verb == "N") or (verb == "S") or (verb == "E") or (verb == "W")):
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
    else:
        desc_print.print_to_description("unknown command")
        
def perform_go_command(direction):

    global current_location
    global refresh_location
    
    if (direction == "N" or direction == "NORTH"):
        new_location = movement.get_location_to_north(current_location)
    elif (direction == "S" or direction == "SOUTH"):
        new_location = movement.get_location_to_south(current_location)
    elif (direction == "E" or direction == "EAST"):
        new_location = movement.get_location_to_east(current_location)
    elif (direction == "W" or direction == "WEST"):
        new_location = movement.get_location_to_west(current_location)
    else:
        new_location = 0
        
    if (new_location == 0):
        desc_print.print_to_description("You can't go that way!")
    else:
        current_location = new_location
        refresh_location = True

def perform_get_command(object_name):
    
    global refresh_objects_visible
    game_object = get_game_object(object_name)
    
    if not (game_object is None):
        if (game_object.location != current_location or game_object.visible == False):
            desc_print.print_to_description("You don't see one of those here!")
        elif (game_object.movable == False):
            desc_print.print_to_description("You can't pick it up!")
        elif (game_object.carried == True):
            desc_print.print_to_description("You are already carrying it")
        else:
            #handle special conditions
            if (False):
                desc_print.print_to_description("special condition")
            else:
                #pick up the object
                game_object.carried = True
                game_object.visible = False
                refresh_objects_visible = True
    else:
        desc_print.print_to_description("You don't see one of those here!")

# 
def perform_put_command(object_name):

    global refresh_objects_visible
    game_object = get_game_object(object_name)
    
    if not (game_object is None):
        if (game_object.carried == False):
            desc_print.print_to_description("You are not carrying one of those.")
        else:
            #put down the object
            game_object.location = current_location
            game_object.carried = False
            game_object.visible = True
            refresh_objects_visible = True
    else:
        desc_print.print_to_description("You are not carrying one of those!")
# 
def perform_look_command(object_name):

    global sword_found
    global refresh_location
    global refresh_objects_visible
    
    game_object = get_game_object(object_name)
 
    if not (game_object is None):

        if ((game_object.carried == True) or (game_object.visible and game_object.location == current_location)):
            desc_print.print_to_description(game_object.description)
        else:
            #recognized but not visible
            desc_print.print_to_description("You can't see one of those!")
 
        #special cases - when certain objects are looked at, others are revealed!
        if (False):
            desc_print.print_to_description("special condition")
            global refresh_objects_visible
            refresh_objects_visible = True

    else:
        if (object_name == ""):
            #generic LOOK
            refresh_location = True
            refresh_objects_visible = True
        else:
            #not visible recognized
            desc_print.print_to_description("You can't see one of those!")

def perform_read_command(object_name):

    game_object = get_game_object(object_name)
 
    if not (game_object is None):
        if (False):
            desc_print.print_to_description("special condition")
        else:
            desc_print.print_to_description("There is no text on it")
    else:
        desc_print.print_to_description("I am not sure which " + object_name + "you are referring to")
# 
def perform_open_command(object_name):

    global door_open
    game_object = get_game_object(object_name)
 
    if not (game_object is None):
        if (False):
            desc_print.print_to_description("special condition")
        else:
            desc_print.print_to_description("You can't open one of those.")
    else:
        desc_print.print_to_description("You don't see one of those here.")

def perform_help_command(verb):
    desc_print.print_to_description("here are the commands for the game:")
    for command in list_of_commands:
        desc_print.print_to_description(command)

def set_current_image():
    
    if (current_location == 1):
        image_label.img = PhotoImage(file ='res/images/blank-1.gif')
    elif (current_location == 2):
        image_label.img = PhotoImage(file ='res/images/blank-2.gif')
    elif (current_location == 3):
        image_label.img = PhotoImage(file ='res/images/blank-3.gif')
    elif (current_location == 4):
        image_label.img = PhotoImage(file ='res/images/hallway_prototype.png')
    else:
        image_label.img = PhotoImage(file ='res/images/blank-1.gif')
        
    image_label.config(image = image_label.img)


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
    
    for current_object in game_objects:
        if ((current_object.location  == current_location) and (current_object.visible == True) and (current_object.carried == False)):
            object_list = object_list + ("," if object_count > 0 else "") + current_object.name
            object_count = object_count + 1
            
    desc_print.print_to_description("You see: " + (object_list + "." if object_count > 0 else "nothing special."))

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
        desc_print.print_to_description("GAME OVER")
        end_of_game = True


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

    root = Tk()
    root.resizable(0,0)
    
    style = ttk.Style()
    style.configure("BW.TLabel", foreground="black", background="white")

    image_label = ttk.Label(root)
    if (PORTRAIT_LAYOUT):
        image_label.grid(row=0, column=0, columnspan =3,padx = 2, pady = 2)
    else:
        image_label.grid(row=0, column=0, rowspan=3, columnspan=1,padx = 2, pady = 2)

    desc_print.description_widget = Text(root, width =60, height = 10, relief = GROOVE, wrap = 'word')
    desc_print.description_widget.insert(1.0, "Welcome to my game.\n\nGood Luck!\n\n ")
    desc_print.description_widget.config(state = "disabled")
    if (PORTRAIT_LAYOUT):
        desc_print.description_widget.grid(row=1, column=0, columnspan=3, sticky=W, padx=2, pady =2)
    else:
        desc_print.description_widget.grid(row=0, column=1, rowspan=1, columnspan=2, padx=2, pady =2)

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
    
def set_current_state():

    global refresh_location
    global refresh_objects_visible

    if (refresh_location):
        locations.describe_current_location(current_location)
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
    desc_print.print_to_description("N", True)
    perform_command("N", "")
    set_current_state()

def south_button_click():
    desc_print.print_to_description("S", True)
    perform_command("S", "")
    set_current_state()

def east_button_click():
    desc_print.print_to_description("E", True)
    perform_command("E", "")
    set_current_state()

def west_button_click():
    desc_print.print_to_description("W", True)
    perform_command("W", "")
    set_current_state()

def return_key_enter(event):
    if( event.widget == command_widget):
        command_string = command_widget.get()
        desc_print.print_to_description(command_string, True)

        command_widget.delete(0, END)
        words = command_string.split(' ', 1)
        verb = words[0]
        noun = (words[1] if (len(words) > 1) else "")
        perform_command(verb.upper(), noun.upper())
        
        set_current_state()

def set_directions_to_move():

    move_to_north = (movement.get_location_to_north(current_location) > 0) and (end_of_game == False)
    move_to_south = (movement.get_location_to_south(current_location) > 0) and (end_of_game == False)
    move_to_east = (movement.get_location_to_east(current_location) > 0) and (end_of_game == False)
    move_to_west = (movement.get_location_to_west(current_location) > 0) and (end_of_game == False)
    
    north_button.config(state = ("normal" if move_to_north else "disabled"))
    south_button.config(state = ("normal" if move_to_south else "disabled"))
    east_button.config(state = ("normal" if move_to_east else "disabled"))
    west_button.config(state = ("normal" if move_to_west else "disabled"))

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
        sound_file = ""
        path_to_file = 'res/sounds/{}'.format(sound_file)
        os.system('afplay {}'.format(path_to_file))

def main():
    
    build_interface()
    set_current_state()
    root.mainloop()
        
main()
