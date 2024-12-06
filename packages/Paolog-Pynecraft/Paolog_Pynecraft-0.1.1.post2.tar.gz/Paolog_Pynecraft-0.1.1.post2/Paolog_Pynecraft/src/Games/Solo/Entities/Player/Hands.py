from ursina import Entity, camera, Vec3, Vec2

class RightHand(Entity):
    def __init__(self):
        super().__init__(
        parent = camera.ui,
        model = 'assets/rs/objects/arm',
        texture = 'assets/rs/images/arm_texture.png',
        scale = 0.2,
        rotation = Vec3(150,-10,0))
        
    def active(self):
        self.position = Vec2(0.4,-0.5)
        
    def passive(self):
        self.position = Vec2(0.5,-0.6)
        
class LeftHand(Entity):
    def __init__(self):
        super().__init__(
        parent = camera.ui,
        model = 'assets/rs/objects/arm',
        texture = 'assets/rs/images/arm_texture.png',
        scale = 0.2,
        rotation = Vec3(150,10,0))
    def active(self):
        self.position = Vec2(-0.4 + self.scale_x_getter(), -0.5)
    def passive(self):
        self.position = Vec2(-0.5 + self.scale_x_getter() ,-0.6)
        ## Why does I add a +self.scale_x_getter() ?
        ## Because the origin of 3D model is at right top, so to left hand I need to add the width of the object to be centered
        