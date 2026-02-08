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

        # container resolved later
        obj.container = None

        objects[d["id"]] = obj

        # Map normalized name → canonical id
        norm_name = normalize(d["name"])
        name_to_id[norm_name] = d["id"]

        # ---------- Pass 2: resolve containers ----------
        for d in object_defs:
            container_id = d.get("container")
            if container_id:
                if container_id not in objects:
                    raise KeyError(
                        f"Object '{d['id']}' references unknown container '{container_id}'"
                    )
                objects[d["id"]].container = objects[container_id]

        # ---------- Pass 3: sanity-check locations ----------
        for obj_id, obj in objects.items():
            if not hasattr(obj.location, "name"):
                raise TypeError(
                    f"Object '{obj_id}' has invalid location '{obj.location}'. "
                    "Expected a Location enum."
                )

    return objects, name_to_id


# Optional helper for easier access
def get_object(objects, obj_id):
    if obj_id not in objects:
        raise KeyError(f"No object with id '{obj_id}' found")
    return objects[obj_id]
