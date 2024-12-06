from ...src.UI.input import PyneInput
from ...src.UI.text import PyneText
from ...src.UI.button import PyneButton

from ...src.other.settings import node_exists, hive_exists, create_hive, set_key_value, key_exists, get_key_value

from ursina import window

class PyneSettingsMenu:
    def __init__(self, menu_manager):
        self.menu_manager = menu_manager

        self.titText = PyneText(text="Settings", xPos=.0, yPos=.45, scale=2.5)
        self.backButton = PyneButton(text="Back",xPos=-.65,yPos=.45,ySize=.07,xSize=.2,onClick=self.__mainMenu, tooltip="Navigate to the menu that you were before")

        userNameInput_value:str
        if not hive_exists("PYNECRAFT", "USER") or not key_exists("PYNECRAFT", "USER", "USERNAME"):
            userNameInput_value = "Rick"
        else:
            userNameInput_value = get_key_value("PYNECRAFT", "USER", "USERNAME")
        
        fullScreenButton_value:bool
        if not hive_exists("PYNECRAFT", "WINDOW") or not key_exists("PYNECRAFT", "WINDOW", "FULLSCREEN"):
            fullScreenButton_value = False
        else:
            fullScreenButton_value = False if get_key_value("PYNECRAFT", "WINDOW", "FULLSCREEN") == "False" else True

        self.userNameinput = PyneInput(default_value=userNameInput_value, yPos=.3, xPos=-.2, ySize=.07,xSize=.4, tooltip="Username", character_limit=20)
        self.userNamebutton = PyneButton(text="Submit username",yPos=.3,xPos=.2,ySize=.07,xSize=.4,onClick=self.__on_submit)
        self.userNameinput.limit_content_to = 'QWERTZUIOPASDFGHJKLYXCVBNMqwertzuiopasdfghjklyxcvbnm_-ඞ'

        self.fullScreenText = PyneText("Fullscreen: ", xPos=-.2, yPos=.2, scale=1.5)
        self.fullScreenButton = PyneButton(f"Current Status: {fullScreenButton_value}", xPos=.2, yPos=.2, ySize=.07, xSize=.4, onClick=self.__toggleFullScreen)

    def update(self):
        pass  
    
    def input(self, key):
        if key == "escape":
            self.__mainMenu()

    def show(self):
        self.titText.enabled = True
        self.backButton.enabled = True
        self.userNameinput.enabled = True
        self.userNamebutton.enabled = True
        self.fullScreenText.enabled = True
        self.fullScreenButton.enabled = True
        self.menu_manager.bg.show()

    def hide(self):
        self.titText.enabled = False
        self.backButton.enabled = False
        self.userNameinput.enabled = False
        self.userNamebutton.enabled = False
        self.fullScreenText.enabled = False
        self.fullScreenButton.enabled = False
        self.menu_manager.bg.hide()
    
    def __mainMenu(self):
        self.menu_manager.go_back()
    
    def __on_submit(self):
        if not node_exists("PYNECRAFT"):
            return
        if not hive_exists("PYNECRAFT", "USER"):
            create_hive("PYNECRAFT", "USER")
        set_key_value("PYNECRAFT", "USER", "USERNAME", self.userNameinput.text)
    
    def __toggleFullScreen(self):
        if not node_exists("PYNECRAFT"):
            return
        if not hive_exists("PYNECRAFT", "WINDOW"):
            create_hive("PYNECRAFT", "WINDOW")
        if not key_exists("PYNECRAFT", "WINDOW", "FULLSCREEN"):
            set_key_value("PYNECRAFT", "WINDOW", "FULLSCREEN", value="True")
        
        if get_key_value("PYNECRAFT", "WINDOW", "FULLSCREEN") == "False":
            set_key_value("PYNECRAFT", "WINDOW", "FULLSCREEN", value="True")
            self.fullScreenButton.text = "Current Status: True"
            window.fullscreen = True
        else:
            set_key_value("PYNECRAFT", "WINDOW", "FULLSCREEN", value="False")
            self.fullScreenButton.text = "Current Status: False"
            window.fullscreen = False