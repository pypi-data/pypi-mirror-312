from ursina.prefabs.input_field import InputField
from ursina import Tooltip

class PyneInput(InputField):
    def __init__(self, default_value:str, xPos:int, yPos:int,xSize:int,ySize:int,tooltip = None, on_value_changed = None, hide_content=False, on_submit=None, character_limit=24):
        super().__init__(
            default_value=default_value,
            x=xPos,
            y=yPos,
            scale=(xSize, ySize),
            model="quad",
            on_value_changed=on_value_changed,
            hide_content=hide_content,
            on_submit=on_submit,
            character_limit=character_limit
        )
        self.text_field.text_entity.font = "assets/rs/fonts/Pixelon.otf"
        self.text_field.font = "assets/rs/fonts/Pixelon.otf"

        if not tooltip == None or type(tooltip) is str: self.tooltip = Tooltip(text=tooltip, font="assets/rs/fonts/Pixelon.otf")