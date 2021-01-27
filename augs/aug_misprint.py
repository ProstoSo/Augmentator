from augs.base_aug import BaseAug
import random
import json

class Aug_misprint(BaseAug):

    def __init__(self):
        self._marks= json.load(open("augs/files/marks.json"))

    def apply(self, text: str):
        letter = random.choice(text)
        if letter.isupper()==True:
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