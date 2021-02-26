import random

import pymorphy2
import pyonmttok

from augs.base_aug import BaseAug
from augs.utils import remove_punctuation_with_sign, remove_whitespace


class AugRandomChangeWords(BaseAug):
    """ Аугментация, которая меняет местами два случайных слова в предложении """

    def __init__(self):
        self._morph = pymorphy2.MorphAnalyzer()
        self._tokenizer = pyonmttok.Tokenizer('aggressive')

    def apply(self, text: str):
        tokens = self._tokenizer.tokenize(text)[0]
        n_tokens = len(tokens)
        r1 = random.randint(0, n_tokens - 1)
        r2 = random.randint(0, n_tokens - 1)
        word1 = tokens[r1]
        word2 = tokens[r2]
        while word1 == word2:
            r1 = random.randint(0, n_tokens - 1)
            word1 = tokens[r1]
        word1, s1 = remove_punctuation_with_sign(word1)
        word2, s2 = remove_punctuation_with_sign(word2)
        if word1.istitle() or word2.istitle():
            firstword = self._morph.parse(word1)[0]
            if 'Name' not in firstword.tag and 'Geox' not in firstword.tag:
                word1 = word1.lower()
            secondword = self._morph.parse(word2)[0]
            if 'Name' not in secondword.tag and 'Geox' not in secondword.tag:
                word2 = word2.lower()
        tokens[r1] = word2 + s1
        tokens[r2] = word1 + s2
        tokens[0] = tokens[0].capitalize()
        newtext = ' '.join(tokens)
        newtext = remove_whitespace(newtext)
        return newtext


class AugChangeLetters(BaseAug):
    """ Аугментация, которая меняет две соседние буквы в слове """

    def apply(self, text: str) -> str:
        letter = random.choice(text)
        letind = text.index(letter)
        if letind != 0:
            letter2 = text[letind - 1]
            newtext = text.replace(letter2 + letter, letter + letter2)
        else:
            letter2 = text[letind + 1]
            newtext = text.replace(letter + letter2, letter2 + letter)

        return newtext
