from ursina import *
from ursina.window import *

from ...src.UI.splash import CustomSplashScreen

class PyneWindow:
    def __init__(self, title:str, EditorUIEnabled:bool, ExitButtonEnabled:bool, icon:str, isBorderless:bool, alwaysOnTop:bool, COGMenuEnabled:bool, show_startup_screen:bool):
        self.app = Ursina(title=title, icon=icon, borderless=isBorderless)

        if show_startup_screen:
            self.app.splash_screen = CustomSplashScreen()

        window.editor_ui.enabled = EditorUIEnabled
        ### You'll ask me why did I didn't use enabled, and I use visible.
        ### That's because, by disabling it, Shift+Q won't close the app
        ### By hiding it with visible, we can Shift+Q to close the app.
        ### So, if I want to troll the players, I need to make exit button enable
        # window.exit_button.enabled = ExitButton
        window.exit_button.visible = ExitButtonEnabled
        window.cog_button.enabled = COGMenuEnabled
        window.always_on_top = alwaysOnTop

    def run(self):
        self.app.run()