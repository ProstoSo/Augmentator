import re
import os
import json
import random

import pymorphy2

from augs.base_aug import BaseAug
from augs.paths import FILES_PATH
from augs.utils import remove_whitespace, remove_punctuation_with_sign, remove_quote


class AugChangeGeox(BaseAug):
    """ Аугментация, которая заменяет одни географические названия другими, сохраняя тип топонима """

    def __init__(self):
        with open(os.path.join(FILES_PATH, 'geox.json'), 'r', encoding='utf-8') as geoxs:
            self._geoxs = json.load(geoxs)
        self._morph = pymorphy2.MorphAnalyzer()

    def apply(self, text: str) -> str:
        tokens = text.split(' ')
        for token in tokens:
            s_starts = ''
            s_ends = ''
            s = ''
            token, s = remove_punctuation_with_sign(token)
            token,s_starts, s_ends=remove_quote(token)
            # ищем слово с заглавной буквы
            if token.istitle():
                # проверяем, является найденное слово географическим названием
                firstword = self._morph.parse(token)[0]
                if 'Geox' in firstword.tag:
                    newword = token
                    # запоминаем исходный падеж
                    case = firstword.tag.case
                    # для поиска слова в списке геогр.названием выбирапм форму Им.Падежа и пишем ей с заглавной буквы
                    checkword = firstword.normal_form.capitalize()
                    # проверяем, каким типом топонимов является слово
                    for geo_type, names in self._geoxs.items():
                        if checkword in names:
                            newword = random.choice(names)
                            break
                    # если в словаре не нашлось такого географического названия, то мы его пропускаем
                    if newword == token:
                        continue
                    # загружаем новое слово в pymorphy, чтобы получить нужную форму
                    secondword = self._morph.parse(newword)[0]
                    # проверяем "совместимость" предлога
                    previous_token_index = tokens.index(s_starts+token+s_ends + s)
                    if tokens[previous_token_index - 1].lower() in ['в', 'во']:
                        case = 'loct'
                        reg = re.compile("^[В|Ф][^аоуэиыяеёю]")
                        result = re.match(reg, newword)
                        prword = tokens[previous_token_index - 1]
                        if result != None:
                            prword = prword + 'о'
                        else:
                            prword = prword[:1]
                        tokens[previous_token_index - 1] = prword
                        # выбираем нужную форму слова и меняем первую букву слова на заглавную
                    newword1 = s_starts + secondword.inflect({case}).word.capitalize() + s_ends + s
                    # заменяем старое слово на новое
                    n = previous_token_index
                    tokens[n] = newword1
        newtext = ' '.join(tokens)
        newtext = remove_whitespace(newtext)
        return newtext
