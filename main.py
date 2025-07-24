from ursina import *
from game import Game
from ui import UI
from ursina.shaders import lit_with_shadows_shader


app = Ursina()

Entity.default_shader = lit_with_shadows_shader

# Impostazioni finestra
window.title = 'Minesweeper3D'
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True
window.color = color.black

# Inizializza il gioco e l'interfaccia utente
ui = UI()
game = Game(ui)


def update():
    ui.update()

def input(key):
    ui.input(key)


ambient_light = AmbientLight()
ambient_light.color = color.rgb(100, 100, 100)

# Inizializza
app.run()