from ursina.prefabs.health_bar import HealthBar
from ursina import color, Tooltip

class PyneBar(HealthBar):
    def __init__(self, color:color, max_value:int, xPos:int, yPos:int, xSize:int, ySize:int, tooltip = None):
        super().__init__(
            max_value=max_value,
            roundness=0,
            color=color,
            scale=(xSize, ySize),
            x=xPos,
            y=yPos
        )

        self.text_entity.font = "assets/rs/fonts/Pixelon.otf"

        if not tooltip == None or type(tooltip) is str: self.tooltip = Tooltip(text=tooltip, font="assets/rs/fonts/Pixelon.otf")