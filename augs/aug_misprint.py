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
        is_upper = True if letter.isupper() else False
        if letter.lower() in self._marks:
                m = self._marks[letter]
                mark = random.choice(m)
                if is_upper:
                    mark=mark.capitalize()
                newtext = text.replace(letter, mark)
                return newtext
