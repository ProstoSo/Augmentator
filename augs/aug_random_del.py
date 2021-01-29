import random

from augs.base_aug import BaseAug


#аугментация, которая удаляет случайное слово в предложении
class AugRandomDelWord(BaseAug):

    ##никаких атрибутов в этой функции не требуется, но я не знаю, можно ли писать так или нужно удалить def __init__ совсем
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


#аугментация, которая удаляет случайную букву в слове
class AugRandomDelLetter(BaseAug):

    ##никаких атрибутов в этой функции не требуется, но я не знаю, можно ли писать так или нужно удалить def __init__ совсем
    def __init__(self):
        pass

    def apply(self, text: str):
        letter = random.choice(text)
        newtext=text.replace(letter,"")
        return newtext
