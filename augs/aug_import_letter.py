from augs.base_aug import BaseAug
import random
import json

class Aug_add_letter(BaseAug):

    def __init__(self):
        self._marks= json.load(open("augs/files/marks.json"))

    def apply(self, text: str):
        letter = random.choice(text)
        for l in self._marks["letters"][0]:
            if l == letter.lower():
                m = self._marks["letters"][0][l]
                mark = random.choice(m)
                newtext = text.replace(letter, letter+mark)
                return newtext