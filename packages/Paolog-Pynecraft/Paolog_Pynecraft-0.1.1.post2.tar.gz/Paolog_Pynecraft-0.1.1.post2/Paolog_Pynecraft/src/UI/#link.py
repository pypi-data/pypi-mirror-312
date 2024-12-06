import ursina

class PyneLink:
    def __init__(self, text, xPos: float, yPos: float):
        self.text = ursina.Text(text=text, x=xPos, y=yPos, origin=(0, 0), color=ursina.color.cyan)

        self.underline = ursina.Entity(
            texture="assets/rs/ui/Underline",
            position=(xPos, yPos - (self.text.height / 2)),
            scale=(self.text.width, 0.0016),
            parent=ursina.camera.ui,
            color=self.text.color,
            enabled=True,
            model="quad",
            origin=(0, 0)
        )

        self.text.update = self._update

    def killMe(self):
        ursina.destroy(self.text)
    
    def _input(self, key):
        print("aoudeaoghrwuohrdojngoidxnojdjjodjoid")
        if key == "left mouse down" and self.text.hovered:
            print("ajsiodjawiodjawodjwohgeojghsuoj")

    def _update(self):
        print("djaiodhaiohsoighdiofg")
        if ursina.held_keys["left mouse down"] and self.hovered:
            print("ahiuafiugigdij")
    

# Don't use Link, it is not functionnal