from z3 import *
import config
from config import *


def indizio(game):
    solver = Solver()
    vars = {}

    # Creiamo una variabile booleana per ogni cubo non rivelato
    for cube in config.cubes_dict.values():
        if not cube.is_revealed and not cube.is_flagged:
            vars[cube.id] = Bool(cube.id)

    # Costruiamo vincoli per ogni cubo rivelato
    for cube in config.cubes_dict.values():
        if cube.is_revealed:
            neighbors = cube.get_neighbors()
            unknown_neighbors = [
                vars[n.id] for n in neighbors if not n.is_revealed and not n.is_flagged
            ]

            if unknown_neighbors:
                solver.add(Sum([If(var, 1, 0) for var in unknown_neighbors]) == cube.count)

    # Troviamo i cubi sicuramente sicuri o sicuramente mine
    certe_mine = []
    sicuramente_sicuri = []

    for cube_id, var in vars.items():
        solver.push()
        solver.add(var == False)
        if solver.check() == unsat:
            certe_mine.append(cube_id)
        solver.pop()

        solver.push()
        solver.add(var == True)
        if solver.check() == unsat:
            sicuramente_sicuri.append(cube_id)
        solver.pop()

    if certe_mine:
        if DEBUG:
            print(f'Indizio: {certe_mine[0]} è sicuramente una mina!')
        return ('mina', certe_mine[0])
    elif sicuramente_sicuri:
        if DEBUG:
            print(f'Indizio: {sicuramente_sicuri[0]} è sicuramente sicuro.')
        return ('sicuro', sicuramente_sicuri[0])
    else:
        if DEBUG:
            print("Nessun indizio certo disponibile.")
        return None


def risolvi(game):
    # Troviamo gli indizi
    indizi = []
    
    # ???

    return indizi
