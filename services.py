print_fn = None
show_image_fn = None


def register_ui(print_func, image_func):
    global print_fn, show_image_fn
    print_fn = print_func
    show_image_fn = image_func
