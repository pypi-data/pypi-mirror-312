# Import game-related Objects
from ursina import Vec3, Vec2, BoxCollider, camera, scene, mouse, distance, invoke
# Import Widget-related Objects
from ursina import Entity, Button, Text, window, destroy
# Import Resources-related Objects
from ursina import Audio, color, load_texture

# Import entities
from ....src.Games.Solo.Entities.Player.Player import Player

# Import math-related Objects
import time
from ursina import random

# Import Pynecraft Widgets
from ....src.UI.button import PyneButton
from ....src.other.quit import PyneQuit


class Pynecraft:
    def __init__(self, menu_manager, world:str, username:str):
        self.menu_manager = menu_manager

        global player
        player = Player(username=username)
        spawn_position = player.position #get spawn position
        sky_day_texture = load_texture('assets/rs/images/skybox_day.png')
        sky_night_texture = load_texture('assets/rs/images/skybox_night.png')
        punch_sound = Audio('assets/rs/sounds/punch_sound',loop = False, autoplay = False)
        glass_sound = Audio('assets/rs/sounds/glass_sound',loop = False, autoplay = False)
        boss1_sound = Audio('assets/rs/sounds/boss1', loop = True, autoplay = True)
        crash_sound = Audio('assets/rs/sounds/kill', loop = True, autoplay = False)
        global block_pick
        block_pick = 1
        #sky_texture = sky_night_texture
        sky_texture = sky_day_texture
        global escmenuenabled
        escmenuenabled = False
        global isplayerkilled
        isplayerkilled = False
        global cameraposition
        cameraposition = "normal"
        #render_distance = 25
        render_distance = 6

        worldname = world

        def go_back(): 
            # Remove all blocks
            # Make sure that all blocks is removed by doing it 10 times
            for _ in range(10):
                for block in all_blocks:
                    block:Block
                    block.force_destroy(block)
            
            # Disable all entities
            player.right_hand.enabled = False
            player.left_hand.enabled = False
            player.health_bar.enabled = False
            player.username_text.enabled = False
            player.enabled = False
            sky.enabled = False
            """ ra.enabled = False
            mra.enabled = False """
            escmenu.enabled = False
            player.killMenu.enabled = False
            cursor.enabled = False

            # Clear entities
            destroy(player.right_hand)
            destroy(player.left_hand)
            destroy(player.health_bar)
            destroy(player.username_text)
            destroy(player)
            destroy(sky)
            """ destroy(ra)
            destroy(mra) """
            destroy(escmenu)
            destroy(player.killMenu)
            destroy(cursor)

            # Show mouse
            mouse.visible = True

            # Go back in menu manager
            self.menu_manager.go_back()
        
        
        global returntogame
        def returntogame():
            global escmenuenabled
            player.enabled = True
            escmenuenabled = False
            escmenu.hideMenu()
            

            
        
        #mob    
        #set mob to an acronyme for move_entity
        #mob code
        """ class RickAstley(Entity):
            def __init__(self, position = (0,3,0)):
                super().__init__(
                    parent = scene,
                    position = position,
                    model = 'assets/rs/objects/default_obj',
                    texture = 'assets/rs/images/ra2',
                    scale = 10,
                    collider = "box")
        ra = RickAstley(position=(0, -10, 0))
        boss1_sound.play()            

        class MiniRickAsltey(Entity):
            def __init__(self, position = ra.position):
                super().__init__(
                    parent = scene,
                    position = position,
                    model = 'assets/rs/objects/default_obj',
                    texture = 'assets/rs/images/ra2',
                    scale = 2.75,
                    collider = "box")
        mra = MiniRickAsltey() """
                
        class Cursor(Entity):
            def __init__(self):
                super().__init__(
                    parent = camera.ui,
                    position = (0, 0),
                    texture = 'assets/rs/images/cursor.png',
                    model = 'quad',
                    scale = .032,
                    color = color.white,
                    always_on_top = True
                )
                # self.always_on_top_setter(True)
            def update(self):
                if (player.enabled):
                    self.position = Vec2(0, 0)
                else:
                    self.position = Vec2(mouse.x, mouse.y)
                    mouse.visible = False
        
        global cursor
        cursor = Cursor()

        #blocks    
        all_blocks = []
        global prev_player_position
        prev_player_position = player.position

        # Base Block class

        class Block(Button):
            is_destroyed:bool
            is_reachable:bool

            def __init__(self, texture, position=(0, 0, 0)):
                super().__init__(
                    parent=scene,
                    position=position,
                    model='assets/rs/objects/block',
                    origin_y=0.5,
                    texture=texture,
                    color=color.color(0, 0, random.uniform(0.9, 0.95)),
                    #highlight_color=color.lime,
                    #highlight_color=color.rgba(255,255,255,.5),
                    highlight_color=color.white,
                    scale=0.5,
                    collider='box'
                )
                self.is_destroyed = False  # Add a flag to track if the block is destroyed
                self.is_reachable = True  # Default flag for reachable

                self.block_dict:dict = {
                    1: GrassBlock,
                    2: StoneBlock,
                    3: BrickBlock,
                    4: DirtBlock,
                    5: BedrockBlock,
                    6: GlassBlock,
                    7: BasicWoodBlock,
                    8: BasicWoodBlockPlanks
                }

                all_blocks.append(self)

            """ def update(self):
                global prev_player_position
                if player.position is None or distance(player.position, prev_player_position) > refresh_rate:
                    prev_player_position = player.position
                    for block in all_blocks:
                        dist = distance(block.position, player.position)
                        if dist < render_distance:
                            if not block.is_reachable:
                                block.is_reachable = True
                                block.highlight_color = color.white
                            block.ignore = False
                        else:
                            if block.is_reachable:
                                block.is_reachable = False
                                block.highlight_color = color.black
                            block.ignore = True """
            
            """ def update(self):
                global prev_player_position
                if player.position is None or distance(player.position, prev_player_position) > refresh_rate:
                    prev_player_position = player.position
                    dist = distance(self.position, player.position)
                    if dist < render_distance:
                        if not self.is_reachable:
                            self.is_reachable = True
                            self.highlight_color = color.white
                    else:
                        if self.is_reachable:
                            self.is_reachable = False
                            self.highlight_color = color.black """
            
            """ def update(self):
                self.is_reachable = distance(self.position, player.position) < render_distance
                self.highlight_color = color.white if self.is_reachable else color.black """
            
            def update(self):
                dist = distance(self.position, player.position)
                if dist < render_distance:
                    if not self.is_reachable:
                        self.is_reachable = True
                        self.highlight_color = color.white
                else:
                    if self.is_reachable:
                        self.is_reachable = False
                        self.highlight_color = color.black

            def input(self, key):
                if self.hovered and self.is_reachable:
                    if key == 'right mouse down' and player.enabled:
                        self.play_create_sound()

                        # Create the block from block atlas
                        self.block_dict.get(block_pick)(position = self.position + mouse.normal)
                    elif key == 'left mouse down' and player.enabled:
                        self.play_destroy_sound()
                        self.destroy_block()
            
            def play_create_sound(self):
                punch_sound.play()
            
            def play_destroy_sound(self):
                punch_sound.play()

            def destroy_block(self):
                if not self.is_destroyed:
                    self.is_destroyed = True
                    destroy(self)

                    all_blocks.remove(self)
            
            # Make a force_destroy method that can't be changed
            @staticmethod
            def force_destroy(self):
                destroy(self)

                all_blocks.remove(self)

        """ # Base Block class
        class Block(Button):
            def __init__(self, texture, position=(0, 0, 0), cooldown=1.0):
                super().__init__(
                    parent=scene,
                    position=position,
                    model='assets/rs/objects/block',
                    origin_y=0.5,
                    texture=texture,
                    color=color.color(0, 0, random.uniform(0.9, 1)),
                    highlight_color=color.white,
                    scale=0.5,
                    collider='box'
                )
                self.block_texture = texture
                self.is_destroyed = False  # Flag to track if the block is destroyed
                self.cooldown = cooldown  # Time in seconds required to break the block
                self.hold_start_time = None  # Time when the player started holding the left mouse button
                self.holding = False  # Flag to indicate if the player is holding the mouse button
                all_blocks.append(self)

            def update(self):
                if self.holding and self.hovered:
                    current_time = time.time()
                    if current_time - self.hold_start_time >= self.cooldown:
                        self.holding = False  # Reset holding state
                        self.on_destroy()
                else:
                    self.holding = False  # Reset if not hovered or not holding

                global prev_player_position
                if player.position is None or distance(player.position, prev_player_position) > refresh_rate:
                    prev_player_position = player.position
                    for block in all_blocks:
                        dist = distance(block.position, player.position)
                        if dist < render_distance:
                            if block.position in deactivated_blocks:
                                deactivated_blocks.remove(block.position)
                            block.visible = True
                            block.ignore = False
                            block.enabled = True
                        else:
                            if block.position not in deactivated_blocks:
                                deactivated_blocks.append(block.position)
                            block.visible = True
                            block.ignore = True
                            block.enabled = True

            def input(self, key):
                if self.hovered:
                    if key == 'right mouse down' and player.enabled:
                        self.play_create_sound()
                        if block_pick == 1: block_texture = GrassBlock
                        if block_pick == 2: block_texture = StoneBlock
                        if block_pick == 3: block_texture = BrickBlock
                        if block_pick == 4: block_texture = DirtBlock
                        if block_pick == 5: block_texture = BedrockBlock
                        if block_pick == 6: block_texture = GlassBlock
                        if block_pick == 7: block_texture = BasicWoodBlock
                        if block_pick == 8: block_texture = BasicWoodBlockPlanks
                        block_texture(position = self.position + mouse.normal)

                    elif key == 'left mouse down' and player.enabled:
                        # Start holding for block destruction
                        self.hold_start_time = time.time()
                        self.holding = True
                    elif key == 'left mouse up':
                        # Stop holding if the button is released
                        self.holding = False

            def play_create_sound(self):
                punch_sound.play()

            def play_destroy_sound(self):
                punch_sound.play()

            def on_destroy(self):
                if not self.is_destroyed:
                    self.play_destroy_sound()
                    self.is_destroyed = True
                    BlockItemEntity(texture=self.texture, original_block=type(self), position=self.position)
                    destroy(self)
                    all_blocks.remove(self) """
        
        class BlockItemEntity(Entity):
            def __init__(self, texture, original_block: str, position=(0, 0, 0)):
                super().__init__(
                    parent=scene,
                    position=position,
                    model='assets/rs/objects/block',
                    origin_y=0.7,  # Adjusted origin_y for proper alignment
                    texture=texture,
                    scale=0.1
                )
                self.collider = BoxCollider(self)
                self.block = original_block
                self.velocity_y = 0  # Vertical velocity
                self.gravity = -9.8  # Gravity constant

            def update(self):
                # Apply gravity to the velocity
                self.velocity_y += self.gravity * time.dt
                
                # Calculate potential new position
                potential_y = self.y + self.velocity_y * time.dt
                
                # Check for collision
                if self.detect_collision(potential_y):
                    # If collision is detected, stop the movement
                    self.velocity_y = 0
                else:
                    # Otherwise, apply the velocity
                    self.y = potential_y
                
                # Additional rotation logic
                self.rotation_y += 1

            def detect_collision(self, potential_y):
                # Create a bounding box for the new position
                potential_position = Vec3(self.x, potential_y, self.z)
                self.collider = BoxCollider(self)  # Update collider to potential position
                hit_info = self.intersects()
                
                if hit_info.hit:
                    # If there is a collision, return True
                    return True
                return False


        # Specific block types
        class GrassBlock(Block):
            def __init__(self, position=(0, 0, 0)):
                super().__init__(texture='assets/rs/images/grass_block.png', position=position)
        
        class StoneBlock(Block):
            def __init__(self, position=(0, 0, 0)):
                super().__init__(texture='assets/rs/images/stone_block.png', position=position)

        class BrickBlock(Block):
            def __init__(self, position=(0, 0, 0)):
                super().__init__(texture='assets/rs/images/brick_block.png', position=position)

        class DirtBlock(Block):
            def __init__(self, position=(0, 0, 0)):
                super().__init__(texture='assets/rs/images/dirt_block.png', position=position)

        class BedrockBlock(Block):
            def __init__(self, position=(0, 0, 0)):
                super().__init__(texture='assets/rs/images/bedrock_block.png', position=position)
            
            def destroy_block(self):
                # Bedrock can't be destroyed
                pass

        class GlassBlock(Block):
            def __init__(self, position=(0, 0, 0)):
                super().__init__(texture='assets/rs/images/glass_block.png', position=position)
            
            def play_destroy_sound(self):
                # Play glass destroying sound
                glass_sound.play()

        class BasicWoodBlock(Block):
            def __init__(self, position=(0, 0, 0)):
                super().__init__(texture='assets/rs/images/basic_wood_block.png', position=position)

        class BasicWoodBlockPlanks(Block):
            def __init__(self, position=(0, 0, 0)):
                super().__init__(texture='assets/rs/images/basic_wood_planks_block.png', position=position)
        
        class DEBUG_CHOCOLATE_CAKE_BLOCK(Block):
            def __init__(self, position=(0,0,0)):
                super().__init__(texture='assets/rs/images/old_basic_wood_block.png', position=position)

        global save_world
        def save_world():
            with open('{}/world.pcw'.format(worldname), 'w') as file:
                for i, voxel in enumerate(all_blocks, 1):
                    file.write(f'{voxel.position}:{type(voxel).__name__}\n')
                    escmenu.showStateText("Finished saving world")

        def load_world():
            try:
                block_atlas = {'GrassBlock': GrassBlock, 'StoneBlock': StoneBlock, 'BrickBlock': BrickBlock, 'DirtBlock': DirtBlock, 'BedrockBlock': BedrockBlock, 'GlassBlock': GlassBlock, 'BasicWoodBlock': BasicWoodBlock, 'BasicWoodBlockPlanks': BasicWoodBlockPlanks}
                with open(f"{worldname}/world.pcw", "r") as file:
                    lines = file.readlines()
                    total_lines = len(lines)
                    for line_id, line in enumerate(lines, start=0):
                        #print((line_id * 100) / total_lines)
                        line = line.strip()
                        if line:
                            position, block_class_name = line.split(":")
                            position = tuple(map(int, position.replace('Vec3(', '').replace(')', '').split(',')))

                            block = block_atlas.get(block_class_name, DEBUG_CHOCOLATE_CAKE_BLOCK) # Load block
                            block(position = position) # Insert it

            except FileNotFoundError :
                """ print("startng world resetting...")
                default_world = open('worlds/default/world.pcw', "r")
                open('{}/world.pcw'.format(worldname), "w").writelines(default_world)
                load_world() """

                # Implement a recreation of the world with the base seed
                print("world.pcw not found in your world.")
                PyneQuit(1)

        
        class EscMenu(Entity):
            def __init__(self):
                super().__init__(
                    enabled=True, # Enable it
                    color=color.hsv(0, 0, .5, .5), # Use transparent gray, so we can see-through 
                    scale=(window.aspect_ratio, 1),  # Scale adjusted for correct aspect ratio
                    position=(0, 0),  # Center the menu on screen
                    parent=camera.ui, # Set the parent to CameraUI
                    model='quad' # Set the model to quad
                )
                Text(
                    "PAUSED",
                    position=(0, .2),
                    scale=(3 / window.aspect_ratio, 3),  # Apply inverse scale to text
                    origin=(0, 0), # Center the origin
                    parent=self,
                    font="assets/rs/fonts/Pixelon.otf"
                ) # Make the PAUSED Text

                PyneButton(
                    text="Return to The Game",
                    xPos=.0, yPos=.1,
                    ySize=.07, xSize=.4 / window.aspect_ratio,
                    onClick=returntogame,
                    tooltip="Click here to return to the game",
                    parent=self
                ) # Return to game Button

                savebtn_mainmenubtn_Group = Entity(parent=self, position=(0, 0))  # Group the Save World and Go to menu

                PyneButton(
                    text="Save World",
                    xPos=-.11 / window.aspect_ratio, yPos=.0,
                    ySize=.07, xSize=.18 / window.aspect_ratio,
                    onClick=save_world,
                    tooltip="Click here to save world",
                    parent=savebtn_mainmenubtn_Group
                ) # Save World Button

                PyneButton(
                    text="Main Menu",
                    xPos=.11 / window.aspect_ratio, yPos=0,
                    ySize=.07, xSize=.18 / window.aspect_ratio,
                    onClick=go_back, 
                    tooltip="Save the world, and go to the main menu",
                    parent=savebtn_mainmenubtn_Group
                ) # Main menu Button

                PyneButton(
                    text="Quit The Game",
                    xPos=.0, yPos=-.1,
                    ySize=.07, xSize=.4 / window.aspect_ratio,
                    onClick=PyneQuit,
                    tooltip="Click here to quit the game",
                    parent=self
                ) # Quit the game button

                self.__stateText = Text(
                    "",
                    position=(0, -.2),
                    scale=(1 / window.aspect_ratio, 1),
                    origin=(0, 0),
                    parent=self,
                    font="assets/rs/fonts/Pixelon.otf"
                ) # This is state text. The state text is a text to show like "World saved" or other things. You can show text by doing escmenu.showStateText(text="Some State Text")
                        
                
                self.hideMenu() # By default, the player is playing, and not paused

            def showMenu(self): # Use this function to show the esc menu
                self.visible = True

                for item in self.children:
                    if not isinstance(item, Entity): # If the children isn't an entity, don't do anything with it
                        pass
                    item.enabled = True # Enable the item

            def hideMenu(self): # Use this function to hide the esc menu
                self.visible = False

                for item in self.children:
                    if not isinstance(item, Entity): # If the children isn't an entity, don't do anything with it
                        pass
                    
                    item.enabled = False # Disable the item
            
            def showStateText(self, text:str):
                self.__stateText.text = text
                invoke(self.__stateText.__setattr__, 'text', '', delay=3) # Clear the text after 3 seconds using ursina invoke

        global escmenu
        escmenu = EscMenu()

        #Sky
        class Sky(Entity):
            def __init__(self):
                super().__init__(
                parent = scene,
                model = 'sphere',
                texture = sky_texture,
                scale = 150,
                double_sided = True)
            def update(self):
                self.position = player.position
        #Hand
        
                
        """ load_world_process:Thread = Thread(target=load_world, args="")
        load_world_process.start() """
        load_world()
 
        """ def move_entity(e1=ra, e2=player, speed=1.5, gravity=-0.1, y_velocity=0, power=1, isdamaging=True, knowback=True, collisions=True):
            if player.enabled == True:
                direction = (e2.position - e1.position).normalized()
                distance = (e2.position - e1.position).length()
                e1.rotation_y = atan2(direction.x, direction.z) * 180 / pi
                if distance > 1:
                    e1.position += direction + Vec3(0, gravity, 0)* speed * time.dt
                if distance < 1:
                    if isdamaging == True:
                        player.damage(power)
                        if knowback == True:
                            e1.position = e1.position + Vec3(1, 0.5, 1)
                if collisions == True:
                    hit_info = e1.intersects()
                    if hit_info.hit:
                        e1.position = e1.position + Vec3(0, 0.1, 0)
                        print("AAAH, BBBBBBBh") """
            
        sky = Sky()

    def update(self):
        """ if player.health == 0 and not player.isDead:
            player.kill() """

        # This code destroy the old ursina default cursor, and make it an blank entity to don't destroy the code
        destroy(player.cursor)
        player.cursor = Entity()
    
    def input(self, key):
            global block_pick
            global fullscreen
            global camera_pos
            if key == 'escape' and not isplayerkilled:
                global escmenuenabled

                if escmenuenabled == False:
                    escmenu.showMenu()
                    player.enabled = False
                    escmenuenabled = True
                else:
                    escmenu.hideMenu()
                    player.enabled = True
                    escmenuenabled = False

            if key == 'b':
                PyneQuit()
            if key == 'r':
                player.respawn()
            if key == 'k':
                player.damage(20)
            if key == "t":
                player.damage(1)

            if key == "1": block_pick = 1
            if key == "2": block_pick = 2
            if key == "3": block_pick = 3
            if key == "4": block_pick = 4
            if key == "5": block_pick = 5
            if key == "6": block_pick = 6
            if key == "7": block_pick = 7
            if key == "8": block_pick = 8

            if key == "left mouse down" and player.enabled:
                player.left_hand.active()
            else:
                player.left_hand.passive()
            
            if key == "right mouse down" and player.enabled:
                player.right_hand.active()
            else:
                player.right_hand.passive()
    
    def show(self):
        pass
    
    def hide(self):
        pass

    def killMe(self):
        pass