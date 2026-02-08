from GameObject import GameObject

def normalize(text):
    """Normalize text for robust lookup (lowercase, remove spaces/underscores)."""
    return text.lower().replace(" ", "").replace("_", "")

def build_objects(object_defs):
    objects = {}
    name_to_id = {}

    # --- Pass 1: create all objects ---
    for d in object_defs:
        obj = GameObject(
            obj_id=d["id"],
            name=d["name"],
            location=d["location"],
            movable=d["movable"],
            visible=d["visible"],
            carried=d["carried"],
            description=d["description"],
            glueable=d.get("glueable", False),
            on_read=d.get("on_read", None),
            progression_locked=d.get("progression_locked", False)
        )
        objects[d["id"]] = obj

        # Map normalized name → canonical id
        norm_name = d["name"].lower().replace(" ", "").replace("_", "")
        name_to_id[norm_name] = d["id"]

    # --- Pass 2: resolve containers ---
    for d in object_defs:
        container_id = d.get("container")
        if container_id:
            if container_id not in objects:
                raise KeyError(f"Object '{d['id']}' references unknown container '{container_id}'")
            objects[d["id"]].container = objects[container_id]  # do NOT touch location

    return objects, name_to_id


# Optional helper for easier access
def get_object(objects, obj_id):
    if obj_id not in objects:
        raise KeyError(f"No object with id '{obj_id}' found")
    return objects[obj_id]
