from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
import GameObject

PORTRAIT_LAYOUT = True

FIRST_LOCATION = 1
SECOND_LOCATION = 2
THIRD_LOCATION = 3
FOURTH_LOCATION = 4
FIFTH_LOCATION = 5
SIXTH_LOCATION = 6
SEVENTH_LOCATION = 7
EIGHTH_LOCATION = 8
NINTH_LOCATION = 9
TENTH_LOCATION = 10
ELEVENTH_LOCATION = 11
TWELFTH_LOCATION = 12
THIRTEENTH_LOCATION = 13
FOURTEENTH_LOCATION = 14
FIFTEENTH_LOCATION = 15
SIXTEENTH_LOCATION = 16
SEVENTEENTH_LOCATION = 17
EIGHTEENTH_LOCATION = 18
NINETEENTH_LOCATION = 19
TWENTIETH_LOCATION = 20
TWENTY_FIRST_LOCATION = 21
TWENTY_SECOND_LOCATION = 22
TWENTY_THIRD_LOCATION = 23
TWENTY_FOURTH_LOCATION = 24
TWENTY_FIFTH_LOCATION = 25
TWENTY_SIXTH_LOCATION = 26
TWENTY_SEVENTH_LOCATION = 27
TWENTY_EIGHTH_LOCATION = 28
TWENTY_NINTH_LOCATION = 29
THIRTIETH_LOCATION = 30
THIRTY_FIRST_LOCATION = 31
THIRTY_SECOND_LOCATION = 32
THIRTY_THIRD_LOCATION = 33
THIRTY_FOURTH_LOCATION = 34
THIRTY_FIFTH_LOCATION = 35
THIRTY_SIXTH_LOCATION = 36

command_widget = None
image_label = None
description_widget = None
inventory_widget = None
north_button = None
south_button = None
east_button = None
west_button = None
root = None

refresh_location = True
refresh_objects_visible = True

current_location = FIRST_LOCATION
end_of_game = False

generic_object = GameObject.GameObject("object", FIRST_LOCATION, True, True, False, "description")

game_objects = [generic_object]

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
    else:
        print_to_description("huh?")       
        
def perform_go_command(direction):

    global current_location
    global refresh_location
    
    if (direction == "N" or direction == "NORTH"):
        new_location = get_location_to_north()
    elif (direction == "S" or direction == "SOUTH"):
        new_location = get_location_to_south()
    elif (direction == "E" or direction == "EAST"):
        new_location = get_location_to_east()
    elif (direction == "W" or direction == "WEST"):
        new_location = get_location_to_west()
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
        if (game_object.location != current_location or game_object.visible == False):
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

# 
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
# 
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
        if (False):
            print_to_description("special condition")
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
        if (False):
            print_to_description("special condition")
        else:
            print_to_description("There is no text on it")
    else:
        print_to_description("I am not sure which " + object_name + "you are referring to")
# 
def perform_open_command(object_name):

    global door_openend
    game_object = get_game_object(object_name)
 
    if not (game_object is None):
        if (False):
            print_to_description("special condition")
        else:
            print_to_description("You can't open one of those.")
    else:
        print_to_description("You don't see one of those here.")
                
def describe_current_location():
        
    if (current_location == FIRST_LOCATION):
        print_to_description("starting room (1)")
    elif (current_location == SECOND_LOCATION):
        print_to_description("starting room (2)")
    elif (current_location == THIRD_LOCATION):
        print_to_description("starting room (3)")
    elif (current_location == FOURTH_LOCATION):
        print_to_description("hallway (1)")
    elif (current_location == FIFTH_LOCATION):
        print_to_description("hallway (2)")
    elif (current_location == SIXTH_LOCATION):
        print_to_description("hallway (3)")
    elif (current_location == SEVENTH_LOCATION):
        print_to_description("hallway (4)")
    elif (current_location == EIGHTH_LOCATION):
        print_to_description("orange room (1)")
    elif (current_location == NINTH_LOCATION):
        print_to_description("orange room (2)")
    elif (current_location == TENTH_LOCATION):
        print_to_description("orange room (3)")
    elif (current_location == ELEVENTH_LOCATION):
        print_to_description("orange room (4)")
    elif (current_location == TWELFTH_LOCATION):
        print_to_description("hallway (5)")
    elif (current_location == THIRTEENTH_LOCATION):
        print_to_description("hallway (6)")
    else:
        print_to_description("unknown location:" + current_location)

def set_current_image():
    
    if (current_location == FIRST_LOCATION):
        image_label.img = PhotoImage(file = 'res/blank-1.gif')
    elif (current_location == SECOND_LOCATION):
        image_label.img = PhotoImage(file = 'res/blank-2.gif')
    elif (current_location == THIRD_LOCATION):
        image_label.img = PhotoImage(file = 'res/blank-3.gif')
    elif (current_location == FOURTH_LOCATION):
        image_label.img = PhotoImage(file = 'res/blank-4.gif')
    else:
        image_label.img = PhotoImage(file = 'res/blank-1.gif')
        
    image_label.config(image = image_label.img)
        

def get_location_to_north():
    
    if (current_location == THIRD_LOCATION):
        return SECOND_LOCATION
    elif (current_location == SECOND_LOCATION):
        return FIRST_LOCATION
    elif (current_location == SIXTH_LOCATION):
        return SEVENTH_LOCATION
    elif (current_location == SEVENTH_LOCATION):
        return TWELFTH_LOCATION
    elif (current_location == EIGHTH_LOCATION):
        return ELEVENTH_LOCATION
    elif (current_location == NINTH_LOCATION):
        return TENTH_LOCATION
    elif (current_location == FIFTEENTH_LOCATION):
        return FOURTEENTH_LOCATION
    elif (current_location == SIXTEENTH_LOCATION):
        return FIFTEENTH_LOCATION
    elif (current_location == SEVENTEENTH_LOCATION):
        return SIXTEENTH_LOCATION
    elif (current_location == EIGHTEENTH_LOCATION):
        return SEVENTEENTH_LOCATION
    elif (current_location == NINETEENTH_LOCATION):
        return EIGHTEENTH_LOCATION
    elif (current_location == TWENTIETH_LOCATION):
        return TWENTY_THIRD_LOCATION
    elif (current_location == TWENTY_FOURTH_LOCATION):
        return TWENTY_FIFTH_LOCATION
    elif (current_location == TWENTY_FIFTH_LOCATION):
        return TWENTY_SIXTH_LOCATION
    elif (current_location == TWENTY_SEVENTH_LOCATION):
        return TWENTY_EIGHTH_LOCATION
    elif (current_location == THIRTIETH_LOCATION):
        return TWENTY_NINTH_LOCATION
    elif (current_location == THIRTY_FIRST_LOCATION):
        return THIRTY_SECOND_LOCATION
    elif (current_location == THIRTY_FOURTH_LOCATION):
        return THIRTY_THIRD_LOCATION
    elif (current_location == THIRTY_FIFTH_LOCATION):
        return THIRTY_FOURTH_LOCATION
    else:
        return 0

def get_location_to_south():
    
    if (current_location == FIRST_LOCATION):
        return SECOND_LOCATION
    elif (current_location == SECOND_LOCATION):
        return THIRD_LOCATION
    elif (current_location == SEVENTH_LOCATION):
        return SIXTH_LOCATION
    elif (current_location == ELEVENTH_LOCATION):
        return EIGHTH_LOCATION
    elif (current_location == TENTH_LOCATION):
        return NINTH_LOCATION
    elif (current_location == TWELFTH_LOCATION):
        return SEVENTH_LOCATION
    elif (current_location == FOURTEENTH_LOCATION):
        return FIFTEENTH_LOCATION
    elif (current_location == FIFTEENTH_LOCATION):
        return SIXTEENTH_LOCATION
    elif (current_location == SIXTEENTH_LOCATION):
        return SEVENTEENTH_LOCATION
    elif (current_location == EIGHTEENTH_LOCATION):
        return NINETEENTH_LOCATION
    elif (current_location == TWENTY_THIRD_LOCATION):
        return TWENTIETH_LOCATION
    elif (current_location == TWENTY_FOURTH_LOCATION):
        return TWENTY_THIRD_LOCATION
    elif (current_location == TWENTY_FIFTH_LOCATION):
        return TWENTY_FOURTH_LOCATION
    elif (current_location == TWENTY_SIXTH_LOCATION):
        return TWENTY_FIFTH_LOCATION
    elif (current_location == TWENTY_EIGHTH_LOCATION):
        return TWENTY_SEVENTH_LOCATION
    elif (current_location == TWENTY_NINTH_LOCATION):
        return THIRTIETH_LOCATION
    elif (current_location == THIRTY_SECOND_LOCATION):
        return THIRTY_FIRST_LOCATION
    elif (current_location == THIRTY_THIRD_LOCATION):
        return THIRTY_FOURTH_LOCATION
    elif (current_location == THIRTY_FIRST_LOCATION):
        return THIRTY_FIFTH_LOCATION
    else:
        return 0

def get_location_to_east():
    
    if (current_location == THIRD_LOCATION):
        return FOURTH_LOCATION
    elif (current_location == FOURTH_LOCATION):
        return FIFTH_LOCATION
    else:
        return 0

def get_location_to_west():
    
    if (current_location == FOURTH_LOCATION):
        return THIRD_LOCATION
    elif (current_location == FIFTH_LOCATION):
        return FOURTH_LOCATION
    else:
        return 0
        
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
            
    print_to_description("You see: " + (object_list + "." if object_count > 0 else "nothing special.")) 

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

def print_to_description(output, user_input=False):
    description_widget.config(state = 'normal')
    description_widget.insert(END, output)
    if (user_input):
        description_widget.tag_add("blue_text", CURRENT + " linestart", END + "-1c")
        description_widget.tag_configure("blue_text", foreground = 'blue')
    description_widget.insert(END, '\n')        
    description_widget.config(state = 'disabled')
    description_widget.see(END)

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

    description_widget = Text(root, width =60, height = 10, relief = GROOVE, wrap = 'word')
    description_widget.insert(1.0, "Welcome to my game.\n\nGood Luck!\n\n ")
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
    
def set_current_state():

    global refresh_location
    global refresh_objects_visible

    if (refresh_location):
        describe_current_location()
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
    perform_command("N", "")
    set_current_state()

def south_button_click():
    print_to_description("S", True)
    perform_command("S", "")
    set_current_state()

def east_button_click():
    print_to_description("E", True)
    perform_command("E", "")
    set_current_state()

def west_button_click():
    print_to_description("W", True)
    perform_command("W", "")
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

    move_to_north = (get_location_to_north() > 0) and (end_of_game == False)
    move_to_south = (get_location_to_south() > 0) and (end_of_game == False)
    move_to_east = (get_location_to_east() > 0) and (end_of_game == False)
    move_to_west = (get_location_to_west() > 0) and (end_of_game == False)
    
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

def main():
    
    build_interface()
    set_current_state()
    root.mainloop()
        
main()
