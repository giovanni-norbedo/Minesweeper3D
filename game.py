import sys
import math
from random import randrange, uniform
from functools import partial
from ursina import *
from config import *
import config


class Cube(Entity):
    def __init__(self, position, id, game, **kwargs):
        random_variable = random.uniform(.3 , .9)
        super().__init__(
            model='cube',
            color=lerp(color.black, colors[rand_color], random_variable),
            scale=(side - gap, side - gap, side - gap),
            position=position,
            parent=scene,
            collider='box',
            is_mine=False,
            **kwargs
        )
        self.id = id
        self.game = game
        self.is_flagged = False
        self.is_revealed = False
        self.text_entity = Text(
            text='',
            position=self.position,
            parent=self,
            scale=0.1,
            visible=False
        )


    def reveal(self):
        if self.is_flagged:
            return
        
        x, y, z = map(int, self.id.split('_'))
        count = 0
        self.is_revealed = True
        
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                for k in range(z - 1, z + 2):
                    if (i, j, k) == (x, y, z):
                        continue
                    cube = cubes_dict.get((i, j, k))
                    if cube and cube.is_mine:
                        count += 1
        
        if count > 0:
            self.text_entity = Text(
                text=str(count),
                position=self.position,
                scale=side * 20,
                parent=self.game.pivot,
                billboard=True,
                color=color.white
            )
            self.initial_value = count
        else:
            self.game.flood_fill(x, y, z)
        
        if DEBUG:
            print(f'Clicked {self.id}, Mines around: {count}, Is mine: {self.is_mine}, Revealed {self.is_revealed}')
        
        self.disable()

        if self.is_mine:
            print('Game Over!')
            self.game.game_over()
    
    
    def get_neighbors(self):
        x, y, z = map(int, self.id.split('_'))
        neighbors = []
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                for k in range(z - 1, z + 2):
                    if (i, j, k) == (x, y, z):
                        continue
                    cube = cubes_dict.get((i, j, k))
                    if cube:
                        neighbors.append(cube)
        return neighbors
    
    
    def on_click(self):
        if config.flag_mode:
            self.is_flagged = not self.is_flagged
            self.color = color.red if self.is_flagged else color.black
            
            for cube in self.get_neighbors():
                if cube.is_revealed and hasattr(cube, 'text_entity'):
                    count = int(cube.text_entity.text)
                    if DEBUG:
                        print(cube.text_entity.text)
                    
                    if self.is_flagged:  
                        cube.text_entity.text = str(count - 1)
                        
                    else:  
                        if count < cube.initial_value:
                            cube.text_entity.text = str(count + 1)
        
        else:
            self.reveal()



class Game:
    def __init__(self, ui):
        self.ui = ui
        self.revealed_cubes = []
        self.not_revealed_cubes = []
        self.pivot = None
        self.dim = None


    def start_game(self, dim, difficulty):
        if DEBUG:
            print(f'Starting game with dimension {dim} and difficulty {difficulty}')
        
        global cubes_dict
        cubes_dict = {}
        
        self.dim = dim
        self.mines = difficulty * dim * dim * dim
        self.center = (dim - 1) * side / 2

        self.pivot = Entity(
            parent=scene,
            position=(self.center, self.center, self.center),
        )
        camera.parent = self.pivot
        
        if dim == 5:
            camera.position = (self.center, 20, self.center) 
        elif dim == 7:
            camera.position = (self.center, 23, self.center)
        elif dim == 9:
            camera.position = (self.center, 25, self.center)
        camera.look_at(self.pivot)

        for x in range(dim):
            for y in range(dim):
                for z in range(dim):
                    cube = Cube(
                        position=(x * side, y * side, z * side),
                        id=f'{x}_{y}_{z}',
                        game=self,
                    )
                    cube.parent = self.pivot
                    cubes_dict[(x, y, z)] = cube
                    
        if DEBUG:
            print(f'Created {len(cubes_dict)} cubes')

        for _ in range(int(self.mines)):
            while True:
                x, y, z = randrange(dim), randrange(dim), randrange(dim)
                if not cubes_dict[(x,y,z)].is_mine:
                    cubes_dict[(x,y,z)].is_mine = True
                    break 


    def flood_fill(self, x, y, z):
        stack = [(x, y, z)]
        visited = set()
        
        while stack:
            cx, cy, cz = stack.pop()
            
            if (cx, cy, cz) in visited:
                continue
            
            visited.add((cx, cy, cz))
            cube = cubes_dict.get((cx, cy, cz))
            cube.is_revealed = True
            
            if DEBUG:
                print(f'Popped {cube.id}, Revealed {cube.is_revealed}')
            
            if not cube or cube.is_mine:
                continue
            
            count = 0
            
            for i in range(cx - 1, cx + 2):
                for j in range(cy - 1, cy + 2):
                    for k in range(cz - 1, cz + 2):
                        if (i, j, k) == (cx, cy, cz):
                            continue
                        neighbor = cubes_dict.get((i, j, k))
                        if neighbor and neighbor.is_mine:
                            count += 1
            if count > 0:
                cube.text_entity = Text(
                    text=str(count),
                    position=cube.position,
                    scale=side * 20,
                    parent=self.pivot,
                    billboard=True
                )
                cube.initial_value = count
            else:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        for dz in [-1, 0, 1]:
                            if dx == dy == dz == 0:
                                continue
                            nx, ny, nz = cx + dx, cy + dy, cz + dz
                            if (nx, ny, nz) not in visited and (0 <= nx < dim and 0 <= ny < dim and 0 <= nz < dim):
                                stack.append((nx, ny, nz))
            if cube:
                cube.disable()


    def get_revealed_cubes(self):
        self.revealed_cubes.clear()
        for cube in cubes_dict.values():
            if cube.is_revealed:
                self.revealed_cubes.append((cube.id, cube.text_entity.text))
        return self.revealed_cubes


    def get_not_revealed_cubes(self):
        self.not_revealed_cubes.clear()
        for cube in cubes_dict.values():
            if not cube.is_revealed:
                self.not_revealed_cubes.append((cube.id))
        return self.not_revealed_cubes


    def game_over(self):
        self.ui.game_over()

