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
        while word1==word2:
            r1 = random.randint(0, l - 1)
            word1 = text[r1]
        s1 = ""
        s2=""
        for symb in [",", ".", "!", "?"]:
            if symb in word1:
                word1 = word1.replace(symb, "")
                s1 = symb
            if symb in word2:
                word2 = word2.replace(symb, "")
                s2 = symb
        if word1.istitle() or word2.istitle():
            firstword = self._morph.parse(word1)[0]
            if "Name" not in firstword.tag and "Geox" not in firstword.tag:
                word1 = word1.lower()
            secondword = self._morph.parse(word2)[0]
            if "Name" not in secondword.tag and "Geox" not in secondword.tag:
                word2 = word2.lower()
        text[r1] = word2+s1
        text[r2] = word1+s2
        text[0] = text[0].capitalize()
        newtext = " ".join(text)
        return newtext


#аугментация, которая меняет две соседние буквы в слове
class AugChangeLetters(BaseAug):

    def apply(self, text: str):
        letter = random.choice(text)
        letind=text.index(letter)
        if letind != 0:
            letter2= text[letind- 1]
            newtext = text.replace(letter2+letter, letter + letter2)
        else:
            letter2 = text[letind + 1]
            newtext = text.replace(letter+letter2, letter2+letter)

        return newtext