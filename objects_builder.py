from GameObject import GameObject

def normalize(text):
    """Normalize text for robust lookup (lowercase, remove spaces/underscores)."""
    return text.lower().replace(" ", "").replace("_", "")

def build_objects(object_defs):
    objects = {}
    name_to_id = {}

    # Pass 1: create all objects
    for d in object_defs:
        obj = GameObject(
            d["name"],
            d["location"],
            d["movable"],
            d["visible"],
            d["carried"],
            d["description"],
            d.get("glueable", False),
            d.get("on_read", None),
        )
        objects[d["id"]] = obj

        # Map normalized name → canonical id
        norm_name = normalize(d["name"])
        name_to_id[norm_name] = d["id"]

    # Pass 2: resolve string-based locations
    for d in object_defs:
        loc = d["location"]
        if isinstance(loc, str):
            if loc in objects:  # if it's another object
                objects[d["id"]].location = objects[loc]
            else:  # otherwise assume it's a room
                objects[d["id"]].location = rooms[loc]  # <-- you need a rooms dict

    return objects, name_to_id


# Optional helper for easier access
def get_object(objects, obj_id):
    if obj_id not in objects:
        raise KeyError(f"No object with id '{obj_id}' found")
    return objects[obj_id]
