class GameObject:

    def __init__(self, name, location, movable, visible, carried, description, glueable=False):
        self.name  = name
        self.location = location
        self.movable = movable
        self.visible = visible
        self.carried = carried
        self.description  = description
        self.glueable = glueable
