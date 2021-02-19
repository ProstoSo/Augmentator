import random
import json
import os

from .base_aug import BaseAug
from paths import FILES_PATH


#аугментация, которая добавляет одну букву в слово, учитывая ближайшее окуржение вокруг буквы на клавиатуре
class AugAddLetter(BaseAug):

    def __init__(self):
        with open(os.path.join(FILES_PATH, "marks.json"),'r', encoding='utf-8') as marks:
            self._marks=json.load(marks)

    def apply(self, text: str):
        letter = random.choice(text)
        if letter.lower() in self._marks:
            m = self._marks[letter]
            mark = random.choice(m)
            newtext = text.replace(letter, letter+mark)
            return newtext
