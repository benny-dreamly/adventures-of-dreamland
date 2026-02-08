class GameObject:

    def __init__(self, obj_id, name, location, movable, visible, carried, description, glueable=False, on_read=None, container=None, progression_locked=False, visibility_condition=None):
        self.id = obj_id
        self.name  = name
        self.location = location
        self.container = container
        self.movable = movable
        self.visible = visible
        self.carried = carried
        self.description  = description
        self.glueable = glueable
        self.on_read = on_read
        self.progression_locked = progression_locked
        self.visibility_condition = visibility_condition
