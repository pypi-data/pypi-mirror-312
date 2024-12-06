from ...src.UI.background import PyneBackground
from ...src.other.audio_manager import PyneMusicManager

from ...src.other.settings import node_exists, hive_exists, key_exists, get_key_value

from ursina import window

class PyneMenuManager:
    def __init__(self):
        self.current_menu = None
        self.old_menu = None
        self.bg = PyneBackground()
        self.music_manager = PyneMusicManager()

        # Load Music Manager
        if node_exists("PYNECRAFT") and hive_exists("PYNECRAFT", "SOUNDS") and key_exists("PYNECRAFT", "SOUNDS", "PLAY_MUSIC"):
            play_music:bool = get_key_value("PYNECRAFT", "SOUNDS", "PLAY_MUSIC")
            if play_music == "True": self.music_manager.start()
            else: self.music_manager.stop()
        
        # Load fullscreen settings
        if not node_exists("PYNECRAFT") or not hive_exists("PYNECRAFT", "WINDOW") or not key_exists("PYNECRAFT", "WINDOW", "FULLSCREEN"):
            window.fullscreen = False
        else:
            window.fullscreen = False if get_key_value("PYNECRAFT", "WINDOW", "FULLSCREEN") == "False" else True

    def set_menu(self, menu):
        self.old_menu = self.current_menu
        if self.current_menu is not None:
            self.current_menu.hide()  # Hide the current menu
        self.current_menu = menu
        self.current_menu.show()  # Show the new menu

    def update(self):
        if self.current_menu is not None:
            self.current_menu.update()
        
        self.bg.update()
        self.music_manager.update()
    
    def input(self, key):
        if self.current_menu is not None:
            self.current_menu.input(key)
    
    def go_back(self):
        self.set_menu(self.old_menu)