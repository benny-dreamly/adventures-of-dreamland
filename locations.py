import json

def load_locations():
    with open('json/locations.json') as locations_file:
        return json.load(locations_file)

def load_location_names():
    with open('json/names.json') as names_file:
        return json.load(names_file)

def load_location_descriptions():
    with open('json/descriptions.json') as descriptions_file:
        return json.load(descriptions_file)

def load_commands():
    with open('json/commands.json') as commands_file:
        return json.load(commands_file)

def load_location_subtitles():
    with open('json/sub_titles.json') as subtitles_file:
        return json.load(subtitles_file)

def load_commands():
    with open('json/commands.json') as commands_file:
        return json.load(commands_file)
