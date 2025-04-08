from ursina import *
from game import Game
from ui import UI


app = Ursina()

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

app.run()