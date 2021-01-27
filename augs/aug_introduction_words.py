from augs.base_aug import BaseAug
import random
import pymorphy2

class Aug_introduction_words(BaseAug):

    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()
        self.introduction_words_lst= open("/augs/files/introduction_words.txt","r").read().split("\n")

    def apply(self, text: str):
        txt = text.split(" ")
        firstword = self.morph.parse(txt[0])[0]
        if "Name" not in firstword.tag and "Geox" not in firstword.tag:
            txt[0] = txt[0].lower()
        newword = random.choice(self.introduction_words_lst)
        count = len(txt) - 1
        place = random.randint(0, count)
        if txt[place - 1] != "не" and txt[place - 1] != "ни" and txt[place - 1] != "ли":
            txt.insert(place, ",")
            txt.insert(place, newword)
            if place != 0:
                txt.insert(place, ",")
        txt[0] = txt[0].capitalize()
        newtext = " ".join(txt)
        newtext = newtext.replace(" ,", ",")
        newtext = newtext.replace(",.", ".")
        return (newtext)
