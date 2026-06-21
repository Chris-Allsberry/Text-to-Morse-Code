import os
from dataclasses import dataclass
from typing import Callable, Optional
import time
import datetime as dt
from tempfile import TemporaryDirectory
from pathlib import Path

from rich.console import Console
from rich.rule import Rule
from rich.progress import track

from .morse import Morse
from .tones import ToneGenerator
from .player import SoundPlayer
from .art import Gallery


@dataclass(frozen=True)
class NextScreen:
    func: Callable
    args: Optional[dict] = None


class UI:
    def __init__(self):
        self.art = Gallery()
        self.console = Console()
        self.temp_dir = TemporaryDirectory()
        self.power_on = True

    def __clear_screen(self):
        if os.name == 'nt':
            command = 'cls'
        else:
            command = 'clear'
        os.system(command)

    def __rule(self):
        message = "Text to Morse Converter"
        self.console.print(Rule(message))

    def screen_welcome(self) -> NextScreen:
        self.__clear_screen()
        self.__rule()
        self.console.print(self.art.welcome)
        self.console.input('Enter to Continue...')
        return NextScreen(func=self.screen_input_morse)

    def screen_goodbye(self):
        self.__clear_screen()
        self.__rule()
        self.console.print(self.art.goodbye)
        self.power_on = False
        time.sleep(1)
        self.__clear_screen()
        return None

    def screen_input_morse(self) -> NextScreen:
        message_ok = False
        while not message_ok:
            self.__clear_screen()
            self.__rule()
            prompt = 'Enter a phrase to translate: '
            message = self.console.input(prompt=prompt)
            if len(message) > 0:
                message_ok = True
        return NextScreen(func=self.screen_waiting, args={'message': message})

    def screen_waiting(self, message):
        self.__clear_screen()
        self.__rule()
        status = 'Wait...'
        sleep_seconds = 1
        with self.console.status(status=status, spinner='aesthetic'):
            start = dt.datetime.now()
            ms = Morse(message=message)
            temp_dir = Path(self.temp_dir.name)
            tg = ToneGenerator(message=ms.morse_code, save_directory=temp_dir)
            tg.create_wav()
            finish = dt.datetime.now()
            time_diff = finish - start
            if time_diff.seconds < sleep_seconds:
                time.sleep(sleep_seconds - time_diff.seconds)
            args = {
                'filepath': tg.file_path,
                'message': message,
                'morse': ms.morse_code
                }
        return NextScreen(self.screen_play_morse, args=args)

    def screen_play_morse(self, filepath: Path, message: str, morse: str):
        audio_played = False
        user_selection_ok = False
        while not user_selection_ok:
            self.__clear_screen()
            self.__rule()
            original_text = f'[red]Original Text:[/red] [bold]{message}[/bold]\n'
            self.console.print(original_text)
            morse_text = f'[green]Morse Code:[/green] [bold on blue]{morse}[/bold on blue]\n'
            self.console.print(morse_text)
            if not audio_played:
                pl = SoundPlayer(filepath)
                pl.play_audio()
                for i in track(range(pl.sound_length), description="Playing..."):
                    time.sleep(1)
                audio_played = True
            ask_prompt = 'Would you like to do another? ([green]y[/green]/[red]n[/red]): '
            us = self.console.input(ask_prompt)

            if us.lower() in ('y', 'n'):
                user_selection_ok = True
        if us.lower() == 'y':
            return NextScreen(self.screen_input_morse)
        elif us.lower() == 'n':
            return NextScreen(self.screen_goodbye)

    def run_ui(self):
        current_screen = NextScreen(self.screen_welcome)
        while self.power_on:
            if current_screen.args:
                next_screen = current_screen.func(**current_screen.args)
            else:
                next_screen = current_screen.func()
            current_screen = next_screen
        self.temp_dir.cleanup()
