from ursina import Entity, scene, Vec3

class PyneBackground:
    def __init__(self):
        self.sky = Entity(
            parent=scene,
            model='sphere',
            texture="assets/rs/images/skybox_day.png",
            position=Vec3(0, -.4, -20),
            double_sided=True
        )

        self.time = 0

    def hide(self):
        self.sky.enabled = False
    
    def show(self):
        self.sky.enabled = True
    
    def update(self):
        self.sky.rotation += Vec3(0, .5, 0)