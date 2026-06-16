from pathlib import Path
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame


class SoundPlayer:
    def __init__(self, path: Path):
        self.path = path

    def play_audio(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():  # wait for playback to finish
            ui = input('press q to stop music')
            if ui.lower() == 'q':
                pygame.mixer.music.stop()
        print('done!')


if __name__ == '__main__':
    mypath = Path('mywave.wav')
    sp = SoundPlayer(mypath)
    sp.play_audio()