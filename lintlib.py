import re
import json
from errors import InvalidFileExension
from definitions import EXTENSIONS
from pathlib import Path
from collections import namedtuple
from pprint import pprint
from languages import Java, Cpp
from string import ascii_letters, digits, whitespace, printable
from string import ascii_uppercase as uppercase
from string import ascii_lowercase as lowercase
import colorama
from colorama import Fore, Style

Token = namedtuple('Token', ['pos', 'type', 'value'])
colorama.init()


class Linter:
    def __init__(self, filename: str):
        ext = Path(filename).suffix
        if ext not in EXTENSIONS:
            raise InvalidFileExension(ext)
        self.filename = filename
        self.msg: str = ''

    def analyze(self):
        with open(self.filename) as f:
            text_program = f.read().splitlines()
        tokenizer = Tokenizer(text_program)
        tokens_list = tokenizer.tokenize()
        self.__check_rules(tokens_list)
        print(f'Run linter for {self.filename}')
        if self.msg:

            print(Fore.RED + 'UNSUCCESSFUL')
            for line in self.msg.splitlines():
                print(line)
        else:
            print(Fore.GREEN + 'SUCCESSFUL')
        print(Style.RESET_ALL + '\n')

    def __read_json(self):
        with open('config.json') as config:
            data = json.load(config)
        return data

    def __check_rules(self, tokens_list):
        config = self.__read_json()
        java_rules = config['java']['rules']
        # cpp_rules = config['cpp']
        indent_rule = java_rules['indent']
        spaces_around_the_operator = java_rules['spaces_around_the_operator']
        count_of_empty_lines = java_rules['count_of_empty_lines']
        practice_of_writing = java_rules['practice_of_writing']

        _count_of_empty_lines = 0
        shift_level = 0
        for tokens in tokens_list:
            # count_of_empty_lines
            if len(tokens) == 1 and tokens[0].type == TokenType.EMPTY_LINE:
                _count_of_empty_lines += 1
            else:
                if self.__check_count_of_empty_lines(count_of_empty_lines,
                                                     _count_of_empty_lines):
                    self.add_message(tokens[0].pos, f'Too many empty lines')
                _count_of_empty_lines = 0
                for i in range(len(tokens)):
                    if tokens[i].value == '{':
                        shift_level += 1
                    # elif tokens[i].value == '}':
                    #     shift_level -= 1

                    elif (tokens[i].type == TokenType.OP
                          and tokens[
                              i].value not in Java.bracket_operators_and_calls):
                        if spaces_around_the_operator:
                            if i == 0:
                                if self.__check_spaces_around_the_operator(
                                        cur=tokens[i], next=tokens[i + 1]):
                                    self.add_message(tokens[i].pos,
                                                     f'Missing whitespace around the operator {tokens[i].value}')
                            elif i == len(tokens) - 1:
                                if self.__check_spaces_around_the_operator(
                                        cur=tokens[i], prev=tokens[i - 1]):
                                    self.add_message(tokens[i].pos,
                                                     f'Missing whitespace around the operator {tokens[i].value}')
                            else:
                                if self.__check_spaces_around_the_operator(
                                        cur=tokens[i], prev=tokens[i - 1],
                                        next=tokens[i + 1]):
                                    self.add_message(tokens[i].pos,
                                                     f'Missing whitespace around the operator {tokens[i].value}')
                    elif tokens[i].type == TokenType.NAME:
                        if self.__check_practice_of_writing(tokens[i].value,
                                                            practice_of_writing):
                            self.add_message(tokens[i].pos,
                                             f'Invalid naming format')
                    elif tokens[i].type == TokenType.INDENT:
                        if tokens[i+1].value == '}':
                            shift_level -= 1
                        if self.__check_indent_rule(tokens[i].value,
                                                    indent_rule, shift_level):
                            self.add_message(tokens[i].pos,
                                             f'Invalid indent level')

    @staticmethod
    def __check_practice_of_writing(name: str, practice: str):
        if name in Java.common_classes:
            return False
        if practice == 'camelcase':
            if name[0] not in lowercase:
                return True
            if '_' in name:
                return True
        elif practice == 'pascalcase':
            if name[0] not in uppercase:
                return True
            if '_' in name:
                return True
        elif practice == 'snakecase':
            if set(uppercase).intersection(set(name[1:])):
                return True
        return False

    @staticmethod
    def __check_count_of_empty_lines(expected: int, actual: int):
        if actual > expected:
            return True
        return False

    @staticmethod
    def __check_spaces_around_the_operator(cur, prev=None, next=None):
        if next and next.type != 'SPACE':
            return True

        if prev and prev.type != 'SPACE':
            return True

        return False

    @staticmethod
    def __check_indent_rule(indent: str, rule, shift_level):
        if len(indent) != rule * shift_level:
            return True
        return False

    def add_message(self, pos, text):
        pos = str(pos)
        pattern = '{: <12} | {text}'.format(pos, text=text)
        self.msg += Fore.RED + pattern + '\n'


class TokenType:
    EMPTY_LINE = 'EMPTY LINE'
    INDENT = 'INDENT'
    SPACE = 'SPACE'
    KEYWORD = 'KEYWORD'
    NAME = 'NAME'
    VAR = 'VAR'
    OP = 'OP'


class Tokenizer:
    # Класс внутри класса
    def __init__(self, text):
        self.__text = text

    def tokenize(self):
        tokens = []
        text = self.__text
        for row_number in range(len(text)):
            cur_tokens = []
            if text[row_number] in whitespace:
                cur_tokens.append(Token((row_number + 1, 0), 'EMPTY LINE', ''))
                tokens.append(cur_tokens)
                continue

            whitespaces_idx = [m.start() for m in
                               re.finditer(' ', text[row_number])]

            count = 1
            indent = False
            for idx in range(len(whitespaces_idx)):
                if whitespaces_idx[idx] == 0 and idx == 0:
                    indent = True
                    continue

                elif indent:
                    if whitespaces_idx[idx] - whitespaces_idx[idx - 1] == 1:
                        count += 1
                    else:
                        if indent:
                            indent = False
                            cur_tokens.append(Token((row_number + 1,
                                                    0),
                                                    'INDENT',
                                                    ' ' * count))
                            count = 1
                        cur_tokens.append(Token((row_number + 1,
                                                 whitespaces_idx[idx]),
                                                'SPACE',
                                                ' ' * count))

                else:
                    if whitespaces_idx[idx] - whitespaces_idx[idx - 1] == 1:
                        count += 1
                    else:
                        indent = False
                        cur_tokens.append(Token((row_number + 1,
                                                 whitespaces_idx[idx]),
                                                'SPACE',
                                                ' ' * count))
                        count = 1

            row = text[row_number].split()
            for word in row:
                if word in Java.keywords:
                    cur_tokens.append(Token((row_number + 1,
                                             text[row_number].index(word)),
                                            'KEYWORD',
                                            word))
                    continue
                curr_word = ''
                for index in range(len(word)):
                    if index == len(word) - 1:
                        if (word[index] in ascii_letters
                                or word[index] in Java.quoates):
                            curr_word += word[index]
                            if curr_word in Java.keywords:
                                cur_tokens.append(Token(
                                    (row_number + 1,
                                     text[row_number].index(curr_word)),
                                    'KEYWORD',
                                    curr_word))
                            else:
                                if curr_word[0] in Java.quoates:
                                    cur_tokens.append(Token((
                                        row_number + 1,
                                        text[row_number].index(curr_word)),
                                        'VAR',
                                        curr_word))
                                else:
                                    cur_tokens.append(Token((
                                        row_number + 1,
                                        text[row_number].index(curr_word)),
                                        'NAME',
                                        curr_word))
                        elif word[index] in Java.operators:
                            if curr_word:
                                if curr_word in Java.keywords:
                                    cur_tokens.append(Token((
                                        row_number + 1,
                                        text[row_number].index(curr_word)),
                                        'KEYWORD',
                                        curr_word))
                                else:
                                    if curr_word[0] in Java.quoates:
                                        cur_tokens.append(Token((
                                            row_number + 1,
                                            text[row_number].index(curr_word)),
                                            'VAR',
                                            curr_word))
                                    else:
                                        cur_tokens.append(Token((
                                            row_number + 1,
                                            text[row_number].index(curr_word)),
                                            'NAME',
                                            curr_word))
                            cur_tokens.append(Token((
                                row_number + 1,
                                text[row_number].index(word[index])),
                                'OP',
                                word[index]))

                    else:
                        if (word[index] in ascii_letters
                                or word[index] in Java.quoates):
                            curr_word += word[index]

                        elif word[index] in Java.operators:
                            if curr_word:
                                if curr_word in Java.keywords:
                                    cur_tokens.append(Token((
                                        row_number + 1,
                                        text[row_number].index(curr_word)),
                                        'KEYWORD',
                                        curr_word))
                                else:
                                    if curr_word[0] in Java.quoates:
                                        cur_tokens.append(Token((
                                            row_number + 1,
                                            text[row_number].index(curr_word)),
                                            'VAR',
                                            curr_word))
                                    else:
                                        cur_tokens.append(Token((
                                            row_number + 1,
                                            text[row_number].index(curr_word)),
                                            'NAME',
                                            curr_word))
                            cur_tokens.append(Token((
                                row_number + 1,
                                text[row_number].index(word[index])),
                                'OP',
                                word[index]))
                            curr_word = ''
            cur_tokens = sorted(cur_tokens, key=lambda x: x.pos[1])
            tokens.append(cur_tokens)

        return tokens
