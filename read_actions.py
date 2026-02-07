import services

def read_text(*lines):
    def action():
        if services.print_fn is None:
            raise RuntimeError("UI not registered")
        for line in lines:
            services.print_fn(line)
    return action


def read_image(image_name):
    def action():
        if services.show_image_fn is None:
            raise RuntimeError("UI not registered")
        services.show_image_fn(image_name)
    return action
