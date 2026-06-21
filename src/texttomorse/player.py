from pathlib import Path
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame


class SoundPlayer:
    def __init__(self, path: Path):
        pygame.init()
        self.sound = pygame.mixer.Sound(path)
        self.sound_length = int(self.sound.get_length())

    def play_audio(self):
        self.sound.play()
