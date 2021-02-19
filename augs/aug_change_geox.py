import json
import random
import re
import os

import pymorphy2

from .base_aug import BaseAug
from .paths import FILES_PATH


#аугментация, которая заменяет одни географические названия другими, сохраняя тип топонима
class AugChangeGeox(BaseAug):

    def __init__(self):
        with open (os.path.join(FILES_PATH, 'geox.json'),'r',encoding='utf-8') as geoxs:
            self._geoxs=json.load(geoxs)
        self._morph=pymorphy2.MorphAnalyzer()

    def apply(self, text: str):
        text = text.split(" ")
        for word in text:
            s=""
            # ищем слово с заглавной буквы
            if word.istitle():
                for symb in [",", ".", "!", "?"]:
                    if symb in word:
                        word = word.replace(symb, "")
                        s=symb
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
                    if text[text.index(word+s) - 1].lower() in ["в", "во"]:
                        case = 'loct'
                        reg = re.compile("^[В|Ф][^аоуэиыяеёю]")
                        result = re.match(reg, newword)
                        prword = text[text.index(word+s) - 1]
                        if result != None:
                            prword = prword + "о"
                        else:
                            prword = prword[:1]
                        text[text.index(word+s) - 1] = prword
                        # выбираем нужную форму слова и меняем первую букву слова на заглавную
                    newword1 = secondword.inflect({case}).word.capitalize()+s
                    # заменяем старое слово на новое
                    n = text.index(word+s)
                    text[n] = newword1
        newtext = " ".join(text)
        return newtext
