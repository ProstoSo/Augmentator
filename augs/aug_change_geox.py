import json
import random
import re

import pymorphy2

from augs.base_aug import BaseAug


#аугментация, которая заменяет одни географические названия другими, сохраняя тип топонима
class AugChangeGeox(BaseAug):

    def __init__(self):
        with open("files/geox.json",'r',encoding='utf-8') as geoxs:
            self._geoxs=json.load(geoxs)
        self._morph=pymorphy2.MorphAnalyzer()

    def apply(self, text: str):
        text = text.split(" ")
        for word in text:
            # ищем слово с заглавной буквы
            if word.istitle():
                # проверяем, является найденное слово географическим названием
                firstword = self._morph.parse(word)[0]
                if "Geox" in firstword.tag:
                    newword = word
                    # запоминаем исходный падеж
                    case = firstword.tag.case
                    # для поиска слова в списке геогр.названием выбирапм форму Им.Падежа и пишем ей с заглавной буквы
                    checkword = firstword.normal_form.capitalize()
                    # проверяем, каким типом топонимов является слово
                    for geo_type, names in self._geoxs.items():
                        if checkword in names:
                            newword = random.choice(names)
                            break
                    #если в словаре не нашлось такого географического названия, то мы его пропускаем
                    if newword == word:
                        continue
                    # загружаем новое слово в pymorphy, чтобы получить нужную форму
                    secondword = self._morph.parse(newword)[0]
                    # проверяем "совмеестимость" предлога
                    if text[text.index(word) - 1].lower() in ["в", "во"]:
                        case = 'loct'
                        reg = re.compile("^[В|Ф][^аоуэиыяеёю]")
                        result = re.match(reg, newword)
                        prword = text[text.index(word) - 1]
                        if result != None:
                            prword = prword + "о"
                        else:
                            prword = prword[:1]
                        text[text.index(word) - 1] = prword
                        # выбираем нужную форму слова и меняем первую букву слова на заглавную
                    newword1 = secondword.inflect({case}).word.capitalize()
                    # заменяем старое слово на новое
                    n = text.index(word)
                    text[n] = newword1
        newtext = " ".join(text)
        return newtext
