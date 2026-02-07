from location_ids import Location, LocationData

LOCATIONS: dict[Location, LocationData] = {

    Location.CELL_1: LocationData(
        "Cell (Room 1)",
        """Benny wakes up in a dark room. He realizes that Fala and Nodo have locked him in the castle jail. Unfortunately, it seems like the great evil has possessed them and decided to lock him up for good. Luckily for him, the guards may have forgotten to lock the cell door behind them! The room looks dilapidated, like nobody’s bothered to maintain it since there hasn’t been any prisoners for years. 

Cobwebs are scattered around the room, and it looks like the cell is bigger than he thought. There’s a table in the corner, with an old looking scroll that might be made from papyrus. Under the table, he can see a puzzle piece. It seems like the hidden puzzles he heard about when he was being transported into the cell were real. He might have a shot at escaping."""
    ),

    Location.CELL_2: LocationData(
        "Cell (Room 2)",
        "Unfortunately for Benny, in the next room he can’t see anything obvious. He thinks he might have to come back later in case there’s something hidden in the room that he can’t see right now. It feels like there might be something hidden in this room."
    ),

    Location.CELL_3: LocationData(
        "Cell (Room 3)",
        "Benny realizes that this cell he’s in right now is really big. It still looks about the same as the other two rooms, lots of cobwebs and some various scattered furniture pieces. This room seems special, though. There’s a pedestal in the middle with a puzzle on it? Yep. Looks like a puzzle. Maybe this will help him escape?"
    ),

    Location.HALLWAY_1: LocationData("Hallway (Room 1)", "Benny finds himself in a hallway that doesn’t quite seem to have an end to it. He thinks nothing of it, as it appears just to be a hallway."),
    Location.HALLWAY_2: LocationData("Hallway (Room 2)", "Still looks like a hallway."),
    Location.HALLWAY_3: LocationData("Hallway (Room 3)", "At last, Benny finds a turn in the corridor. Maybe he’ll find something hidden in the next room?"),
    Location.HALLWAY_4: LocationData("Hallway (Room 4)", "Benny is still in a hallway, but it looks like he’s finally getting somewhere. He can see a room to his left. Maybe he should investigate it?"),

    Location.VAULT_1: LocationData(
        "Vault (Room 1)",
        "Benny finds himself in another room. It looks like it could be one of the vaults... nice wood floors and well kept bricks instead."
    ),

    Location.VAULT_2: LocationData(
        "Vault (Room 2)",
        "Benny finds a little room with some shelves behind the counter, with a small box on one of the shelves."
    ),

    Location.VAULT_3: LocationData(
        "Vault (Room 3)",
        "Benny finds himself in the actual heart of the vault. There’s a small safe here, but he doesn’t have the combination yet."
    ),

    Location.VAULT_4: LocationData(
        "Vault (Room 4)",
        "There seems to be lots of gold and silver in this room. Oh look — an engraving on one of the gold bars and a little piece of paper."
    ),

    Location.HALLWAY_5: LocationData("Hallway (Room 5)", "Another corner, this time it’s a right turn."),
    Location.HALLWAY_6: LocationData("Hallway (Room 6)", "Still in a straight hallway, how long even is this?"),
    Location.HALLWAY_7: LocationData("Hallway (Room 7)", "How can there be such a long hallway? It feels impractical."),
    Location.HALLWAY_8: LocationData("Hallway (Room 8)", "It's yet another straight hallway... Why?"),
    Location.HALLWAY_9: LocationData("Hallway (Room 9)", "This hallway feels endless. When will it end?"),
    Location.HALLWAY_10: LocationData("Hallway (Room 10)", "SERIOUSLY!?!? MORE HALLWAY!?!?"),
    Location.HALLWAY_11: LocationData("Hallway (Room 11)", "WHAT THE HECK? THIS HALLWAY WILL NEVER END..."),
    Location.HALLWAY_12: LocationData("Hallway (Room 12)", "Another right turn... maybe this is finally the end?"),
    Location.HALLWAY_13: LocationData("Hallway (Room 13)", "There’s a fork in the road and a locked door. How is he going to get a key?"),

    Location.SUPPLY_1: LocationData(
        "Supply Closet (Room 1)",
        "There's a broom, bucket, and lighter here. Looks like some kind of weird puzzle setup."
    ),

    Location.SUPPLY_2: LocationData(
        "Supply Closet (Room 2)",
        "The closet seems to have a small tub of water in it. Maybe that will somehow be helpful?"
    ),

    Location.STAIRWELL: LocationData(
        "Stairwell",
        "At last, Benny finds himself at the stairwell. He can escape now, thanks to you."
    ),
}