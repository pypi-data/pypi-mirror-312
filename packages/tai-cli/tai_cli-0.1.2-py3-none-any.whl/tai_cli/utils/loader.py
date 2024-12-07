from itertools import cycle
from shutil import get_terminal_size
from threading import Thread
from time import sleep
import click

class Loader:
    def __init__(
            self,
            desc: str="Loading...",
            end: str="Done!",
            timeout: float=0.1,
            main_color: str='blue'):
        """
        A loader-like context manager

        Args:
            desc (str, optional): The loader's description. Defaults to "Loading...".
            end (str, optional): Final print. Defaults to "Done!".
            timeout (float, optional): Sleep time between prints. Defaults to 0.1.
        """
        self.desc = desc
        self.end = end
        self.timeout = timeout
        self.main_color = main_color

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False
    
    def msg(self, text: str, nl: bool=False):
        return click.echo(click.style(text, fg=self.main_color), nl=nl)

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            self.msg(f"\r{self.desc} {c}")
            sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        self.msg("\r" + " " * cols)
        self.msg(f"\r{self.end}\n", nl=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()