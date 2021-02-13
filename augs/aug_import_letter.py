import random
import json

from augs.base_aug import BaseAug


#аугментация, которая добавляет одну букву в слово, учитывая ближайшее окуржение вокруг буквы на клавиатуре
class AugAddLetter(BaseAug):

    def __init__(self):
        with open("files/marks.json",'r', encoding='utf-8') as marks:
            self._marks=json.load(marks)

    def apply(self, text: str):
        letter = random.choice(text)
        if letter.lower() in self._marks:
            m = self._marks[letter]
            mark = random.choice(m)
            newtext = text.replace(letter, letter+mark)
            return newtext
