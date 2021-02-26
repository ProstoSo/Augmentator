import random

import pyonmttok

from augs.base_aug import BaseAug


class AugRandomDelWord(BaseAug):
    """ Аугментация, которая удаляет случайное слово в предложении """

    def __init__(self):
        self._tokenizer = pyonmttok.Tokenizer('aggressive')

    def apply(self, text: str) -> str:
        tokens = self._tokenizer.tokenize(text)[0]
        is_upper = True if tokens[0].isupper() else False
        n_tokens = len(tokens)
        r = random.randint(0, n_tokens - 1)
        tokens.remove(tokens[r])
        if is_upper:
            tokens[0] = tokens[0].capitalize()
        newtext = ' '.join(tokens)
        return newtext


class AugRandomDelLetter(BaseAug):
    """ Аугментация, которая удаляет случайную букву в слове """

    def apply(self, text: str) -> str:
        letter = random.choice(text)
        newtext = text.replace(letter, '')
        return newtext
