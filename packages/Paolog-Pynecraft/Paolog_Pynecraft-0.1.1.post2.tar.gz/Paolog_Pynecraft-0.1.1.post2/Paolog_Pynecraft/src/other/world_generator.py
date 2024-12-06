from perlin_noise import PerlinNoise

from ...src.other.get_config_path import get_pynecraft_config_path as conf_path
from ...src.other.world_status import WORLD_GENERATOR_STATUS

from threading import Thread

import os

class WorldGenerator():
    def __init__(self):
        self.progression:int = 0
    
    def generate_world(self, world_name:str, seed:str, world_size:str) -> None:
        process:Thread = Thread(target=self.__generate_world, args=(world_name, seed, world_size))
        process.start()
    
    def __generate_world(self, world_name:str, seed:str, world_size:str) -> None:
        self.progression = 0
        try:
            seed_int:int = int.from_bytes(seed.encode(), 'big')

            noise:PerlinNoise = PerlinNoise(octaves=3, seed=seed_int)
            map_size:int = int(world_size)
            if map_size == 0:
                raise WORLD_GENERATOR_STATUS.WORLD_SIZE_0()
            if world_name == "":
                raise WORLD_GENERATOR_STATUS.EMPTY_WORLD_NAME()
            
            world_data:list = []

            world_folder:str = conf_path() + '/worlds/{}/'.format(world_name)
            if not os.path.exists(world_folder):
                try:
                    os.makedirs(world_folder)
                except OSError as e:
                    if (e.winerror == 123):
                        raise WORLD_GENERATOR_STATUS.INVALID_WORLD_NAME()
                    else:
                        raise WORLD_GENERATOR_STATUS.OS_ERROR()
                open(world_folder + "world.pcw", "w+")

            for z in range(map_size):
                total = pow(map_size, 2)
                self.progression += (map_size * 90) / total
                for x in range(map_size):
                    y=round(noise([x/map_size,z/map_size])*10)
                    for i in range(y):
                        if i==y-1:
                            world_data.append(f"Vec3({x},{i},{z}):GrassBlock")
                            break
                        elif i>=y-3:
                            world_data.append(f"Vec3({x},{i},{z}):DirtBlock")
                            continue
                        world_data.append(f"Vec3({x},{i},{z}):StoneBlock")
                    world_data.append(f"Vec3({x},-5,{z}):BedrockBlock")
                    for i in range(-4, 0):
                        world_data.append(f"Vec3({x},{i},{z}):StoneBlock")
            with open(conf_path() + '/worlds/{}/world.pcw'.format(world_name), 'w') as file:
                for line in world_data:
                    file.write(line + " \n")
            
            self.__finish_generation(world_name=world_name, seed=seed, world_size=world_size)
        except WORLD_GENERATOR_STATUS.INVALID_WORLD_NAME:
            self.progression = -1
        except WORLD_GENERATOR_STATUS.EMPTY_WORLD_NAME:
            self.progression = -2
        except WORLD_GENERATOR_STATUS.OS_ERROR:
            self.progression = -100
        except WORLD_GENERATOR_STATUS.WORLD_SIZE_0:
            self.progression = -101
        except Exception as e:
            self.progression = -100
    
    def get_progression(self) -> int:
        return self.progression

    def __finish_generation(self, world_name:str, seed:str, world_size:str) -> None:
        with open(conf_path() + '/worlds/{}/info.txt'.format(world_name), 'w') as file:
            file.write(f"world_version=1\nworld_name={world_name}\nseed={seed}\nworld_size={world_size}")
        
        self.progression = 100