from ...src.UI.input import PyneInput
from ...src.UI.text import PyneText
from ...src.UI.button import PyneButton

from ...src.other.get_config_path import get_pynecraft_config_path as conf_path
import os
import sys

class PyneMultiMenu:
    def __init__(self, menu_manager):
        self.menu_manager = menu_manager

        self.selServText = PyneText(text="Select Server", xPos=-.3, yPos=.45, scale=2.5)
        self.creServText = PyneText(text="Create Server", xPos=.3, yPos=.45, scale=2.5)

        self.selServURLText = PyneText(text="Server URL:", xPos=-.3, yPos=.35, scale=1.5)
        self.selServURLInput = PyneInput(default_value="Not supported yet", xPos=-.3, yPos=.3, ySize=.07, xSize=.4)
        self.selServURLInput.limit_content_to = "1234567890.:"
        self.selServButton = PyneButton(text="Connect to server", xPos=-.3, yPos=.2, xSize=.4, ySize=.07, onClick=self.__connect)

        self.creServNeedBinaryText = PyneText(text="You need Pynecraft server binary.\n\nhttps://paologgithub.github.io/products/Pynecraft/server", xPos=.3, yPos=.35, scale=1)

        self.backButton = PyneButton(text="Back",xPos=-.65,yPos=.45,ySize=.07,xSize=.2,onClick=self.__mainMenu, tooltip="Navigate to the menu that you were before")

    def update(self):
        server_binary_path = conf_path() + "/server"
        if os.path.exists(server_binary_path) and os.path.isdir(server_binary_path):
            self.creServNeedBinaryText.enabled = False
            
            sys.path.insert(0, conf_path())
        else:
            self.creServNeedBinaryText.enabled = True
    
    def input(self, key):
        if key == "escape":
            self.__mainMenu()

    def show(self):
        self.selServText.enabled = True
        self.creServText.enabled = True

        self.selServURLText.enabled = True
        self.selServURLInput.enabled = True
        self.creServNeedBinaryText.enabled = True
        self.selServButton.enabled = True

        self.backButton.enabled = True
        self.menu_manager.bg.show()

    def hide(self):
        self.selServText.enabled = False
        self.creServText.enabled = False

        self.selServURLText.enabled = False
        self.selServURLInput.enabled = False
        self.creServNeedBinaryText.enabled = False
        self.selServButton.enabled = False

        self.backButton.enabled = False
        self.menu_manager.bg.hide()
    
    def __mainMenu(self):
        self.menu_manager.go_back()
    
    def __connect(self):
        print(self.selServURLInput.text)