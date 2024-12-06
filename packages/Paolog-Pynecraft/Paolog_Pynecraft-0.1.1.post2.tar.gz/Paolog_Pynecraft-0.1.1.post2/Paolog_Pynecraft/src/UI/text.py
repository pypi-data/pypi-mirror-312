from ursina import Text, Vec3

class PyneText(Text):
    def __init__(self, text:str, xPos: float, yPos: float, scale: float):
        super().__init__(
            text=text,
            position=(xPos, yPos),
            origin=(0, 0),
            font="assets/rs/fonts/Pixelon.otf",
            scale=scale
        )
    
    def changeScale(self, scale: float):
        self.scale = Vec3(scale, scale, scale)

    def getXScale(self):
        return self.scale.x  # Access x component of the scale Vec3