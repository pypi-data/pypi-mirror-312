from ursina import *
from .......src.UI.button import PyneButton
from .......src.other.quit import PyneQuit


class KillMenu(Entity):
    def __init__(self, player):                
        super().__init__(
            enabled=True, # Enable it
            color=color.hsv(0, .7, 1, .5), # Use transparent red, so we can see-through 
            scale=(window.aspect_ratio, 1),  # Scale adjusted for correct aspect ratio
            position=(0, 0),  # Center the menu on screen
            parent=camera.ui, # Set the parent to CameraUI
            model='quad' # Set the model to quad
        )
        Text(
            "You are dead",
            position=(0, .15),
            scale=(3 / window.aspect_ratio, 3),  # Apply inverse scale to text
            origin=(0, 0), # Center the origin
            parent=self
        ) # Make the You are dead Text

        PyneButton(
            text="Respawn",
            xPos=.0, yPos=.05,
            ySize=.07, xSize=.4 / window.aspect_ratio,
            onClick=player.respawn,
            tooltip="Click here to respawn",
            parent=self
        ) # Respawn Button

        PyneButton(
            text="Quit The Game",
            xPos=.0, yPos=-.05,
            ySize=.07, xSize=.4 / window.aspect_ratio,
            onClick=PyneQuit,
            tooltip="Click here to quit the game",
            parent=self
        ) # Quit the game button
                
        
        self.hideMenu() # By default, the player isn't killed

    def showMenu(self): # Use this function to show the kill menu
        kill_sound = Audio('assets/rs/sounds/kill', loop = False, autoplay = False)
        
        self.visible = True

        for item in self.children:
            if not isinstance(item, Entity): # If the children isn't an entity, don't do anything with it
                pass
            item.enabled = True # Enable the item

        kill_sound.play() # Play the kill sound when the kill menu is shown

    def hideMenu(self): # Use this function to hide the kill menu
        self.visible = False

        for item in self.children:
            if not isinstance(item, Entity): # If the children isn't an entity, don't do anything with it
                pass
            
            item.enabled = False # Disable the item