import random

from .base_aug import BaseAug


#аугментация, которая удаляет случайное слово в предложении
class AugRandomDelWord(BaseAug):

    def apply(self, text: str):
        text = text.split(" ")
        is_upper = True if text[0].isupper() else False
        l = len(text)
        r = random.randint(0, l - 1)
        text.remove(text[r])
        if is_upper:
            text[0] = text[0].capitalize()
        newtext = " ".join(text)
        return newtext


#аугментация, которая удаляет случайную букву в слове
class AugRandomDelLetter(BaseAug):

    def apply(self, text: str):
        letter = random.choice(text)
        newtext=text.replace(letter,"")
        return newtext
