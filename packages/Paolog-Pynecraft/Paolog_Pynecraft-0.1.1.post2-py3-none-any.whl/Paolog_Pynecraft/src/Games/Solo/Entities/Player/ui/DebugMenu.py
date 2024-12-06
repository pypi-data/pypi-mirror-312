from ursina import *
import platform


class DebugMenu(Entity):
    def __init__(self):                
        super().__init__(
            enabled=True, # Enable it
            color=color.clear, 
            scale=(window.aspect_ratio, 1),  # Scale adjusted for correct aspect ratio
            position=(0, 0),  # Center the menu on screen
            parent=camera.ui, # Set the parent to CameraUI
            model='quad' # Set the model to quad
        )
        Text(
            f"Pynecraft - Python {platform.python_version()}",
            position=(window.top_left.x / window.aspect_ratio, window.top_left.y),
            scale=(1 / window.aspect_ratio, 1),  # Apply inverse scale to text
            origin=(-.5, .5), # Center the origin
            parent=self,
            color=color.lime
        )
        self.fpsText = Text(
            "0 FPS", # The text
            position=(window.top_left.x / window.aspect_ratio, window.top_left.y - 0.7 * Text.size), # Make the FPS text down the main text
            scale=(1 / window.aspect_ratio, 1), # Set the scale
            origin=(-.5, .5), # Center the text
            parent=self,
            i=0 # Some ursina magic code to make FPS counter works
        )
        
        self.hideMenu() # By default, the player doesn't have debug menu
    
    def update(self):
        # Update FPS Counter
        if self.fpsText.i > 60:
            self.fpsText.text = str(int(1//time.dt_unscaled)) + " FPS"
            self.fpsText.i = 0
        self.fpsText.i += 1

    def showMenu(self): # Use this function to show the debug menu
        self.visible = True

        for item in self.children:
            if not isinstance(item, Entity): # If the children isn't an entity, don't do anything with it
                pass
            item.enabled = True # Enable the item

    def hideMenu(self): # Use this function to hide the kill menu
        self.visible = False

        for item in self.children:
            if not isinstance(item, Entity): # If the children isn't an entity, don't do anything with it
                pass
            
            item.enabled = False # Disable the item