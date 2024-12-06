from ursina import *

class PyneScroll(Entity):
    def __init__(self, xSize:float, ySize:float, xPos:float, yPos:float, parent=camera.ui):
        # Init Entity
        super().__init__(
            scale=(xSize, ySize),
            position=(xPos, yPos),
            color=color.black,
            parent=parent,
            model='quad',
            collider='box'
        )

        # Sample text for testing
        Text("hi", parent=self, y=0.4, scale=(2, 2/window.aspect_ratio))
        Text("there", parent=self, y=0.2, scale=(2, 2/window.aspect_ratio))
        Text("scroll", parent=self, y=0, scale=(2, 2/window.aspect_ratio))
        Text("works", parent=self, y=-0.2, scale=(2, 2/window.aspect_ratio))
        Text("now!", parent=self, y=-0.4, scale=(2, 2/window.aspect_ratio))
    
    def input(self, key):
        if key == "scroll down" and self.hovered:
            for child in self.children:
                child.y -= 0.05
                self.update_visibility()
            
        if key == "scroll up" and self.hovered:
            for child in self.children:
                child.y += 0.05
                self.update_visibility()
        
    
    def update_visibility(self):
        ySize = self.scale.y
        # Determine the bounds of the visible area
        top_bound = self.position.y + (ySize / 5)
        bottom_bound = self.position.y - (ySize / 5)

        for child in self.children:
            child_top = child.position.y + (child.scale.y / window.aspect_ratio / 2)
            child_bottom = child.position.y - (child.scale.y / window.aspect_ratio / 2)
            
            # Enable only if within the scroll bounds
            child.enabled = (child_bottom < top_bound and child_top > bottom_bound)