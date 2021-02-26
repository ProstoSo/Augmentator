import os
import json
import random

from augs.base_aug import BaseAug
from augs.paths import FILES_PATH


class AugAddLetter(BaseAug):
    """ Аугментация, которая добавляет одну букву в слово, учитывая ближайшее окуржение вокруг буквы на клавиатуре """

    def __init__(self):
        with open(os.path.join(FILES_PATH, 'marks.json'), 'r', encoding='utf-8') as marks:
            self._marks = json.load(marks)

    def apply(self, text: str) -> str:
        letter = random.choice(text)
        if letter.lower() in self._marks:
            m = self._marks[letter.lower()]
            mark = random.choice(m)
            l_ind = text.index(letter) + 1
            text = text[:l_ind] + mark + text[l_ind:]
            text = text.replace(letter, letter+mark)
        return text
