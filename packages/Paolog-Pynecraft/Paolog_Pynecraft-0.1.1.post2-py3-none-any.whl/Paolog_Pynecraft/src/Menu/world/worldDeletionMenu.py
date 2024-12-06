from ....src.UI.bar import PyneBar
from ....src.UI.input import PyneInput
from ....src.UI.text import PyneText
from ....src.UI.button import PyneButton

from ....src.other.world_destroyer import WorldDestroyer

from ursina import color, Entity, window, camera

class PyneWorldDeletionMenu:
    def __init__(self, menu_manager):
        self.menu_manager = menu_manager

        self.worldGenerator = WorldDestroyer()

        self.percentageBar = PyneBar(color=color.green, max_value=100, xPos=-.2, yPos=.3, xSize=.4, ySize=.07, tooltip=None)
        self.percentageBar.text_color = color.gray
        self.duringDelWorldText = PyneText(text="Deleting world", xPos=.0, yPos=.4, scale=2)

        self.bgBlur = Entity(enabled=True, color=color.hsv(0, 0, .5, .4), scale=(window.aspect_ratio, 1), position=(0,0), parent=camera.ui, model='quad', z=0)

        self.titText = PyneText(text="Delete World", xPos=.0, yPos=.45, scale=2.5)
        self.titText.z = -1
        self.backButton = PyneButton(text="Back",xPos=-.65,yPos=.45,ySize=.07,xSize=.2,onClick=self.__mainMenu, tooltip="Return to world selection")

        self.delWorldNameText = PyneText(text="World Name:", xPos=0, yPos=.025, scale=1.5)
        self.delWorldNameInput = PyneInput(default_value="", xPos=0, yPos=-.025, ySize=.07, xSize=.7, character_limit=33)
        
        self.delWorldButton = PyneButton(text="Delete World",xPos=0,yPos=-.2,ySize=.07,xSize=.7,onClick=self.__deleteWorld)

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
            self.percentageBar.text = "World doesn't exist"
            self.backButton.enabled = True
        elif self.worldGenerator.get_progression() == -2:
            self.percentageBar.bar_color = color.yellow
            self.percentageBar.text = "World is a file?"
            self.backButton.enabled = True
        elif self.worldGenerator.get_progression() == -100:
            self.percentageBar.bar_color = color.orange
            self.percentageBar.text = "Can't delete world :,("
            self.backButton.enabled = True

    def input(self, key):
        if key == "escape":
            self.__mainMenu()

    def show(self):
        # Show all the UI elements of the settings menu
        self.titText.enabled = True
        self.backButton.enabled = True
        self.bgBlur.enabled = True

        self.delWorldButton.enabled = True
        self.delWorldNameText.enabled = True
        self.delWorldNameInput.enabled = True

        self.delWorldButton.enabled = True
        self.backButton.enabled = True
        self.percentageBar.enabled = False
        self.duringDelWorldText.enabled = False

        self.menu_manager.bg.show()

    def hide(self):
        # Hide all the UI elements of the settings menu
        self.titText.enabled = False
        self.backButton.enabled = False
        self.bgBlur.enabled = False

        self.delWorldButton.enabled = False
        self.delWorldNameText.enabled = False
        self.delWorldNameInput.enabled = False

        self.delWorldButton.enabled = False
        self.percentageBar.enabled = False
        self.backButton.enabled = False
        self.duringDelWorldText.enabled = False

        self.menu_manager.bg.hide()
    
    def __deleteWorld(self):
        worldname:str = self.delWorldNameInput.text

        self.hide()
        self.percentageBar.enabled = True

        self.duringDelWorldText.enabled = True
        self.menu_manager.bg.show()
        
        self.worldGenerator.delete_world(worldname)

    def __mainMenu(self):
        if (self.duringDelWorldText.enabled):
            self.show()
        else:
            self.menu_manager.go_back()