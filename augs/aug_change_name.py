import random

import pymorphy2

from augs.base_aug import BaseAug


#аугментация, которая изменяет мужские имена на мужские, женские на женские, а имена неодназначно определяющие пол на имена такого типа
class AugChangeName(BaseAug):

    def __init__(self):
        with open("files/names.txt", "r", encoding='utf-8') as names:
            self._names_lst = names.read().split(" ")
        with open("files/femnames.txt", "r", encoding='utf-8') as fnames:
            self._fems_names_lst = fnames.read().split(" ")
        with open("files/mascnames.txt", "r", encoding='utf-8') as mnames:
            self._masc_names_lst = mnames.read().split(" ")
        self._morph=pymorphy2.MorphAnalyzer()

    def apply(self, text: str):
        txt=text.split(" ")
        for word in txt:
            firstword = self._morph.parse(word)[0]
            case = firstword.tag.case
            if "Name" in firstword.tag:
                newname=word
                if "ms-f" in firstword.tag:
                    newname = random.choice(self._names_lst)
                if "femn" in firstword.tag:
                    newname = random.choice(self._fems_names_lst)
                elif "masc" in firstword.tag:
                    newname = random.choice(self._masc_names_lst)
                newname2 = self._morph.parse(newname)[0]
                # выбираем нужную форму слова и меняем первую букву слова на заглавную
                newname3 = newname2.inflect({case}).word.capitalize()
                n = txt.index(word)
                txt[n] = newname3
        newtext = " ".join(txt)
        return newtext