import locations

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