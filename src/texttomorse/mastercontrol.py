from .morse import Morse
from .tones import ToneGenerator

class MasterControl:
    def __init__(self, message):
        self.text = message

    def main(self):
        ms = Morse(self.text)
        tg = ToneGenerator(ms.morse_code)
        tg.create_wav()