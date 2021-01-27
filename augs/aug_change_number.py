from augs.base_aug import BaseAug
import random
import pymorphy2

class Aug_change_number(BaseAug):
    # замена с сохранением количества цифр в числе
    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()

    def apply(self, text: str):
        txt = text.split(" ")
        for el in txt:
            if el.isdigit():
                c = len(el) - 1
                a = int("1" * c + "0")
                b = int("9" * c + "9")
                n = random.randint(a, b)
                word = txt[txt.index(el) + 1]
                # процесс согласования
                word_0 = self.morph.parse(word)[0]
                ww = word_0.normal_form
                word_0 = self.morph.parse(ww)[0]
                if n == 11 or n == 12 or n == 13 or n == 14:
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
                txt[txt.index(el)] = str(n)
                txt[txt.index(word)] = new_form
        text = " ".join(txt)
        return(text)

class Aug_change_number_2(BaseAug):
    # замена с выбором диапазона
    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()

    def apply(self, text: str,a:int, b:int):
        txt = text.split(" ")
        for el in txt:
            if el.isdigit():
                n = random.randint(a, b)
                word = txt[txt.index(el) + 1]
                # процесс согласования
                word_0 = self.morph.parse(word)[0]
                ww = word_0.normal_form
                word_0 = self.morph.parse(ww)[0]
                if n == 11 or n == 12 or n == 13 or n == 14:
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
                txt[txt.index(el)] = str(n)
                txt[txt.index(word)] = new_form
        text = " ".join(txt)
        return(text)

