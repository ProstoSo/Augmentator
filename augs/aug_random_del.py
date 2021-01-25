from augs.base_aug import BaseAug
import random

class NERAug(BaseAug):

    def __init__(self):
        pass
    def apply(self, text: str):
        text = text.split(" ")
        l = len(text)
        r = random.randint(0, l - 1)
        text.remove(text[r])
        text[0] = text[0].capitalize()
        newtext = " ".join(text)
        return f'{newtext}_augmented'