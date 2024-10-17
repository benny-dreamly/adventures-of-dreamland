class GameObject:

    def __init__(self, name, location, movable, visible, carried, description, glueable=False):
        self.name  = name
        self.location = location
        self.movable = movable
        self.visible = visible
        self.carried = carried
        self.description  = description
        self.glueable = glueable

    def to_dict(self):
        def serialize(value):
            # Check if the value is a GameObject and convert it to dict recursively
            if isinstance(value, GameObject):
                return value.to_dict()
            return value

        return {
            'name': self.name,
            'location': serialize(self.location),  # If location is a GameObject, it will be converted
            'movable': self.movable,
            'visible': self.visible,
            'carried': self.carried,
            'description': self.description,
            'glueable': self.glueable
        }