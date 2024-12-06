from ....src.UI.bar import PyneBar
from ....src.UI.input import PyneInput
from ....src.UI.text import PyneText
from ....src.UI.button import PyneButton

from ....src.other.world_generator import WorldGenerator

from ursina.prefabs.input_field import ContentTypes
from ursina import color, Entity, window, camera
import random

class PyneWorldCreationMenu:
    def __init__(self, menu_manager):
        self.menu_manager = menu_manager

        self.worldGenerator:WorldGenerator = WorldGenerator()
        self.percentageBar = PyneBar(color=color.green, max_value=100, xPos=-.2, yPos=.3, xSize=.4, ySize=.07, tooltip=None)
        self.percentageBar.text_color = color.gray
        self.duringCreWorldText = PyneText(text="Creating world", xPos=.0, yPos=.4, scale=2)

        self.bgBlur = Entity(enabled=True, color=color.hsv(0, 0, .5, .4), scale=(window.aspect_ratio, 1), position=(0,0), parent=camera.ui, model='quad', z=0)

        self.titText = PyneText(text="Create World", xPos=.0, yPos=.45, scale=2.5)
        self.titText.z = -1
        self.backButton = PyneButton(text="Back",xPos=-.65,yPos=.45,ySize=.07,xSize=.2,onClick=self.__mainMenu, tooltip="Return to world selection")

        self.creWorldNameText = PyneText(text="World Name:", xPos=0, yPos=.25, scale=1.5)
        self.creWorldNameInput = PyneInput(default_value="", xPos=0, yPos=.2, ySize=.07, xSize=.7, character_limit=33)

        self.creWorldSeedText = PyneText(text="World Seed:", xPos=0, yPos=.1, scale=1.5)
        self.creWorldSeedInput = PyneInput(default_value=str(random.randrange(1, int('9' * 32)))
                                           , xPos=0, yPos=.05, ySize=.07, xSize=.7, character_limit=33)
        self.creWorldSeedInput.limit_content_to = ContentTypes.int

        self.creWorldSizeText = PyneText(text="World Size:", xPos=.0, yPos=-.05, scale=1.5)
        self.creWorldSizeInput = PyneInput(default_value=str(12)
                                           , xPos=.0, yPos=-.1, ySize=.07, xSize=.7, character_limit=20)
        self.creWorldSizeInput.limit_content_to = ContentTypes.int
        
        self.creWorldButton = PyneButton(text="Create World",xPos=0,yPos=-.2,ySize=.07,xSize=.7,onClick=self.__createWorld)

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
            self.percentageBar.text = "Invalid world name"
            self.backButton.enabled = True
        elif self.worldGenerator.get_progression() == -2:
            self.percentageBar.bar_color = color.yellow
            self.percentageBar.text = "World name can't be empty"
            self.backButton.enabled = True
        elif self.worldGenerator.get_progression() == -100:
            self.percentageBar.bar_color = color.orange
            self.percentageBar.text = "Can't create world :,("
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

        self.creWorldButton.enabled = True
        self.creWorldNameText.enabled = True
        self.creWorldNameInput.enabled = True
        self.creWorldSeedText.enabled = True
        self.creWorldSeedInput.enabled = True
        self.creWorldSizeText.enabled = True
        self.creWorldSizeInput.enabled = True

        self.creWorldButton.enabled = True
        self.backButton.enabled = True
        self.percentageBar.enabled = False
        self.duringCreWorldText.enabled = False

        self.menu_manager.bg.show()

    def hide(self):
        # Hide all the UI elements of the settings menu
        self.titText.enabled = False
        self.backButton.enabled = False
        self.bgBlur.enabled = False

        self.creWorldButton.enabled = False
        self.creWorldNameText.enabled = False
        self.creWorldNameInput.enabled = False
        self.creWorldSeedText.enabled = False
        self.creWorldSeedInput.enabled = False
        self.creWorldSizeText.enabled = False
        self.creWorldSizeInput.enabled = False

        self.creWorldButton.enabled = False
        self.percentageBar.enabled = False
        self.backButton.enabled = False
        self.duringCreWorldText.enabled = False

        self.menu_manager.bg.hide()
    
    def __createWorld(self):
        worldname:str = self.creWorldNameInput.text
        seed:str = self.creWorldSeedInput.text
        world_size:str = self.creWorldSizeInput.text

        self.hide()
        self.percentageBar.enabled = True

        self.duringCreWorldText.enabled = True
        self.menu_manager.bg.show()
        
        self.worldGenerator.generate_world(worldname, seed, world_size)

    def __mainMenu(self):
        if (self.duringCreWorldText.enabled):
            self.show()
        else:
            self.menu_manager.go_back()