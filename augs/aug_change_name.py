import os
import random

import pymorphy2

from augs.base_aug import BaseAug
from augs.paths import FILES_PATH
from augs.utils import remove_punctuation_with_sign


class AugChangeName(BaseAug):
    """
    Аугментация, которая изменяет мужские имена на мужские, женские на женские, а имена неодназначно определяющие пол на
    имена такого типа
    """

    def __init__(self):
        with open(os.path.join(FILES_PATH, 'names.txt'), 'r', encoding='utf-8') as names:
            self._names_lst = names.read().split(' ')
        with open(os.path.join(FILES_PATH, 'femnames.txt'), 'r', encoding='utf-8') as fnames:
            self._fems_names_lst = fnames.read().split(' ')
        with open(os.path.join(FILES_PATH, 'mascnames.txt'), 'r', encoding='utf-8') as mnames:
            self._masc_names_lst = mnames.read().split(' ')
        self._morph=pymorphy2.MorphAnalyzer()

    def apply(self, text: str) -> str:
        tokens = text.split(" ")
        for i, token in enumerate(tokens):
            token, s = remove_punctuation_with_sign(token)
            firstword = self._morph.parse(token)[0]
            case = firstword.tag.case
            if 'Name' in firstword.tag:
                newname = token
                if 'ms-f' in firstword.tag:
                    newname = random.choice(self._names_lst)
                if 'femn' in firstword.tag:
                    newname = random.choice(self._fems_names_lst)
                elif 'masc' in firstword.tag:
                    newname = random.choice(self._masc_names_lst)
                newname2 = self._morph.parse(newname)[0]

                # выбираем нужную форму слова и меняем первую букву слова на заглавную
                newname3 = newname2.inflect({case}).word.capitalize() + s
                tokens[i] = newname3
        newtext = ' '.join(tokens)
        return newtext
