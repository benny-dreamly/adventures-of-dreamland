from location_ids import Location
from read_actions import *

OBJECT_DEFS = [
    # --- Cell objects ---
    {
        "id": "puzzle_piece_1",
        "name": "puzzle piece 1",
        "location": Location.CELL_1,
        "movable": True,
        "visible": True,
        "carried": False,
        "description": "puzzle piece 1",
        "visibility_condition": lambda game: True,  # always visible
    },
    {
        "id": "hint1",
        "name": "hint 1",
        "location": Location.CELL_1,
        "movable": True,
        "visible": False,
        "carried": False,
        "description": "hint #1",
        "progression_locked": True,
        "on_read": read_text(
            "hint #1:",
            "Bw xcb bpm xchhtm xqmkm qv bpm xchhtm, gwc vmml bw xcb qb qv bpm xchhtm. Gwc uig ias: Pwe lw Q xcb bpm xqmkm qv bpm xchhtm? Zmil pqvb 2 bw nqoczm wcb pwe bw xcb bpm xchhtm xqmkm qv bpm nqzab xchhtm."
        ),
        "visibility_condition": lambda game: game.has_in_inventory("puzzle_piece_1") and game.get_object("puzzle").carried
    },
    {
        "id": "clue1",
        "name": "clue 1",
        "location": Location.CELL_2,
        "movable": True,
        "visible": False,
        "carried": False,
        "description": "clue #1",
        "progression_locked": True,
        "on_read": read_text(
            "clue #1:",
            "In order to read the hint, you need to know how to decipher it. Your clue is 8 salad."
        ),
        "visibility_condition": lambda game: game.get_object("hint1").carried
    },
    {
        "id": "clue11",
        "name": "clue 1-2",
        "location": Location.CELL_1,
        "movable": True,
        "visible": False,
        "carried": False,
        "description": "clue #1.5",
        "progression_locked": True,
        "on_read": read_text(
            "clue #1.5:",
            "Still having trouble figuring out how to decipher the hint? I don't blame you, it would require some knowledge that only super nerdy people have. Luckily for you, there exists a way to do it for you. Your clue is the word decipher."
        ),
        "visibility_condition": lambda game: game.get_object("clue1").carried
    },
    {
        "id": "clue2",
        "name": "clue 2",
        "location": Location.CELL_3,
        "movable": True,
        "visible": False,
        "carried": False,
        "description": "clue #2 (ONLY READ ONCE HINT 1 IS SOLVED)",
        "progression_locked": True,
        "on_read": read_text(
            "clue #2:",
            "Still confused after deciphering the first hint? I don't blame you. To progress, you need to SOLVE the puzzle."
        ),
        "visibility_condition": lambda game: game.get_object("clue11").carried
    },
    {
        "id": "puzzle",
        "name": "puzzle",
        "location": Location.CELL_3,
        "movable": True,
        "visible": True,
        "carried": False,
        "description": "puzzle",
    },
    {
        "id": "puzzle_1",
        "name": "puzzle (1/4)",
        "location": Location.CELL_3,
        "container": "puzzle",
        "movable": True,
        "visible": False,
        "carried": False,
        "description": "puzzle",
        "progression_locked": True,
    },
    {
        "id": "scroll",
        "name": "scroll",
        "location": Location.CELL_1,
        "movable": True,
        "visible": True,
        "carried": False,
        "description": "an ancient papyrus scroll",
        "on_read": read_image("scroll.png")
    },

    # --- Vault ---
    {
        "id": "scroll_hint",
        "name": "hint",
        "location": Location.VAULT_4,
        "movable": True,
        "visible": True,
        "carried": False,
        "description": "huh",
        "on_read": read_image("scroll_key.png")
    },
    {
        "id": "safe",
        "name": "safe",
        "location": Location.VAULT_3,
        "movable": False,
        "visible": True,
        "carried": False,
        "description": "a small safe",
    },
    {
        "id": "gold_bar",
        "name": "gold bar",
        "location": Location.VAULT_4,
        "movable": True,
        "visible": True,
        "carried": False,
        "description": "a gold bar with an engraving in it",
        "on_read": read_text("Coins, Minerals, Gold, Silver")
    },
    {
        "id": "bar_clue",
        "name": "clue",
        "location": Location.VAULT_4,
        "movable": True,
        "visible": False,
        "carried": False,
        "description": "clue",
        "on_read": read_text("sounds like you've found a code!"),
        "visibility_condition": lambda state: state.has_in_inventory("gold_bar"),
    },
    {
        "id": "puzzle_piece_2",
        "name": "puzzle piece 2",
        "location": Location.VAULT_3,
        "movable": True,
        "visible": False,
        "carried": False,
        "description": "puzzle piece 2",
        "visibility_condition": lambda game: game.get_flag("safe_open") and not game.get_object("puzzle_2").carried
    },
    {
        "id": "puzzle_2",
        "name": "puzzle (2/4)",
        "location": Location.STAIRWELL,
        "container": "puzzle_1",
        "movable": True,
        "visible": False,
        "carried": False,
        "description": "puzzle",
    },

    # --- Hallway hint fragments ---
    *[
        {
            "id": f"hint_fragment_{i}",
            "name": f"hint {chr(64 + i)}",
            "location": getattr(Location, f"HALLWAY_{i}"),
            "movable": True,
            "visible": i == 1,  # first fragment is visible by default
            "carried": False,
            "description": "a small piece of ripped paper, it looks like it has some writing on it.",
            "glueable": True,
            "progression_locked": True,  # now we track that this is progression-locked
            "on_read": read_text(
                {
                    1: "49 6E 20 6F 72 64 65 72 20 74 6F 20 66",
                    2: "69 6E 64 20 77 68 61 74 20 79 6F 75 20",
                    3: "6D 61 79 20 62 65 20 6C 6F 6F 6B 69 6E",
                    4: "67 20 66 6F 72 2C 20 69 74 20 6D 61 79",
                    5: "20 62 65 20 68 69 64 69 6E 67 20 69 6E",
                    6: "20 70 6C 61 69 6E 20 73 69 67 68 74 2E",
                    7: "20 50 65 72 68 61 70 73 20 61 6C 6C 20",
                    8: "74 68 6F 73 65 20 65 6D 70 74 79 20 68",
                    9: "61 6C 6C 77 61 79 73 20 79 6F 75 20 77",
                    10: "65 6E 74 20 70 61 73 74 20 77 65 72 65",
                    11: "6E 27 74 20 73 6F 20 69 6E 73 69 67 6E",
                    12: "69 66 69 63 61 6E 74 20 61 74 20 61 6C",
                    13: "6C 3F"
                }[i]
            ),
            "visibility_condition": (
                (lambda game, prev=i - 1: game.has_in_inventory(f"hint_fragment_{prev}"))
                if i > 1 else
                (lambda game: True)  # first fragment always visible
            )
        }
        for i in range(1, 14)
    ],

    {
        "id": "fragment_clue",
        "name": "cluee",
        "location": Location.HALLWAY_13,
        "movable": True,
        "visible": True,
        "carried": False,
        "description": "more ripped looking paper...",
        "on_read": read_text("Confused by all the random letters and numbers strewn around the hallway that you've picked up? Can't blame you, but I can... this is how your computer stores the text in a text document. (more specifically a .txt file)")
    },

    {
        "id": "puzzle_piece_3",
        "name": "puzzle piece 3",
        "location": Location.HALLWAY_10,
        "movable": True,
        "visible": False,
        "carried": False,
        "description": "another puzzle piece woo",
        "visibility_condition": lambda game: game.get_flag("trapdoor_open") and not game.get_object("puzzle_with_three_pieces_inserted").carried
    },

    {
        "id": "puzzle_3",
        "name": "puzzle (3/4)",
        "location": Location.STAIRWELL,
        "container": "puzzle_2",
        "movable": True,
        "visible": False,
        "carried": False,
        "description": "puzzle (3/4)",
    },

    # --- Supply rooms ---
    {
        "id": "glue_stick",
        "name": "glue stick",
        "location": Location.SUPPLY_1,
        "movable": True,
        "visible": False,
        "carried": False,
        "description": "a glue stick",
        "visibility_condition": lambda game: all(game.has_in_inventory(f"hint_fragment_{i}") for i in range(1, 14))
    },
    {
        "id": "hint3",
        "name": "hint 3",
        "location": Location.STAIRWELL,
        "movable": True,
        "visible": False,
        "carried": False,
        "description": "hint 3",
        "on_read": read_text("49 6E 20 6F 72 64 65 72 20 74 6F 20 66 69 6E 64 20 77 68 61 74 20 79 6F 75 20 6D 61 79 20 62 65 20 6C 6F 6F 6B 69 6E 67 20 66 6F 72 2C 20 69 74 20 6D 61 79 20 62 65 20 68 69 64 69 6E 67 20 69 6E 20 70 6C 61 69 6E 20 73 69 67 68 74 2E 20 50 65 72 68 61 70 73 20 61 6C 6C 20 74 68 6F 73 65 20 65 6D 70 74 79 20 68 61 6C 6C 77 61 79 73 20 79 6F 75 20 77 65 6E 74 20 70 61 73 74 20 77 65 72 65 6E 27 74 20 73 6F 20 69 6E 73 69 67 6E 69 66 69 63 61 6E 74 20 61 74 20 61 6C 6C 3F")
    },
    {
        "id": "door",
        "name": "door",
        "location": Location.HALLWAY_13,
        "movable": False,
        "visible": True,
        "carried": False,
        "description": "a large door...",
    },
    {
        "id": "finished_puzzle",
        "name": "puzzle (4/4)",
        "location": Location.STAIRWELL,
        "container": "puzzle_3",
        "movable": True,
        "visible": False,
        "carried": False,
        "description": "a finished puzzle, what does it do?",
    },
    {
        "id": "puzzle_piece_4",
        "name": "puzzle piece 4",
        "location": Location.SUPPLY_2,
        "movable": True,
        "visible": False,
        "carried": False,
        "description": "another puzzle piece...",
        "visibility_condition": lambda game: game.get_flag("fire_extinguished")
    },
    {
        "id": "key",
        "name": "key",
        "location": Location.STAIRWELL,
        "container": "finished_puzzle",
        "movable": True,
        "visible": False,
        "carried": False,
        "description": "a golden key",
    },
    {
        "id": "magnifying_glass",
        "name": "magnifying glass",
        "location": Location.HALLWAY_13,
        "movable": True,
        "visible": False,
        "carried": False,
        "description": "a magnifying glass",
        "visibility_condition": lambda game: game.get_object("hint3").carried
    },
    {
        "id": "broom",
        "name": "broom",
        "location": Location.SUPPLY_1,
        "movable": True,
        "visible": True,
        "carried": False,
        "description": "a broom",
    },
    {
        "id": "bucket",
        "name": "bucket",
        "location": Location.SUPPLY_1,
        "movable": True,
        "visible": True,
        "carried": False,
        "description": "an empty bucket",
    },
    {
        "id": "bucket_filled",
        "name": "water bucket",
        "location": Location.SUPPLY_2,
        "container": "bucket",
        "movable": True,
        "visible": False,
        "carried": False,
        "description": "a bucket filled with water",
    },
    {
        "id": "trapdoor",
        "name": "trapdoor",
        "location": Location.HALLWAY_10,
        "movable": False,
        "visible": False,
        "carried": False,
        "description": "a trapdoor",
        "visibility_condition": lambda game: game.get_object("magnifying_glass").carried
    },
    {
        "id": "water",
        "name": "water",
        "location": Location.SUPPLY_2,
        "movable": False,
        "visible": True,
        "carried": False,
        "description": "water",
    },
    {
        "id": "lighter",
        "name": "lighter",
        "location": Location.SUPPLY_1,
        "movable": True,
        "visible": True,
        "carried": False,
        "description": "a lighter, maybe you could light a fire with this?",
    },
]
