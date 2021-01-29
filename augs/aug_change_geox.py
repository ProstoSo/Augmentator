import json
import random
import re

import pymorphy2

from augs.base_aug import BaseAug


#аугментация, которая заменяет одни географические названия другими, сохраняя тип топонима
class AugChangeGeox(BaseAug):

    def __init__(self):
        with open("augs/files/geox.json",'r') as geoxs:
            self._geoxs=json.load(geoxs)
        self._morph=pymorphy2.MorphAnalyzer()

    def apply(self, text: str):
        text = text.split(" ")
        for word in text:
            # ищем слово с заглавной буквы
            if word.istitle() == True:
                # проверяем, является найденное слово географическим названием
                firstword = self._morph.parse(word)[0]
                if "Geox" in firstword.tag:
                    newword=word
                    # запоминаем исходный падеж
                    case = firstword.tag.case
                    # для поиска слова в списке геогр.названием выбирапм форму Им.Падежа и пишем ей с заглавной буквы
                    checkword = firstword.normal_form.capitalize()
                    # проверяем, каким типом топонимов является слово
                    for t in self._geoxs["города"]:
                        if checkword == t:
                            newword = random.choice(self._geoxs["города"])
                    for t in self._geoxs["материки"]:
                        if checkword == t:
                            newword = random.choice(self._geoxs["материки"])
                    for t in self._geoxs["страны"]:
                        if checkword == t:
                            newword = random.choice(self._geoxs["страны"])
                    for t in self._geoxs["реки"]:
                        if checkword == t:
                            newword = random.choice(self._geoxs["реки"])
                    for t in self._geoxs["моря"]:
                        if checkword == t:
                            newword = random.choice(self._geoxs["моря"])
                    for t in self._geoxs["озёра"]:
                        if checkword == t:
                            newword = random.choice(self._geoxs["озёра"])
                    for t in self._geoxs["океаны"]:
                        if checkword == t:
                            newword = random.choice(self._geoxs["океаны"])
                    #если в словаре не нашлось такого географического названия, то мы его пропускаем
                    if newword==word:
                        continue
                    # загружаем новое слово в pymorphy, чтобы получить нужную форму
                    secondword = self._morph.parse(newword)[0]
                    # проверяем "совмеестимость" предлога
                    if text[text.index(word) - 1].lower() in ["в", "во"]:
                        case = 'loct'
                        reg = re.compile("^[В|Ф][^аоуэиыяеёю]")
                        result = re.match(reg, newword)
                        if result != None:
                            text[text.index(word) - 1] = text[text.index(word) - 1] + "о"
                        else:
                            text[text.index(word) - 1] = text[text.index(word) - 1][:1]
                        # выбираем нужную форму слова и меняем первую букву слова на заглавную
                    newword1 = secondword.inflect({case}).word.capitalize()
                    # заменяем старое слово на новое
                    n = text.index(word)
                    text[n] = newword1
        newtext = " ".join(text)
        return newtext
