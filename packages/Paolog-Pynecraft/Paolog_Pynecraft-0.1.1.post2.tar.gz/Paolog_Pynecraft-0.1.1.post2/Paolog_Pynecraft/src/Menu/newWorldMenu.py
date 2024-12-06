from ...src.UI.text import PyneText
from ...src.UI.button import PyneButton

from ...src.Menu.world.worldCreationMenu import PyneWorldCreationMenu
from ...src.Menu.world.worldRegenerationMenu import PyneWorldRegenerationMenu
from ...src.Menu.world.worldDeletionMenu import PyneWorldDeletionMenu

from ursina import color

from ...src.other.get_config_path import get_pynecraft_config_path as conf_path
from ...src.other.settings import get_key_value, hive_exists, key_exists
from ...src.other.world_status import WORLD_STATUS

from ...src.Games.Solo.Pynecraft import Pynecraft

from ursina import destroy

import os

class PyneNewWorldMenu:
    def __init__(self, menu_manager):
        self.menu_manager = menu_manager
        self.main_menu = self.menu_manager.current_menu
        self.worlds = []

        self.currentWorldList = 0

        self.selWorldText = PyneText(text="Select World (New World Menu)", xPos=0, yPos=.45, scale=2.5)

        self.moreWorldsButton = PyneButton(f"More", .505, -.05, .07, .07, lambda: None)
        self.lessWorldsButton = PyneButton(f"Less", .505, .05, .07, .07, lambda: None)

        self.creWorldButton = PyneButton(text="Create a new world", xPos=-.25, yPos=-.45, ySize=.07, xSize=.4, onClick=self.__createWorldMenu)
        self.regWorldButton = PyneButton(text="Regenerate a world", xPos=.25, yPos=-.45, ySize=.07, xSize=.4, onClick=self.__regenerateWorldMenu)
        self.delWorldButton = PyneButton(text="Delete a world", xPos=0, yPos=-.35, ySize=.07, xSize=.4, onClick=self.__deleteWorldMenu)
        
        self.backButton = PyneButton(text="Back",xPos=-.65,yPos=.45,ySize=.07,xSize=.2,onClick=self.__mainMenu, tooltip="Navigate to the menu that you were before")

    def update(self):
        pass
    
    def input(self, key):
        if key == "escape":
            self.__mainMenu()

    def show(self):
        self.__initWorlds()
        self.selWorldText.enabled = True
        self.creWorldButton.enabled = True
        self.regWorldButton.enabled = True
        self.delWorldButton.enabled = True
        self.backButton.enabled = True
        for button in self.worlds:
            button.enabled = True
        
        self.menu_manager.bg.show()

    def hide(self):
        self.selWorldText.enabled = False
        self.creWorldButton.enabled = False
        self.regWorldButton.enabled = False
        self.delWorldButton.enabled = False
        self.backButton.enabled = False
        self.moreWorldsButton.enabled = False
        self.lessWorldsButton.enabled = False
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

        worlds = []

        for worldName in subfolders:
            worldStatus = self.__isValidWorld(worldName)
            world = World(worldStatus, worldName)
            worlds.append(world)
        

        sortedWorlds = self.__sortWorlds(worlds)
        # Display the world ui
        self.__drawWorldUI(sortedWorlds, userName)
    
    def __sortWorlds(self, worlds:list):
        # This is to display first Valid, Deprecated, Newer, Invalid worlds, 16 by 16
        validWorlds = []
        invalidWorlds = []
        newerWorlds = []
        deprecatedWorlds = []

        for world in worlds:
            if type(world) != World:
                pass
            world:World

            if world.worldStatus == WORLD_STATUS.VALID:
                validWorlds.append(world)
            elif world.worldStatus == WORLD_STATUS.DEPRECATED:
                deprecatedWorlds.append(world)
            elif world.worldStatus == WORLD_STATUS.NEWER:
                newerWorlds.append(world)
            elif world.worldStatus == WORLD_STATUS.INVALID:
                invalidWorlds.append(world)
        
        all_worlds = validWorlds + deprecatedWorlds + newerWorlds + invalidWorlds

        return [all_worlds[i:i + 14] for i in range(0, len(all_worlds), 14)]
    
    def __drawWorldUI(self, sorted_worlds, userName):
        totalWorlds = len(sorted_worlds) - 1

        if (totalWorlds > self.currentWorldList):
            self.moreWorldsButton.enabled = True
        else:
            self.moreWorldsButton.enabled = False
        
        if (0 < self.currentWorldList <= totalWorlds):
            self.lessWorldsButton.enabled = True
        else:
            self.lessWorldsButton.enabled = False
        
        self.moreWorldsButton.on_click = lambda: self.__updateWorldIndex(1, sorted_worlds, userName)
        self.lessWorldsButton.on_click = lambda: self.__updateWorldIndex(-1, sorted_worlds, userName)
        
        self.__displayWorlds(sorted_worlds, userName)


    def __updateWorldIndex(self, increment, sorted_worlds, userName):
        """Update the current world index and refresh the UI."""
        self.currentWorldList += increment  # Clamp index
        self.__drawWorldUI(sorted_worlds, userName)  # Redraw the UI with the updated index

    def __displayWorlds(self, all_worlds:list, userName):
        for worldButton in self.worlds:
            destroy(worldButton)

        self.worlds.clear()

        worlds = all_worlds[self.currentWorldList]
        num_worlds = len(worlds)
        column_split = (num_worlds + 1) // 2  # Split evenly across columns

        for index, world in enumerate(worlds):
            if type(world) != World:
                pass
            world:World

            # Determine column and position
            xPos = -0.25 if index < column_split else 0.25  # Left column if index is in first half, right if in second
            yPos = 0.35 - ((index % column_split) / 10)  # Adjust yPos based on row within the column
            
            # Button color and text
            text = os.path.basename(world.worldName)
            color_value = color.white  # Default color

            if world.worldStatus == WORLD_STATUS.NEWER:
                text += " - Newer World?"
                color_value = color.orange
            elif world.worldStatus == WORLD_STATUS.DEPRECATED:
                text += " - Needs Conversion"
                color_value = color.yellow
            elif world.worldStatus == WORLD_STATUS.INVALID:
                text += " - Invalid World"
                color_value = color.light_gray

            # Create the button and add it to self.worlds
            world_button = PyneButton(
                text=text,
                xPos=xPos,
                yPos=yPos,
                ySize=0.07,
                xSize=0.4,
                onClick=lambda world=world, menu_manager=self.menu_manager: world.play(menu_manager, userName)
            )
            world_button.color = color_value
            world_button.text_color_setter(color.white)
            
            self.worlds.append(world_button)

        
    def __mainMenu(self):
        self.menu_manager.set_menu(self.main_menu)
    
    def __createWorldMenu(self):
        self.menu_manager.set_menu(PyneWorldCreationMenu(self.menu_manager))
    
    def __regenerateWorldMenu(self):
        self.menu_manager.set_menu(PyneWorldRegenerationMenu(self.menu_manager))

    def __deleteWorldMenu(self):
        self.menu_manager.set_menu(PyneWorldDeletionMenu(self.menu_manager))
    
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

class World:
    def __init__(self, worldStatus:WORLD_STATUS, worldName:str):
        self.worldStatus = worldStatus
        self.worldName = worldName

    def play(self, menu_manager, userName:str):
        menu_manager.set_menu(Pynecraft(menu_manager, self.worldName, userName))