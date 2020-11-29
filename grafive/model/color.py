from enum import Enum
import random

class Color(Enum):
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    BLACK = "black"
    PINK = "pink"
    WHITE = "white"
    OLIVE = "olive"
    YELLOW = "yellow"
    CYAN = "cyan"
    MAGENTA = "magenta"


def iterate_colors() -> Color:
    for color in list(Color):
        yield color

def random_unique_color():
    colors = set()
    r = lambda: random.randint(0,255)

    while True:
        color_hex = ('#%02X%02X%02X' % (r(),r(),r())) 

        while color_hex in colors:
            color_hex = ('#%02X%02X%02X' % (r(),r(),r()))
        
        colors.add(color_hex)

        yield color_hex
