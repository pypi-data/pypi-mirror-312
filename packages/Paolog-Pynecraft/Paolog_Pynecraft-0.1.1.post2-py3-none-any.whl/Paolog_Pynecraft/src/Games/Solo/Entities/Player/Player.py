from ursina.prefabs.first_person_controller import FirstPersonController
from ursina import Text, scene, Vec3, color

from .Hands import LeftHand, RightHand
from .ui.KillMenu import KillMenu
from ......src.UI.bar import PyneBar

class Player(FirstPersonController):
    # Health
    health:int
    max_health:int
    health_bar:PyneBar

    # Hands
    left_hand:LeftHand
    right_hand:RightHand
    
    # Username
    username:str
    username_text:Text

    # Kill logic
    isDead:bool = False
    killMenu:KillMenu

    # Debug Menu
    # debugMenu:DebugMenu

    # Spawn Position
    # The spawn position of the player won't be changed, to respawn the player at the good location
    spawn_position:Vec3

    def __init__(self, username:str):
        super().__init__()

        # Values
        self.health = 20
        self.max_health = 20
        self.health_bar = PyneBar(color=color.red, ySize=.05, xSize=.6, yPos=-.35, xPos=-.6, max_value=self.max_health)
        self.left_hand = LeftHand()
        self.right_hand = RightHand()
        self.killMenu = KillMenu(self)
        self.username = username
        self.spawn_position = self.position
        #self.debugMenu = DebugMenu()
        

        # Username text
        self.username_text = Text(self.username, position=(0,0), origin=(0,0), scale=(2,2,2), background=True, parent=scene, double_sided=True)
    
    def update(self):
        super().update()
        # Update username text
        self.username_text.position = self.position + Vec3(0,2.5,0)
        self.username_text.rotation = self.rotation
        # Update HealthBar value, if changed
        if self.health_bar.value != self.health:
            self.health_bar.value = self.health
        if self.health_bar.max_value != self.max_health:
            self.health_bar.max_value = self.max_health

        # Kill player is dead
        if self.health == 0 and not self.isDead:
            self.kill()
    
    def input(self, key):
        super().input(key)
        # Enable/Disable F3 Debug Menu
        #if key == "f3":
            #self.debugMenu.hideMenu() if self.debugMenu.visible else self.debugMenu.showMenu()
    
    def damage(self, health:int):
        self.health -= health
    
    def heal(self, health:int):
        self.health += health

    def kill(self):
        self.isDead = True
        if self.isDead:
            self.enabled = False

            # Enable Health Bar, and set the value, because the update loop isn't called
            self.health_bar.enabled = True
            self.health_bar.value = self.health

            self.killMenu.showMenu()
    
    def respawn(self):
        self.enabled = True
        self.health = self.max_health
        self.isDead = False
        self.position = self.spawn_position
        self.rotation = Vec3(0, 0, 0)
        self.killMenu.hideMenu()