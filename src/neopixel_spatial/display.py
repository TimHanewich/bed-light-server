from . import neopixel
from . import spatial

def display(pixels:neopixel.Neopixel, range:list[spatial.pixel], color:tuple(int, int, int)) -> None:
    for pix in range:
        pixels.set_pixel(pix.index, color)