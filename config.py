from ursina import *
from random import randint

# Variabili globali
DEBUG = False

flag_mode = False
cubes_dict = {}

side = 0.5
gap = 0.08
colors = {
    1: color.green,
    2: color.yellow,
    3: color.orange,
    4: color.cyan,
    5: color.magenta,
}
rand_color = randint(1, 5)

rotation_speed = 50
zoom_speed = 0.2
min_zoom = 1
max_zoom = 50

LINE_LENGTH = 1000
LINE_THICKNESS = 0.05

# Variabili iniziali (possono essere modificate dal menu)
dim = 5
difficulty = 0.05