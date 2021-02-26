import os
import json
import random

from augs.base_aug import BaseAug
from augs.paths import FILES_PATH


class AugMisprint(BaseAug):
    """ Аугментация, которая заменяет букву в слове на одну из букв в ближайщем окружении на клавиатуре """

    def __init__(self):
        with open(os.path.join(FILES_PATH, 'marks.json'), 'r', encoding='utf-8') as marks:
            self._marks = json.load(marks)

    def apply(self, text: str) -> str:
        letter = random.choice(text)
        is_upper = True if letter.isupper() else False
        if letter.lower() in self._marks:
                m = self._marks[letter.lower()]
                mark = random.choice(m)
                if is_upper:
                    mark = mark.capitalize()
                l_ind = text.index(letter)
                text = text[:l_ind] + mark + text[l_ind + 1:]
        return text
