import random

import pymorphy2

from augs.base_aug import BaseAug


#аугментация, которая заменяет число с сохранением количества цифр в числе
class AugChangeNumber(BaseAug):

    def __init__(self):
        self._morph = pymorphy2.MorphAnalyzer()

    def apply(self, text: str):
        txt = text.split(" ")
        for el in txt:
            s = ""
            for symb in [",", ".", "!", "?"]:
                if symb in el:
                    el = el.replace(symb, "")
                    s = symb
            if el.isdigit():
                c = len(el) - 1
                if c == 0:
                    a = 0
                else:
                    a = int("1" + "0" * c)
                b = int("9" + "9" * c)
                n = random.randint(a, b)
                wordind= txt.index(el+s)
                if wordind+1 >= len(txt):
                    word = txt[wordind - 1]
                else:
                    word = txt[wordind + 1]
                s2=""
                for symb in [",", ".", "!", "?"]:
                    if symb in word:
                        word = word.replace(symb, "")
                        s2 = symb
                # процесс согласования
                word_0 = self._morph.parse(word)[0]
                ww = word_0.normal_form
                word_0 = self._morph.parse(ww)[0]
                if str(n).endswith("11") or str(n).endswith("12")  or str(n).endswith("13")  or str(n).endswith("14") :
                    w = word_0.inflect({'plur'})
                    w = w.inflect({'gent'})
                    new_form = w.word
                else:
                    if n % 10 == 1:
                        w = word_0.inflect({'nomn'})
                        new_form = w.word
                    elif n % 10 == 2 or n % 10 == 3 or n % 10 == 4:
                        w = word_0.inflect({'gent'})
                        new_form = w.word
                    else:
                        w = word_0.inflect({'plur'})
                        w = w.inflect({'gent'})
                        new_form = w.word
                txt[txt.index(el+s)] = str(n)
                txt[txt.index(word+s2)] = new_form+s2
        text = " ".join(txt)
        return text


#аугментация, которая заменяет число, позволяя определить диапазон для замены
class AugChangeNumber2(BaseAug):

    def __init__(self):
        self._morph = pymorphy2.MorphAnalyzer()

##вижу, что у базовой аугментации нет места для аргументов a и b, но не знаю, как решить эту проблему
    def apply(self, text: str,a:int=None, b:int=None):
        txt = text.split(" ")
        for el in txt:
            s1 = ""
            for symb in [",", ".", "!", "?"]:
                if symb in el:
                    el = el.replace(symb, "")
                    s1 = symb
            if el.isdigit():
                s2=""
                n = random.randint(a, b)
                wordind = txt.index(el + s1)
                if wordind + 1 >= len(txt):
                    word = txt[wordind - 1]
                else:
                    word = txt[wordind + 1]
                for symb in [",", ".", "!", "?"]:
                    if symb in word:
                        word = word.replace(symb, "")
                        s2 = symb
                # процесс согласования
                word_0 = self._morph.parse(word)[0]
                ww = word_0.normal_form
                word_0 = self._morph.parse(ww)[0]
                if str(n).endswith("11") or str(n).endswith("12")  or str(n).endswith("13")  or str(n).endswith("14") :
                    w = word_0.inflect({'plur'})
                    w = w.inflect({'gent'})
                    new_form = w.word
                else:
                    if n % 10 == 1:
                        w = word_0.inflect({'nomn'})
                        new_form = w.word
                    elif n % 10 == 2 or n % 10 == 3 or n % 10 == 4:
                        w = word_0.inflect({'gent'})
                        new_form = w.word
                    else:
                        w = word_0.inflect({'plur'})
                        w = w.inflect({'gent'})
                        new_form = w.word
                txt[txt.index(el+s1)] = str(n)
                txt[txt.index(word+s2)] = new_form+s2
        text = " ".join(txt)
        return text
