import os
import random

import pymorphy2
import pyonmttok

from augs.base_aug import BaseAug
from augs.paths import FILES_PATH
from augs.utils import remove_whitespace


class AugIntroductionWords(BaseAug):
    """ Аугментация, которая добавляет вводные слова и необходимые запятые """

    def __init__(self):
        self._morph = pymorphy2.MorphAnalyzer()
        with open(os.path.join(FILES_PATH, 'introduction_words.txt'), 'r', encoding='utf-8') as inwords:
            self._introduction_words_lst = inwords.read().split('\n')
        self._tokenizer = pyonmttok.Tokenizer('aggressive')

    def apply(self, text: str) -> str:
        tokens = self._tokenizer.tokenize(text)[0]
        firstword = self._morph.parse(tokens[0])[0]
        if 'Name' not in firstword.tag and 'Geox' not in firstword.tag:
            tokens[0] = tokens[0].lower()
        newword = random.choice(self._introduction_words_lst)
        count = len(tokens) - 1
        place = random.randint(0, count)
        if tokens[place - 1] not in {'не', 'ни', 'ли'}:
            tokens.insert(place, ',')
            tokens.insert(place, newword)
            if place != 0:
                tokens.insert(place, ',')
        tokens[0] = tokens[0].capitalize()
        newtext = ' '.join(tokens)
        newtext = remove_whitespace(newtext)
        newtext = newtext.replace(',.', '.')
        return newtext
