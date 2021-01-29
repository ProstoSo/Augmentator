import random

import pymorphy2

from augs.base_aug import BaseAug


#аугментация, которая меняет местами два случайных слова в предложении
class AugRandomChangeWords(BaseAug):

    def __init__(self):
        self._morph = pymorphy2.MorphAnalyzer()

    def apply(self, text: str):
        text = text.split(" ")
        l = len(text)
        r1 = random.randint(0, l - 1)
        r2 = random.randint(0, l - 1)
        word1 = text[r1]
        word2 = text[r2]
        if word1.istitle() or word2.istitle():
            firstword = self._morph.parse(text[r1])[0]
            if "Name" not in firstword.tag and "Geox" not in firstword.tag:
                text[r1] = text[r1].lower()
            secondword = self._morph.parse(text[r2])[0]
            if "Name" not in secondword.tag and "Geox" not in secondword.tag:
                text[r2] = text[r2].lower()
        text[r1] = word2
        text[r2] = word1
        text[0] = text[0].capitalize()
        newtext = " ".join(text)
        return newtext


#аугментация, которая меняет две случайные буквы в слове
class AugChangeLetters(BaseAug):

##никаких атрибутов в этой функции не требуется, но я не знаю, можно ли писать так или нужно удалить def __init__ совсем
    def __init__(self):
        pass

    def apply(self, text: str):
        letter = random.choice(text)
        if text.index(letter) != 0:
            letter2= text[text.index(letter) - 1]
            newtext = text.replace(letter2+letter, letter + letter2)
        else:
            letter2 = text[text.index(letter) + 1]
            newtext = text.replace(letter+letter2, letter2+letter)

        return newtext