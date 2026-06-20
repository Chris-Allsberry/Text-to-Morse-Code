class Morse:
    def __init__(self, message: str):
        self.__alphabet = {
            'a': '. -',
            'b': '- . . .',
            'c': '- . - .',
            'd': '- . .',
            'e': '.',
            'f': '. . - .',
            'g': '- - .',
            'h': '. . . .',
            'i': '. .',
            'j': '. - - -',
            'k': '- . -',
            'l': '. - . .',
            'm': '- -',
            'n': '- .',
            'o': '- - -',
            'p': '. - - .',
            'q': '- - . -',
            'r': '. - .',
            's': '. . .',
            't': '-',
            'u': '. . -',
            'v': '. . . -',
            'w': '. - -',
            'x': '- . . -',
            'y': '- . - -',
            'z': '- - . .',
            '1': '. - - - -',
            '2': '. . - - -',
            '3': '. . . - -',
            '4': '. . . . -',
            '5': '. . . . .',
            '6': '- . . . .',
            '7': '- - . . .',
            '8': ' - - - . .',
            '9': ' - - - - .',
            '0': ' - - - - -',
        }
        self.__word_list = self.__parser(message=message)
        self.__morse_list = None
        self.__translator()
        self.morse_code = self.__create_morse()

    def __parser(self, message):
        message = message.lower()
        return message.split(sep=' ')

    def __translator(self):
        output = []
        for word in self.__word_list:
            new_word = []
            for char in word:
                new_char = self.__alphabet.get(char)
                if new_char:
                    new_word.append(new_char)
            output.append(new_word)
        self.__morse_list = output

    def __create_morse(self):
        my_string = ""
        for word in self.__morse_list:
            for char in word:
                my_string += char
                my_string += '   '
            my_string += '       '
        my_string = my_string.strip()
        if my_string == "":
            my_string = " "
        return my_string


if __name__ == '__main__':
    from .tones import ToneGenerator
    message = 'Hi My Name is Chris!'
    ms = Morse(message=message)
    tg = ToneGenerator(ms.morse_code)
    tg.create_wav()