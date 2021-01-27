from augs.base_aug import BaseAug
import random

class Aug_random_del_word(BaseAug):

    def __init__(self):
        pass
    def apply(self, text: str):
        text = text.split(" ")
        l = len(text)
        r = random.randint(0, l - 1)
        text.remove(text[r])
        text[0] = text[0].capitalize()
        newtext = " ".join(text)
        return newtext

class Aug_random_del_letter(BaseAug):

    def __init__(self):
        pass
    def apply(self, text: str):
        letter = random.choice(text)
        newtext=text.replace(letter,"")
        return newtext