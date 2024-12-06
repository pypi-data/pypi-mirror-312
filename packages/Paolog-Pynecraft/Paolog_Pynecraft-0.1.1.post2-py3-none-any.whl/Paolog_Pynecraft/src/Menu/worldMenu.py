from ...src.UI.text import PyneText
from ...src.UI.button import PyneButton

from ...src.Menu.world.worldCreationMenu import PyneWorldCreationMenu
from ...src.Menu.world.worldRegenerationMenu import PyneWorldRegenerationMenu

from ursina import color

from ...src.other.get_config_path import get_pynecraft_config_path as conf_path
from ...src.other.settings import get_key_value, hive_exists, key_exists
from ...src.other.world_status import WORLD_STATUS

from ...src.Games.Solo.Pynecraft import Pynecraft

import os

class PyneWorldMenu:
    def __init__(self, menu_manager):
        self.menu_manager = menu_manager
        self.main_menu = self.menu_manager.current_menu
        self.worlds = []

        self.selWorldText = PyneText(text="Select World", xPos=-.3, yPos=.45, scale=2.5)

        self.moreWorldText = PyneText(text="More", xPos=.3, yPos=.45, scale=2.5)
        self.creWorldButton = PyneButton(text="Create a new world", xPos=.3, yPos=.35, ySize=.07, xSize=.4, onClick=self.__createWorldMenu)
        self.regWorldButton = PyneButton(text="Regenerate a world", xPos=.3, yPos=.25, ySize=.07, xSize=.4, onClick=self.__regenerateWorldMenu)

        self.backButton = PyneButton(text="Back",xPos=-.65,yPos=.45,ySize=.07,xSize=.2,onClick=self.__mainMenu, tooltip="Navigate to the menu that you were before")

    def update(self):
        pass
    
    def input(self, key):
        if key == "escape":
            self.__mainMenu()

    def show(self):
        self.__initWorlds()
        self.selWorldText.enabled = True
        self.moreWorldText.enabled = True
        self.creWorldButton.enabled = True
        self.regWorldButton.enabled = True
        self.backButton.enabled = True
        for button in self.worlds:
            button.enabled = True
        
        self.menu_manager.bg.show()

    def hide(self):
        self.selWorldText.enabled = False
        self.moreWorldText.enabled = False
        self.creWorldButton.enabled = False
        self.regWorldButton.enabled = False
        self.backButton.enabled = False
        
        for button in self.worlds:
            button.enabled = False
        
        self.menu_manager.bg.hide()

    def __initWorlds(self):
        self.worlds.clear()
        subfolders = [f.path for f in os.scandir(conf_path() + "/worlds") if f.is_dir()]

        userName:str
        if not hive_exists("PYNECRAFT", "USER") or not key_exists("PYNECRAFT", "USER", "USERNAME"):
            userName = "Rick"
        else:
            userName = get_key_value("PYNECRAFT", "USER", "USERNAME")
            # Check if userName is null or empty
            if not userName:
                userName = "Rick"


        for sf in subfolders:
            worldStatus = self.__isValidWorld(sf)
            if worldStatus == WORLD_STATUS.VALID:
                self.worlds.append(
                    PyneButton(
                        text=os.path.basename(sf),
                        xPos=-.3,
                        yPos=.45-(((len(self.worlds) + 1)/10)),
                        ySize=.07,
                        xSize=.4,
                        onClick=lambda name=sf: self.menu_manager.set_menu(Pynecraft(self.menu_manager, name, userName))
                    )
                )
            elif worldStatus == WORLD_STATUS.NEWER:
                worldButton = PyneButton(
                    text=os.path.basename(sf) + " - Newer World?",
                    xPos=-.3,
                    yPos=.45-(((len(self.worlds) + 1)/10)),
                    ySize=.07,
                    xSize=.4,
                    onClick=lambda name=sf: self.menu_manager.set_menu(Pynecraft(self.menu_manager, name, userName))
                )
                worldButton.button.color = color.red
                worldButton.button.text_color_setter(color.white)
                self.worlds.append(worldButton)
            elif worldStatus == WORLD_STATUS.DEPRECATED:
                worldButton = PyneButton(
                    text=os.path.basename(sf) + " - Need to be converted",
                    xPos=-.3,
                    yPos=.45-(((len(self.worlds) + 1)/10)),
                    ySize=.07,
                    xSize=.4,
                    onClick=lambda name=sf: self.menu_manager.set_menu(Pynecraft(self.menu_manager, name, userName))
                )
                worldButton.button.color = color.orange
                self.worlds.append(worldButton)
            elif worldStatus == WORLD_STATUS.INVALID:
                # Invalid world, won't create button
                pass
                

        
    def __mainMenu(self):
        self.menu_manager.set_menu(self.main_menu)
    
    def __createWorldMenu(self):
        self.menu_manager.set_menu(PyneWorldCreationMenu(self.menu_manager))
    
    def __regenerateWorldMenu(self):
        self.menu_manager.set_menu(PyneWorldRegenerationMenu(self.menu_manager))
    
    def __isValidWorld(self, folder:str) -> WORLD_STATUS:
        try:
            with open(folder + "/info.txt") as file:
                lines:list[str] = file.readlines()
                for line in lines:
                    line:str = line.strip()
                    if line:
                        variable, value = line.split("=")
                        if variable == "world_version" and int(value) == 1:
                            return WORLD_STATUS.VALID
                        elif int(value) >= 1:
                            return WORLD_STATUS.NEWER
                        elif int(value) <= 1:
                            return WORLD_STATUS.DEPRECATED
                        else:
                            return WORLD_STATUS.INVALID

        except FileNotFoundError:
            # No info.txt file, which means Pynecraft world isn't valid
            return WORLD_STATUS.INVALID