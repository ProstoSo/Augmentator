from augs.base_aug import BaseAug
import random
import pymorphy2

class Aug_change_name(BaseAug):

    def __init__(self):
        self._names_lst = open("augs/files/names.txt","r").read().split(" ")
        self._masc_names_lst = open("augs/files/mascnames.txt", "r").read().split(" ")
        self._femn_names_lst  = open("augs/files/femnames.txt", "r").read().split(" ")
        self.morph=pymorphy2.MorphAnalyzer()

    def apply(self, text: str):
        for word in text:
            firstword = self.morph.parse(word)[0]
            case = firstword.tag.case
            if "Name" in firstword.tag:
                if "ms-f" in firstword.tag:
                    newname = random.choice(self.names_lst)
                if "femn" in firstword.tag:
                    newname = random.choice(self.fems_names_lst)
                elif "masc" in firstword.tag:
                    newname = random.choice(self.masc_names_lst)
                newname2 = self.morph.parse(newname)[0]
                # выбираем нужную форму слова и меняем первую букву слова на заглавную
                newname3 = newname2.inflect({case}).word.capitalize()
                n = text.index(word)
                text[n] = newname3
        newtext = " ".join(text)
        return (newtext)