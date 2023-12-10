import GameObject
import locations
import desc_print

list_of_locations = locations.load_locations()
current_location = list_of_locations[0]

refresh_objects_visible = True
door_open = False

generic_object = GameObject.GameObject("key", list_of_locations[0], True, True, False, "a golden key")

game_objects = [generic_object]

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
        if ((current_object.location == current_location) and (current_object.visible == True) and (
                current_object.carried == False)):
            object_list = object_list + ("," if object_count > 0 else "") + current_object.name
            object_count = object_count + 1

    desc_print.print_to_description("You see: " + (object_list + "." if object_count > 0 else "nothing special."))
