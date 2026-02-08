from GameObject import GameObject

def build_objects(object_defs):
    objects = {}

    # --- Pass 1: create all objects without worrying about string references ---
    for d in object_defs:
        obj = GameObject(
            name=d["name"],
            location=d["location"],  # keep as-is for now
            movable=d["movable"],
            visible=d["visible"],
            carried=d["carried"],
            description=d["description"],
            glueable=d.get("glueable", False),
            on_read=d.get("on_read", None),
        )
        objects[d["id"]] = obj

    # --- Pass 2: resolve string-based locations ---
    for d in object_defs:
        loc = d["location"]
        if isinstance(loc, str):
            if loc not in objects:
                raise KeyError(f"Object '{d['id']}' references unknown location '{loc}'")
            objects[d["id"]].location = objects[loc]
        # If location is None or a real Location enum, leave as-is

    return objects


# Optional helper for easier access
def get_object(objects, obj_id):
    if obj_id not in objects:
        raise KeyError(f"No object with id '{obj_id}' found")
    return objects[obj_id]
