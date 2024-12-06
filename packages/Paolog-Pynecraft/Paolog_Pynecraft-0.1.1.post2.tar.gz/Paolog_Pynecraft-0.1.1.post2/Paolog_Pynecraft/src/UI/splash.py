from ursina import *

class CustomSplashScreen(Entity):
    def __init__(self):
        # SplashScreen Logic
        super().__init__(scale=(window.aspect_ratio, 1), position=(0, 0), parent=camera.ui, world_z=camera.overlay.z-1, color=color.clear)
        camera.overlay.animate_color(color.black, duration=.1)

        # Title at the top
        self.title = Entity(
            texture="assets/rs/title/pynecraft_title.png",
            position=(0, 0.3),  # Set a z-index to bring it forward,
            parent = self,
            model = "quad",
            scale = (.75225 / window.aspect_ratio, .147),
            color=color.clear
        )

        # Grass Blocks
        x = -.7
        while x <= 0.7:
            if abs(x) < 1e-5:  # Check if x is close to 0 (Yeah, the 0 is at Xe-17)
                Voxel(parent=self, position=Vec2(0, .6), Parent=self, needToFall=True)  # Place at (0, -0.2)
            else:
                Voxel(parent=self, position=Vec2(x, 0), Parent=self)    # Place at (x, 0)
            x += 0.1

        # Dirt Blocks
        y = -0.5 * window.aspect_ratio
        while y <= -0.1:
            x = -.7  # Reset x for each new row of dirt blocks
            while x <= 0.7:
                Voxel(parent=self, position=Vec2(x, y), texture="assets/rs/images/dirt_block", Parent=self)
                x += 0.1
            y += 0.1 * window.aspect_ratio

    def input(self, key):
        pass

    def on_destroy(self):
        camera.overlay.animate_color(color.clear, duration=.25)

class Voxel(Entity):
    def __init__(self, parent, Parent:CustomSplashScreen, needToFall:bool = False, position = (0, 0), texture = "assets/rs/images/grass_block"):
        self.needToFall = needToFall
        self.alreadyFalled = False
        self.title = Parent.title
        self.Splash = Parent

        super().__init__(
            parent=parent,
            position=position,
            model='assets/rs/objects/block',
            origin_y=0.05,
            texture=texture,
            scale=(0.05, window.aspect_ratio * 0.05)
        )

    def update(self):
        if self.needToFall and self.position.y > 0:
            self.position = Vec2(self.position.x, self.position.y - .009)

        if self.needToFall and self.position <= 0 and not self.alreadyFalled:
            self.alreadyFalled = True
            self.position = Vec2(self.position.x, 0)

            # Handle title
            self.title:Entity
            self.title.animate_color(color.white, 0.5, curve=curve.out_sine)
            Text(
                "Made by Paolog and V-333", 
                position=(window.top_left.x / window.aspect_ratio, window.top_left.y),
                color=color.clear, 
                parent=self.Splash, 
                scale=(0.5, 0.5 * window.aspect_ratio),
                origin=(-.5, .5),
                font="assets/rs/fonts/Pixelon.otf"
            ).animate_color(color.white, 0.5, curve=curve.out_sine)

            # Finish the splash screen
            self.Splash.animate_color(color.white, duration=2, delay=1.5, curve=curve.out_quint_boomerang)
            invoke(destroy, self.Splash, delay=3.5)