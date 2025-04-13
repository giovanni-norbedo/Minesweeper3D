from z3 import *
import config
from config import *

def indizio(game, cube, neighbors, revealed_cubes):
    solver = Solver()

    