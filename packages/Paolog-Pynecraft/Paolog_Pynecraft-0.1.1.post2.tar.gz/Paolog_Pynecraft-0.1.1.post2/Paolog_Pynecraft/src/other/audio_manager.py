from ursina import Audio
import os
import random

class PyneMusicManager():
    audio:Audio
    old_audio_sound:str = ""
    play_music:bool = False

    def __init__(self):
        self.audio = Audio()

    def start(self):
        self.play_music = True
        music = self.__getRandomMusic()
        if self.old_audio_sound == music:
            self.start()
        
        self.old_audio_sound = music
        self.audio = Audio(music, autoplay=True)
        self.audio.play()

    def stop(self):
        self.play_music = False

    def update(self):
        if not self.audio.playing and self.play_music:
            self.start()

    def __getRandomMusic(self) -> str:
        musics_dir = 'assets/rs/sounds/music'

        files:list[str] = os.listdir(musics_dir)

        music_files = [file for file in files if file.endswith(('.mp3', '.wav', '.ogg'))]

        if not music_files:
            pass

        random_music_file = random.choice(music_files)

        return os.path.join(musics_dir, random_music_file)
        
