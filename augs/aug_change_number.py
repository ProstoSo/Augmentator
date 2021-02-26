import random

import pymorphy2

from augs.base_aug import BaseAug
from augs.utils import remove_punctuation_with_sign


class AugChangeNumber(BaseAug):
    """ Аугментация, которая заменяет число с сохранением количества цифр в числе """

    def __init__(self):
        self._morph = pymorphy2.MorphAnalyzer()

    def apply(self, text: str):
        tokens = text.split(' ')
        for i, token in enumerate(tokens):
            token, s = remove_punctuation_with_sign(token)
            if token.isdigit():
                c = len(token) - 1
                if c == 0:
                    a = 0
                else:
                    a = int('1' + '0' * c)
                b = int('9' + '9' * c)
                n = random.randint(a, b)
                if i + 1 >= len(tokens):
                    word = tokens[i - 1]
                    word_id = i - 1
                else:
                    word = tokens[i + 1]
                    word_id = i + 1
                word, s2 = remove_punctuation_with_sign(word)
                # процесс согласования
                word_0 = self._morph.parse(word)[0]
                ww = word_0.normal_form
                word_0 = self._morph.parse(ww)[0]
                if str(n).endswith('11') or str(n).endswith('12') or str(n).endswith('13') or str(n).endswith('14'):
                    w = word_0.inflect({'plur'})
                    w = w.inflect({'gent'})
                    new_form = w.word
                else:
                    if n % 10 == 1:
                        w = word_0.inflect({'nomn'})
                        new_form = w.word
                    elif n % 10 in {2, 3, 4}:
                        w = word_0.inflect({'gent'})
                        new_form = w.word
                    else:
                        w = word_0.inflect({'plur'})
                        w = w.inflect({'gent'})
                        new_form = w.word
                tokens[i] = str(n)
                tokens[word_id] = new_form + s2
        text = ' '.join(tokens)
        return text


class AugChangeNumberWithRange(BaseAug):
    """ Аугментация, которая заменяет число, позволяя определить диапазон для замены """

    def __init__(self):
        self._morph = pymorphy2.MorphAnalyzer()

    def apply(self, text: str, a: int=None, b: int=None) -> str:
        tokens = text.split(' ')
        for i, token in enumerate(tokens):
            token, s1 = remove_punctuation_with_sign(token)
            if token.isdigit():
                s2 = ''
                n = random.randint(a, b)
                if i + 1 >= len(tokens):
                    word = tokens[i - 1]
                    word_id = i - 1
                else:
                    word = tokens[i + 1]
                    word_id = i + 1
                word, s2 = remove_punctuation_with_sign(word)
                # процесс согласования
                word_0 = self._morph.parse(word)[0]
                ww = word_0.normal_form
                word_0 = self._morph.parse(ww)[0]
                if str(n).endswith('11') or str(n).endswith('12') or str(n).endswith('13') or str(n).endswith('14'):
                    w = word_0.inflect({'plur'})
                    w = w.inflect({'gent'})
                    new_form = w.word
                else:
                    if n % 10 == 1:
                        w = word_0.inflect({'nomn'})
                        new_form = w.word
                    elif n % 10 in {2, 3, 4}:
                        w = word_0.inflect({'gent'})
                        new_form = w.word
                    else:
                        w = word_0.inflect({'plur'})
                        w = w.inflect({'gent'})
                        new_form = w.word
                tokens[i] = str(n)
                tokens[word_id] = new_form + s2
        text = ' '.join(tokens)
        return text
