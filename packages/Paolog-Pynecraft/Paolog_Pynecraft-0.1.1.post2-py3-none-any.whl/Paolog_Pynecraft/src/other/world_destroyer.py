from ...src.other.get_config_path import get_pynecraft_config_path as conf_path

from threading import Thread

import os
import shutil

class WorldDestroyer:
    def __init__(self):
        self.progression:int = 0
    
    def delete_world(self, world_name:str) -> None:
        process:Thread = Thread(target=self.__delete_world, args=(world_name,))
        process.start()
    
    def __delete_world(self, world_name:str) -> None:
        self.progression = 0
        try:
            world_folder = conf_path() + f"/worlds/{world_name}"
            if not os.path.exists(world_folder):
                self.progression = -1
                return
            if os.path.isfile(world_folder):
                self.progression = -2
                return

            shutil.rmtree(world_folder)

            self.progression = 100
        except OSError:
            self.progression = -100
    
    def get_progression(self) -> int:
        return self.progression