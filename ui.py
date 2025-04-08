from ursina import *
from config import *
import config
from game import Game


class UI:
    def __init__(self):
        self.game = None
        self.game_panel = Entity(parent=scene, enabled=False)
        self.game_over_panel = Entity(parent=camera.ui, enabled=False)
        self.menu_panel = Entity(parent=camera.ui, enabled = True)
        
        self.game_over_text = Text(
            text='Game Over!',
            x=-0.15,
            y=0.15,
            scale=2,
            parent=camera.ui,
            visible=False
        )

        self.flag_text = Text(text="Flag mode OFF", position=(-0.7, 0.45), scale=2, color=color.white, parent=camera.ui)
        self.flag_text.visible = False

        self.selected_dimension = dim
        self.selected_difficulty = difficulty

        self.create_menu()
    
    
    def update(self):
        if not self.game_panel.enabled:
            return  # non fare nulla se il gioco è fermo

        # Movimento WASD
        if held_keys['w']:
            camera.position += camera.up * time.dt * 50
            camera.position += camera.forward * zoom_speed * .12
        
        if held_keys['s']:
            camera.position -= camera.up * time.dt * 50
            camera.position += camera.forward * zoom_speed * .12
        
        if held_keys['a']:
            camera.position -= camera.right * time.dt * 50
        
        if held_keys['d']:
            camera.position += camera.right * time.dt * 50
        
        # Zoom
        if held_keys['up arrow']:
            camera.world_position += camera.forward * zoom_speed
        
        if held_keys['down arrow']:
            camera.world_position -= camera.forward * zoom_speed
        
        # Mantiene la telecamera rivolta al centro
        camera.look_at(self.game.pivot)


    def input(self, key):
        if key == 'space':
            self.toggle_flag_mode()
            if DEBUG:
                print('Flag mode toggled')


    def create_menu(self):
        if hasattr(self, 'dimension_buttons'):
            for btn in self.dimension_buttons:
                destroy(btn)
        if hasattr(self, 'difficulty_buttons'):
            for btn in self.difficulty_buttons:
                destroy(btn)
        
        start_button = Button(
            text = 'Inizia Gioco',
            color = color.azure,
            parent = self.menu_panel,
            scale = .2,
            x = 0,
            y = -0.2,
            on_click = self.start_game_handler
        )

        easy_button = Button(
            text='Facile',
            color = color.azure,
            parent=self.menu_panel,
            scale=.15,
            x = -0.4,
            y = 0.2,
        )
        
        medium_button = Button(
            text='Medio',
            color = color.azure,
            parent=self.menu_panel,
            scale=.15,
            x = -0.1275,
            y = 0.2,
        )
        
        hard_button = Button(
            text='Difficile',
            color = color.azure,
            parent=self.menu_panel,
            scale=.15,
            x = 0.1275,
            y = 0.2,
        )
        
        extreme_button = Button(
            text='Estremo',
            color = color.azure,
            parent=self.menu_panel,
            scale=.15,
            x = 0.4,
            y = 0.2,
        )
        
        exit_button = Button(
            text='Esci',
            color = color.brown,
            parent=self.menu_panel,
            scale=.07,
            x = 0.7,
            y = -0.35,
            on_click=application.quit
        )

        self.difficulty_buttons = [easy_button, medium_button, hard_button, extreme_button]

        dimension_button0 = Button(
            text='5',
            color = color.violet,
            parent=self.menu_panel,
            scale=.10,
            x = -0.2,
            y = 0,
        )
        dimension_button1 = Button(
            text='7',
            color = color.violet,
            parent=self.menu_panel,
            scale=.10,
            x = 0,
            y = 0,
        )
        dimension_button2 = Button(
            text='9',
            color = color.violet,
            parent=self.menu_panel,
            scale=.10,
            x = 0.2,
            y = 0,
        )
        
        self.dimension_buttons = [dimension_button0, dimension_button1, dimension_button2]
        self.difficulty_buttons = [easy_button, medium_button, hard_button, extreme_button]

        dimension_button0.on_click = lambda: self.set_dimension(5, dimension_button0)
        dimension_button1.on_click = lambda: self.set_dimension(7, dimension_button1)
        dimension_button2.on_click = lambda: self.set_dimension(9, dimension_button2)

        easy_button.on_click = lambda: self.set_difficulty(0.05, easy_button)
        medium_button.on_click = lambda: self.set_difficulty(0.10, medium_button)
        hard_button.on_click = lambda: self.set_difficulty(0.15, hard_button)
        extreme_button.on_click = lambda: self.set_difficulty(0.20, extreme_button)

        start_button.on_click = self.start_game_handler
        exit_button.on_click = application.quit


    def start_game_handler(self):
        self.menu_panel.enabled = False
        self.game_panel.enabled = True
        self.flag_text.visible = True
        
        self.game = Game(self)
        self.game.start_game(self.selected_dimension, self.selected_difficulty)


    def game_over(self):
        self.game_panel.enabled = False
        self.game_over_panel.enabled = True
        self.flag_text.visible = False
        
        self.game_over_text.visible = True
        
        
        restart_button = Button(
            text = 'Restart game',
            color = color.red,
            parent = self.game_over_panel,
            scale = .2,
            x = 0,
            y = -0.2,
            on_click = self.restart_game
        )

        for btn in self.dimension_buttons:
            btn.color = color.violet

        for btn in self.difficulty_buttons:
            btn.color = color.azure


    def restart_game(self):
        if DEBUG:
            print("Restarting game...")
        
        destroy(self.game.pivot)
        cubes_dict = {}

        self.game_over_panel.enabled = False
        self.menu_panel.enabled = True
        self.game_over_text.visible = False
        
        self.create_menu()
        camera.position = (0,0,-10)


    def toggle_flag_mode(self):
        if self.game:
            config.flag_mode = not config.flag_mode
            self.flag_text.text = "Flag mode ON" if config.flag_mode else "Flag mode OFF"


    def set_dimension(self, value, selected_button):
        self.selected_dimension = value
        if DEBUG:
            print(f'Dimensione impostata a {value}')

        for btn in self.dimension_buttons:
            btn.color = color.violet
            print(f'Impostato {btn.text} a viola')

        selected_button.color = color.magenta
        print(f'Impostato {selected_button.text} a magenta')



    def set_difficulty(self, value, selected_button):
        self.selected_difficulty = value
        if DEBUG:
            print(f'Difficoltà impostata a {value}')

        for btn in self.difficulty_buttons:
            btn.color = color.azure

        selected_button.color = color.orange


    def toggle_flag_mode(self):
        config.flag_mode = not config.flag_mode
        self.flag_text.text = "Flag mode ON" if config.flag_mode else "Flag mode OFF"
        print(f'Modalità flag: {config.flag_mode}')