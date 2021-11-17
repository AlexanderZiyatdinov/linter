class BaseLinterException(Exception):
    pass


class InvalidFileExension(BaseLinterException):
    def __init__(self, ext: str):
        self.__ext = ext

    def __str__(self):
        return f'The file extension should be .java or .cpp, not {self.__ext}'
