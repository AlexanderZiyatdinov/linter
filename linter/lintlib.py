from typing import TextIO
from errors import InvalidFileExension
from definitions import EXTENSIONS
from pathlib import Path
from languages import Java, Cpp
from string import ascii_letters, digits, punctuation, whitespace, printable


class Linter:
    def __init__(self, filename: str):
        ext = Path(filename).suffix
        if ext not in EXTENSIONS:
            raise InvalidFileExension(ext)
        self.filename = filename
        self.information: str = ''

    def analyze(self):
        with open(self.filename) as f:
            text_program = f.read().splitlines()
        tokenizer = Tokenizer(text_program)
        print(text_program)
        tokenizer.tokenize()


class Tokenizer:
    def __init__(self, text):
        self.__text = text

    def tokenize(self):
        for num_line in range(len(self.__text)):
            for char in self.__text[num_line]:


