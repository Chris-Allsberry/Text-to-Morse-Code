from tones import SINE_WAVE, SAWTOOTH_WAVE
from tones.mixer import Mixer
from pathlib import Path


class ToneGenerator:
    def __init__(self, message: str, save_directory: Path):
        self.message = message
        self.mixer = Mixer(44100, 0.5)
        self.unit_length = .1
        self.file_path = save_directory / 'mywave.wav'
        self.functions = {
            '.': self.__add_dot,
            '-': self.__add_dash,
            ' ': self.__add_space
        }

    def __add_dot(self):
        self.mixer.add_note(
            trackname=0,
            note='c',
            octave=5,
            duration=self.unit_length
        )

    def __add_dash(self):
        self.mixer.add_note(
            trackname=0,
            note='c',
            octave=5,
            duration=self.unit_length * 3
        )

    def __add_space(self):
        self.mixer.add_silence(trackname=0, duration=self.unit_length)

    def __add_all_notes(self):
        self.mixer.create_track(0, SINE_WAVE)
        for char in self.message:
            myfunc = self.functions[char]
            myfunc()

    def create_wav(self):
        self.__add_all_notes()
        # self.mixer.write_wav(self.file_path.name)
        self.mixer.write_wav('mywave.wav')
        self.file_path = 'mywave.wav'

