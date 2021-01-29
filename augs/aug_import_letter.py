import random
import json

from augs.base_aug import BaseAug


#аугментация, которая добавляет одну букву в слово, учитывая ближайшее окуржение вокргу буквы на клавиатуре
class AugAddLetter(BaseAug):

    def __init__(self):
        with open("augs/files/marks.json",'r') as marks:
            self._marks=json.load(marks)

    def apply(self, text: str):
        letter = random.choice(text)
        for l in self._marks["letters"][0]:
            if l == letter.lower():
                m = self._marks["letters"][0][l]
                mark = random.choice(m)
                newtext = text.replace(letter, letter+mark)
                return newtext
