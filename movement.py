import AdventureGame
current_location = AdventureGame.current_location

def get_location_to_north():
    if (current_location == 3):
        return 2
    elif (current_location == 2):
        return 3
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

def get_location_to_south():
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
        return list_of_locations[7 - 1]
    elif (current_location == 14):
        return list_of_locations[15 - 1]
    elif (current_location == 15):
        return list_of_locations[16 - 1]
    elif (current_location == 16):
        return list_of_locations[17 - 1]
    elif (current_location == 17):
        return list_of_locations[18 - 1]
    elif (current_location == 18):
        return list_of_locations[19 - 1]
    elif (current_location == 23):
        return list_of_locations[20 - 1]
    elif (current_location == 24):
        return list_of_locations[23 - 1]
    elif (current_location == 25):
        return list_of_locations[24 - 1]
    elif (current_location == 26):
        return list_of_locations[25 - 1]
    elif (current_location == 28):
        return list_of_locations[27 - 1]
    elif (current_location == 29):
        return list_of_locations[30 - 1]
    elif (current_location == 32):
        return list_of_locations[31 - 1]
    elif (current_location == 33):
        return list_of_locations[34 - 1]
    elif (current_location == 31 and door_open == True):
        return list_of_locations[35 - 1]
    else:
        return 0


def get_location_to_east():
    if (current_location == 3):
        return list_of_locations[4 - 1]
    elif (current_location == 4):
        return list_of_locations[5 - 1]
    elif (current_location == 5):
        return list_of_locations[6 - 1]
    elif (current_location == 8):
        return list_of_locations[7 - 1]
    elif (current_location == 9):
        return list_of_locations[8 - 1]
    elif (current_location == 10):
        return list_of_locations[11 - 1]
    elif (current_location == 12):
        return list_of_locations[13 - 1]
    elif (current_location == 13):
        return list_of_locations[14 - 1]
    elif (current_location == 20):
        return list_of_locations[19 - 1]
    elif (current_location == 21):
        return list_of_locations[20 - 1]
    elif (current_location == 22):
        return list_of_locations[21 - 1]
    elif (current_location == 27):
        return list_of_locations[23 - 1]
    elif (current_location == 28):
        return list_of_locations[24 - 1]
    elif (current_location == 29):
        return list_of_locations[28 - 1]
    elif (current_location == 31):
        return list_of_locations[30 - 1]
    elif (current_location == 34):
        return list_of_locations[32 - 1]
    elif (current_location == 33):
        return list_of_locations[31 - 1]
    elif (current_location == 36):
        return list_of_locations[35 - 1]
    else:
        return 0


def get_location_to_west():
    if (current_location == 4):
        return list_of_locations[3 - 1]
    elif (current_location == 5):
        return list_of_locations[4 - 1]
    elif (current_location == 6):
        return list_of_locations[5 - 1]
    elif (current_location == 13):
        return list_of_locations[12 - 1]
    elif (current_location == 14):
        return list_of_locations[13 - 1]
    elif (current_location == 19):
        return list_of_locations[20 - 1]
    elif (current_location == 20):
        return list_of_locations[21 - 1]
    elif (current_location == 21):
        return list_of_locations[22 - 1]
    elif (current_location == 23):
        return list_of_locations[27 - 1]
    elif (current_location == 24):
        return list_of_locations[28 - 1]
    elif (current_location == 28):
        return list_of_locations[29 - 1]
    elif (current_location == 30):
        return list_of_locations[31 - 1]
    elif (current_location == 31):
        return list_of_locations[34 - 1]
    elif (current_location == 32):
        return list_of_locations[33 - 1]
    elif (current_location == 35):
        return list_of_locations[36 - 1]
    else:
        return 0