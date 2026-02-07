from GameObject import GameObject

def build_objects(object_defs):
    objects = {}

    # Pass 1: create all objects
    for d in object_defs:
        obj = GameObject(
            d["name"],
            d["location"],   # Location or str (fixed later)
            d["movable"],
            d["visible"],
            d["carried"],
            d["description"],
            d.get("glueable", False),
        )
        objects[d["id"]] = obj

    # Pass 2: resolve string-based locations
    for d in object_defs:
        loc = d["location"]
        if isinstance(loc, str):
            objects[d["id"]].location = objects[loc]

    return objects
