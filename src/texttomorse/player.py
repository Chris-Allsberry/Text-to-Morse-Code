import threading
import sys
from pathlib import Path
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame


class SoundPlayer:
    def __init__(self, path: Path):
        self.path = path
        self.stop_event = threading.Event()
        pygame.init()

    def _listen_for_quit(self): # Make this into a UI screen in UI module. Add input for UI screen here.
        print("Press 'q' + Enter to stop.")
        for line in sys.stdin:
            if line.strip().lower() == 'q':
                self.stop_event.set()
                break
            if self.stop_event.is_set():
                break


    def play_audio(self):
        pygame.mixer.music.load(self.path)
        pygame.mixer.music.play()
        listener = threading.Thread(target=self._listen_for_quit, daemon=True)
        listener.start()

        while pygame.mixer.music.get_busy():
            if self.stop_event.is_set():
                pygame.mixer.music.stop()
                break
            pygame.time.Clock().tick(10)

        self.stop_event.set()  # signal listener to exit if song ended naturally
        print("Playback finished.")

if __name__ == '__main__':
    cwd = Path.cwd()
    mypath = cwd / 'temp' / 'mywave.wav'
    sp = SoundPlayer(mypath)
    sp.play_audio()