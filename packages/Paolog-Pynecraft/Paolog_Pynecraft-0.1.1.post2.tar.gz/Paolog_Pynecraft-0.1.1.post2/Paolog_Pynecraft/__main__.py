from .src.Graphics.window import PyneWindow

from .src.Menu.mainMenu import PyneMainMenu
from .src.other.menu_manager import PyneMenuManager

from .src.other.get_config_path import get_pynecraft_config_path as conf_path
from .src.other.setup import setup_pynecraft

import os

# Initialize Window, MenuManager and MainMenu
window = PyneWindow(
    "Pynecraft", # Title
    True, # Enabled Editor UI
    False, # Disable ursina's exit button
    'assets/rs/window/icon.ico', # Application icon
    False, # App with the default os border
    False, # App isn't always on top
    True, # Enabled COGMenu
    True # Enable Startup Screen
)

menu_manager = PyneMenuManager()
pyneMainMenu = PyneMainMenu(menu_manager)
menu_manager.set_menu(pyneMainMenu)

# Update and Input functions

def update():
    menu_manager.update()

def input(key):
    menu_manager.input(key=key)

# Check if Pynecraft base settings exists. If it doesn't, create them
if not os.path.exists(conf_path()):
    setup_pynecraft()

# Run the app
window.run()

"""
python3 -bc "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"; python3 -Bc "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]"
"""
