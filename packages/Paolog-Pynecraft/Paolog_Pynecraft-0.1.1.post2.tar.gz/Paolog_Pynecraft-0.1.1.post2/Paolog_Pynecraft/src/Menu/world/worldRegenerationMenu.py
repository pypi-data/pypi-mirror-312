from ....src.UI.bar import PyneBar
from ....src.UI.input import PyneInput
from ....src.UI.text import PyneText
from ....src.UI.button import PyneButton

from ....src.other.world_generator import WorldGenerator
from ....src.other.get_config_path import get_pynecraft_config_path as conf_path

from ursina import color, Entity, window, camera
import os

class PyneWorldRegenerationMenu:
    def __init__(self, menu_manager):
        self.menu_manager = menu_manager

        self.worldGenerator:WorldGenerator = WorldGenerator()
        self.percentageBar = PyneBar(color=color.green, max_value=100, xPos=-.2, yPos=.3, xSize=.4, ySize=.07, tooltip=None)
        self.percentageBar.text_color = color.gray
        self.duringRegWorldText = PyneText(text="Regenerating world", xPos=.0, yPos=.4, scale=2)

        self.bgBlur = Entity(enabled=True, color=color.hsv(0, 0, .5, .4), scale=(window.aspect_ratio, 1), position=(0,0), parent=camera.ui, model='quad', z=0)

        self.titText = PyneText(text="Renegerate World", xPos=.0, yPos=.45, scale=2.5)
        self.titText.z = -1
        self.backButton = PyneButton(text="Back",xPos=-.65,yPos=.45,ySize=.07,xSize=.2,onClick=self.__mainMenu, tooltip="Return to world selection")

        self.regWorldNameText = PyneText(text="World Name:", xPos=0, yPos=.025, scale=1.5)
        self.regWorldNameInput = PyneInput(default_value="", xPos=0, yPos=-.025, ySize=.07, xSize=.7, character_limit=33)
        
        self.regWorldButton = PyneButton(text="Regenerate World",xPos=0,yPos=-.15,ySize=.07,xSize=.7,onClick=self.__createWorld)

    def update(self):
        if self.worldGenerator.get_progression() != 100 and self.worldGenerator.get_progression() > 0:
            self.percentageBar.bar_color = color.lime
            self.percentageBar.value = self.worldGenerator.get_progression()
            self.percentageBar.text = str(self.worldGenerator.get_progression()) + "%"
        elif self.worldGenerator.get_progression() == 100:
            self.percentageBar.bar_color = color.green
            self.percentageBar.value = 100
            self.percentageBar.text = "Finished"
            self.backButton.enabled = True
        elif self.worldGenerator.get_progression() == -1:
            self.percentageBar.bar_color = color.yellow
            self.percentageBar.text = "World doesn't exists."
            self.backButton.enabled = True
        elif self.worldGenerator.get_progression() == -2:
            self.percentageBar.bar_color = color.yellow
            self.percentageBar.text = "World name can't be empty"
            self.backButton.enabled = True
        elif self.worldGenerator.get_progression() == -100:
            self.percentageBar.bar_color = color.orange
            self.percentageBar.text = "Can't regenerate world :,("
            self.backButton.enabled = True
        elif self.worldGenerator.get_progression() == -101:
            self.percentageBar.bar_color = color.yellow
            self.percentageBar.text = "World size can't be 0"
            self.backButton.enabled = True
    
    def input(self, key):
        if key == "escape":
            self.__mainMenu()

    def show(self):
        # Show all the UI elements of the settings menu
        self.titText.enabled = True
        self.backButton.enabled = True
        self.bgBlur.enabled = True

        self.regWorldButton.enabled = True
        self.regWorldNameText.enabled = True
        self.regWorldNameInput.enabled = True

        self.regWorldButton.enabled = True
        self.backButton.enabled = True
        self.percentageBar.enabled = False
        self.duringRegWorldText.enabled = False

        self.menu_manager.bg.show()

    def hide(self):
        # Hide all the UI elements of the settings menu
        self.titText.enabled = False
        self.backButton.enabled = False
        self.bgBlur.enabled = False

        self.regWorldButton.enabled = False
        self.regWorldNameText.enabled = False
        self.regWorldNameInput.enabled = False

        self.regWorldButton.enabled = False
        self.percentageBar.enabled = False
        self.backButton.enabled = False
        self.duringRegWorldText.enabled = False

        self.menu_manager.bg.hide()
    
    def __createWorld(self):
        worldname:str = self.regWorldNameInput.text
        worldFolder = os.path.join(conf_path(), "worlds")
        if not os.path.exists(os.path.join(worldFolder, worldname)):
            self.worldGenerator.progression = -1

            self.hide()
            self.percentageBar.enabled = True
            self.duringRegWorldText.enabled = True
            self.menu_manager.bg.show()
            return

        seed:str
        world_size:str

        # Get seed and world size
        try:
            with open(os.path.join(worldFolder, worldname, "info.txt")) as file:
                lines = file.readlines()
                
                for line in lines:
                    if line.startswith("seed"):
                        seed = line.split("=")[1]
                    if line.startswith("world_size"):
                        world_size = line.split("=")[1]
        except:
            self.worldGenerator.progression = -100

            self.hide()
            self.percentageBar.enabled = True
            self.duringRegWorldText.enabled = True
            self.menu_manager.bg.show()
            return

        self.hide()
        self.percentageBar.enabled = True

        self.duringRegWorldText.enabled = True
        self.menu_manager.bg.show()
        
        self.worldGenerator.generate_world(worldname, seed, world_size)

    def __mainMenu(self):
        if (self.duringRegWorldText.enabled):
            self.show()
        else:
            self.menu_manager.go_back()