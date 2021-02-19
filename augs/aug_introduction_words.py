import random
import os

import pymorphy2

from .base_aug import BaseAug
from paths import FILES_PATH


#аугментация, которая добавляет вводные слова и необходимые запятые
class AugIntroductionWords(BaseAug):

    def __init__(self):
        self._morph = pymorphy2.MorphAnalyzer()
        with open(os.path.join(FILES_PATH,"introduction_words.txt"),"r", encoding='utf-8') as inwords:
            self._introduction_words_lst = inwords.read().split("\n")

    def apply(self, text: str):
        txt = text.split(" ")
        firstword = self._morph.parse(txt[0])[0]
        if "Name" not in firstword.tag and "Geox" not in firstword.tag:
            txt[0] = txt[0].lower()
        newword = random.choice(self._introduction_words_lst)
        count = len(txt) - 1
        place = random.randint(0, count)
        if txt[place - 1] not in {'не', 'ни', 'ли'}:
            txt.insert(place, ",")
            txt.insert(place, newword)
            if place != 0:
                txt.insert(place, ",")
        txt[0] = txt[0].capitalize()
        newtext = " ".join(txt)
        newtext = newtext.replace(" ,", ",")
        newtext = newtext.replace(",.", ".")
        return newtext
