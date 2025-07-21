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
        self.count = 0
        self.text_entity = Text(
            text='',
            position=self.position,
            scale=20 * side,
            parent=self.game.pivot,
            color=color.white,
            visible= False
        )

    
    def get_neighbors(self):
        x, y, z = map(int, self.id.split('_'))
        neighbors = []
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                for k in range(z - 1, z + 2):
                    if (i, j, k) == (x, y, z):
                        continue
                    cube = config.cubes_dict.get((i, j, k))
                    if cube:
                        neighbors.append(cube)
        return neighbors
    
    def check_onclick(self):
        if self.is_flagged:
                return
            
        if self.is_mine:
            if DEBUG:
                print('Game Over!')
            self.game.game_over()

                    
        if self.count == 0:
            self.game.flood_fill(
                int(self.id.split('_')[0]),
                int(self.id.split('_')[1]),
                int(self.id.split('_')[2])
            )
        else:
            destroy(self.text_entity)
            self.text_entity = Text(
                text=str(self.count),
                position=self.position,
                parent=self.game.pivot,
                scale=side * 20,
                billboard=True,
                color=color.white,
            )
            
            self.is_revealed = True
        
        if DEBUG:
            print(f'Clicked {self.id}, Mines around: {self.count}, Is mine: {self.is_mine}, Revealed {self.is_revealed}, count: {self.count}')
        
        self.update_count_display()
        self.disable()
        self.is_won()
        
    
    def on_click(self):
        
        if DEBUG:
            print(f'Clicked on {self.id}, with count {self.count}')

        if config.flag_mode:
            if DEBUG:
                print('Is mine:', self.is_mine)

            self.is_flagged = not self.is_flagged
            self.color = color.red if self.is_flagged else \
                lerp(color.black, colors[rand_color], random.uniform(.3 , .9))
            
            self.is_won() # qua non funziona
            
            for neighbor in self.get_neighbors():
                if self.is_flagged:
                    neighbor.count -= 1
                    if neighbor.count == 0:
                        neighbor.text_entity.visible = False
                    else:
                        neighbor.text_entity.visible = True
                    neighbor.update_count_display()
                        
                else:
                    neighbor.count += 1
                    if neighbor.count == 0:
                        neighbor.text_entity.visible = False
                    else:
                        neighbor.text_entity.visible = True
                    neighbor.update_count_display()
    
        else:
            self.check_onclick()


    def update_count_display(self):
        self.text_entity.text = str(self.count)

    def is_won(self):
        if DEBUG:
            print('Checking win condition')
            
        not_revealed_cubes = self.game.get_not_revealed_cubes()
        if DEBUG:
            print(f'Not revealed cubes: {not_revealed_cubes}')

        if len(not_revealed_cubes) == self.game.mines or (not_revealed_cubes == [] and self.is_mine):
            if DEBUG:
                print('You won!')

            self.game.ui.game_won()


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
        
        config.cubes_dict = {}
        
        self.dim = dim
        self.mines = int(difficulty * dim * dim * dim)
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
                    config.cubes_dict[(x, y, z)] = cube
                    
        if DEBUG:
            print(f'Created {len(config.cubes_dict)} cubes')

        # Place mines
        for _ in range(self.mines):
            while True:
                x, y, z = randrange(dim), randrange(dim), randrange(dim)
                if not config.cubes_dict[(x,y,z)].is_mine:
                    config.cubes_dict[(x,y,z)].is_mine = True
                    break
        
        # Count mines around each cube
        for cube in config.cubes_dict.values():
            
            count = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    for k in range(-1, 2):
                        if (i, j, k) == (0, 0, 0):
                            continue
                        neighbor = config.cubes_dict.get((int(cube.id.split('_')[0]) + i,
                                                            int(cube.id.split('_')[1]) + j,
                                                            int(cube.id.split('_')[2]) + k)
                        )
                        if neighbor and neighbor.is_mine:
                            count += 1
            
            cube.count = count
            cube.text_entity.text = str(count)
            
            
            
            if DEBUG:
                print(f'Cube {cube.id} has {cube.count} mines around it')


    def flood_fill(self, x, y, z):
        if DEBUG:
            print(f'Flood fill from {x}, {y}, {z}')
        
        stack = [(x, y, z)]
        visited = set()
        
        while stack:
            cx, cy, cz = stack.pop()
            
            if (cx, cy, cz) in visited:
                continue
            
            visited.add((cx, cy, cz))
            cube = config.cubes_dict.get((cx, cy, cz))
            
            
            if not cube or cube.is_mine or cube.is_revealed:
                continue

            cube.is_revealed = True
            
            count = cube.count
            
            if count > 0:
                destroy(cube.text_entity)
                cube.text_entity = Text(
                    text=str(count),
                    position=cube.position,
                    scale=20 * side,
                    parent=self.pivot,
                    billboard=True
                )
            else:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        for dz in [-1, 0, 1]:
                            if dx == dy == dz == 0:
                                continue
                            nx, ny, nz = cx + dx, cy + dy, cz + dz
                            if (nx, ny, nz) not in visited and (
                                    0 <= nx < self.dim and 
                                    0 <= ny < self.dim and 
                                    0 <= nz < self.dim
                                ):
                                stack.append((nx, ny, nz))
            if cube:
                cube.disable()
        
        cube.is_won()


    def get_revealed_cubes(self):
        self.revealed_cubes.clear()
        for cube in config.cubes_dict.values():
            if cube.is_revealed:
                self.revealed_cubes.append((cube.id, cube.text_entity.text))
        return self.revealed_cubes


    def get_not_revealed_cubes(self):
        self.not_revealed_cubes.clear()
        for cube in config.cubes_dict.values():
            if not cube.is_revealed:
                self.not_revealed_cubes.append((cube.id))
        return self.not_revealed_cubes


    def game_over(self):
        self.ui.game_over()

