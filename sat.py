from z3 import *
import config
from config import *


def indizio(game, is_tutto):
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
    sicuramente_mine = []
    sicuramente_sicuri = []

    for cube_id, var in vars.items():
        solver.push()
        solver.add(var == False)
        if solver.check() == unsat:
            sicuramente_mine.append(cube_id)
        solver.pop()

        solver.push()
        solver.add(var == True)
        if solver.check() == unsat:
            sicuramente_sicuri.append(cube_id)
        solver.pop()
        
    if is_tutto:
        if sicuramente_sicuri:
            return sicuramente_sicuri[0]
        return None

    if sicuramente_mine:
        if DEBUG:
            print(f'Indizio: {sicuramente_mine[0]} è sicuramente una mina!')
        return ('mina', sicuramente_mine[0])
    elif sicuramente_sicuri:
        if DEBUG:
            print(f'Indizio: {sicuramente_sicuri[0]} è sicuramente sicuro.')
        return ('sicuro', sicuramente_sicuri[0])
    else:
        if DEBUG:
            print("Nessun indizio certo disponibile.")
        return None


def risolvi(game):
    solver = Solver()
    vars = {}

    # Crea variabili per tutti i cubi non rivelati e non flaggati
    for cube in config.cubes_dict.values():
        if not cube.is_revealed and not cube.is_flagged:
            vars[cube.id] = Bool(cube.id)

    # Vincoli derivati dai cubi rivelati
    for cube in config.cubes_dict.values():
        if cube.is_revealed:
            neighbors = cube.get_neighbors()
            unknown_neighbors = [
                vars[n.id] for n in neighbors if not n.is_revealed and not n.is_flagged
            ]
            if unknown_neighbors:
                solver.add(Sum([If(var, 1, 0) for var in unknown_neighbors]) == cube.count)

    # Trova tutti i cubi sicuramente sicuri o mine
    indizi = []

    for cube_id, var in vars.items():
        solver.push()
        solver.add(var == False)
        if solver.check() == unsat:
            indizi.append(('mina', cube_id))
        solver.pop()

        solver.push()
        solver.add(var == True)
        if solver.check() == unsat:
            indizi.append(('sicuro', cube_id))
        solver.pop()

    if DEBUG:
        if indizi:
            print("Indizi trovati:")
            for tipo, id in indizi:
                print(f" - {id} è sicuramente {tipo}")
        else:
            print("Nessun indizio certo disponibile.")

    return indizi

from time import sleep

def tutto_tu(game):
    config.flag_mode = False

    def elimina_prossimo():
        indizio_ora = indizio(game, True)
        if not indizio_ora:
            print("hell nah")
            return

        x, y, z = map(int, indizio_ora.split('_'))
        cube = config.cubes_dict.get((x, y, z))
        if not cube:
            print("niente cube trovato")
            return

        print(f'eliminando cube: {cube.id}')
        cube.check_onclick()    # qui il cubo viene rimosso
        # ora invochiamo di nuovo questa stessa funzione fra 0.2 secondi
        invoke(elimina_prossimo, delay=0.2)

    # lancio la prima
    elimina_prossimo()