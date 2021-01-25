from augs.base_aug import BaseAug
import random
import pymorphy2
import json
import re

class NERAug(BaseAug):

    def __init__(self):
        self._geoxs=json.load("augs/files/geox.json")
        self.morph=pymorphy2.MorphAnalyzer()

    def apply(self, text: str):
        text = text.split(" ")
        for word in text:
            # ищем слово с заглавной буквы
            if word.istitle() == True:
                # проверяем, является найденное слово географическим названием
                firstword = self.morph.parse(word)[0]
                if "Geox" in firstword.tag:
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
                    # загружаем новое слово в pymorphy, чтобы получить нужную форму
                    secondword = self.morph.parse(newword)[0]
                    # проверяем "совмеестимость" предлога
                    if text[text.index(word) - 1].lower() in ["в", "во"] :
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
        return f'{newtext}_augmented'
