import random
import ursina

from ...src.Menu.settingsMenu import PyneSettingsMenu
from ...src.Menu.worldMenu import PyneWorldMenu
from ...src.Menu.newWorldMenu import PyneNewWorldMenu
from ...src.Menu.multiMenu import PyneMultiMenu

from ...src.UI.button import PyneButton
from ...src.UI.text import PyneText

from ...src.other.quit import PyneQuit

import os

class PyneMainMenu:
    def __init__(self, menu_manager):
        self.menu_manager = menu_manager
        
        self.titText = ursina.Entity(
            texture="assets/rs/title/pynecraft_title.png",
            position=(0, 0.3),  # Set a z-index to bring it forward,
            parent = ursina.camera.ui,
            model = "quad",
            scale = (.75225, .147)
        )

        # Load hint texts from file
        with open(os.path.dirname(os.path.realpath(__file__)) + "/../../assets/rs/title/hints.txt", "r") as file:
            hint_lines = [line.strip() for line in file.readlines()]
        
        # Randomly choose a line from the hint texts
        hint_text = random.choice(hint_lines)

        self.hintText = PyneText(text=hint_text, xPos=.34, yPos=.26, scale=1.25)
        self.hintText.rotation = (0, 0, -15)  # Rotating the hint text
        self.hintText.color = ursina.color.yellow  # Changing color to yellow
        self.hintText.origin = (0, 0)

        self.solbuttonOld = PyneButton(text="Play Solo (Old Menu)", xPos=0, yPos=-.2,ySize=.07, xSize=.4, onClick=self.__playSoloOld, tooltip="Deprecated, will be removed")
        self.solbutton = PyneButton(text="Play Solo", xPos=0, yPos=.1, ySize=.07, xSize=.4, onClick=self.__playSolo)
        self.mulbutton = PyneButton(text="Play Multiplayer", xPos=0, yPos=0, ySize=.07, xSize=.4, onClick=self.__playMulti)
        
        # Create a parent entity to group the Settings and Quit buttons
        self.moreButtonsGroup = ursina.Entity(parent=ursina.camera.ui, position=(0, -.1))  # Centered and slightly below the other buttons

        # Add the Settings and Quit buttons with relative positions inside the parent
        self.setbutton = PyneButton(
            text="Settings", xPos=-.11, yPos=0, ySize=.07, xSize=.18, 
            onClick=self.__settingsMenu
        )
        self.setbutton.parent = self.moreButtonsGroup
        self.quitbutton = PyneButton(
            text="Quit", xPos=.11, yPos=0, ySize=.07, xSize=.18, 
            onClick=PyneQuit, tooltip="Quit the Game"
        )
        self.quitbutton.parent = self.moreButtonsGroup

        self.creditsText = PyneText(text="A moddable fan game created by Paolog", xPos=ursina.window.bottom_left.x, yPos=ursina.window.bottom_left.y, scale=1)
        self.creditsText.origin = (-0.5, -0.5)

        self.versionText = PyneText(text="Pynecraft 0.1.1.Post2", xPos=ursina.window.bottom_right.x, yPos=ursina.window.bottom_right.y, scale=1)
        self.versionText.origin = (0.5, -0.5)

        self.direction = 1  # 1 for increasing size, -1 for decreasing size
        self.__eastersEgg(hint_lines.index(hint_text))
    
    def __eastersEgg(self, hintLine:int):
        hintLine += 1
        if hintLine == 30:
            self.hintText.position = (.32, -.25)
        elif hintLine == 29:
            self.hintText.color = ursina.color.cyan
        elif hintLine == 31:
            self.titText.texture = "assets/rs/title/pynecraft_title-31.png"
            self.titText.scale = (.723, .1035)
        elif hintLine == 35:
            self.titText.texture = "assets/rs/title/pynecraft_title-35.png"
        elif hintLine == 49:
            self.menu_manager.bg.sky.texture = "assets/rs/images/skybox_night.png"

    def update(self):
        current_scale = self.hintText.getXScale()
        if current_scale >= 1.4:
            self.direction = -1
        elif current_scale <= 1.25:
            self.direction = 1
        self.hintText.changeScale(current_scale + self.direction * 0.006)
        
    
    def input(self, key):
        pass
    
    def show(self):
        self.titText.enabled = True
        self.moreButtonsGroup.enabled = True
        self.versionText.enabled = True
        self.creditsText.enabled = True
        self.hintText.enabled = True
        self.solbutton.enabled = True
        self.solbuttonOld.enabled = True
        self.mulbutton.enabled = True
        self.setbutton.enabled = True
        self.quitbutton.enabled = True
        self.menu_manager.bg.show()

    def hide(self):
        self.titText.enabled = False
        self.moreButtonsGroup.enabled = False
        self.versionText.enabled = False
        self.creditsText.enabled = False
        self.hintText.enabled = False
        self.solbutton.enabled = False
        self.solbuttonOld.enabled = False
        self.mulbutton.enabled = False
        self.setbutton.enabled = False
        self.quitbutton.enabled = False
        self.menu_manager.bg.hide()



    def __playSolo(self):
        self.menu_manager.set_menu(PyneNewWorldMenu(self.menu_manager))
    
    def __playSoloOld(self):
        self.menu_manager.set_menu(PyneWorldMenu(self.menu_manager))

    def __playMulti(self):
        self.menu_manager.set_menu(PyneMultiMenu(self.menu_manager))

    def __settingsMenu(self):
        self.menu_manager.set_menu(PyneSettingsMenu(self.menu_manager))