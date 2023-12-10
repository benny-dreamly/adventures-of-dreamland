import json
import desc_print

with open('json/locations.json') as locations_file:
    list_of_locations = json.load(locations_file)

with open('json/names.json') as names_file:
    location_names = json.load(names_file)

with open('json/descriptions.json') as descriptions_file:
    location_descriptions = json.load(descriptions_file)

def describe_current_location(current_location):
    if (current_location == 1):
        desc_print.print_to_description(location_names[0])
    elif (current_location == 2):
        desc_print.print_to_description(location_names[1])
    elif (current_location == 3):
        desc_print.print_to_description(location_names[2])
    elif (current_location == 4):
        desc_print.print_to_description(location_names[3])
    elif (current_location == 5):
        desc_print.print_to_description(location_names[4])
    elif (current_location == 6):
        desc_print.print_to_description(location_names[5])
    elif (current_location == 7):
        desc_print.print_to_description(location_names[6])
    elif (current_location == 8):
        desc_print.print_to_description(location_names[7])
    elif (current_location == 9):
        desc_print.print_to_description(location_names[8])
    elif (current_location == 10):
        desc_print.print_to_description(location_names[9])
    elif (current_location == 11):
        desc_print.print_to_description(location_names[10])
    elif (current_location == 12):
        desc_print.print_to_description(location_names[11])
    elif (current_location == 13):
        desc_print.print_to_description(location_names[12])
    else:
        desc_print.print_to_description("unknown location:" + current_location)
