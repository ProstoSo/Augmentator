import random
import json

from augs.base_aug import BaseAug


#аугментация, которая заменяет букву в слове на одну из букв в ближайщем окружении на клавиатуре
class AugMisprint(BaseAug):

    def __init__(self):
        with open("augs/files/marks.json", 'r') as marks:
            self._marks = json.load(marks)

    def apply(self, text: str):
        letter = random.choice(text)
        if letter.isupper():
            t=1
        else:
            t=0
        for l in self._marks["letters"][0]:
            if l == letter.lower():
                m = self._marks["letters"][0][l]
                mark = random.choice(m)
                if t==1:
                    mark=mark.capitalize()
                newtext = text.replace(letter, mark)
                return newtext
