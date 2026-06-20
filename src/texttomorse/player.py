from pathlib import Path
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame


class SoundPlayer:
    def __init__(self, path: Path):
        self.path = path
        pygame.init()

    def play_audio(self):
        sound = pygame.mixer.Sound(self.path)
        sound.play()
        pygame.time.wait(int(sound.get_length() * 1000))
