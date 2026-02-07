from enum import IntEnum


class Location(IntEnum):

    # --- Cells ---
    CELL_1 = 1
    CELL_2 = 2
    CELL_3 = 3

    # --- Hallways ---
    HALLWAY_1  = 4
    HALLWAY_2  = 5
    HALLWAY_3  = 6
    HALLWAY_4  = 7
    HALLWAY_5  = 12
    HALLWAY_6  = 13
    HALLWAY_7  = 14
    HALLWAY_8  = 15
    HALLWAY_9  = 16
    HALLWAY_10 = 17
    HALLWAY_11 = 18
    HALLWAY_12 = 19
    HALLWAY_13 = 20

    # --- Vaults ---
    VAULT_1 = 8
    VAULT_2 = 9
    VAULT_3 = 10
    VAULT_4 = 11

    # --- Supply / misc ---
    SUPPLY_1 = 21
    SUPPLY_2 = 22
    STAIRWELL = 23
