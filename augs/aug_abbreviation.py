import os
import json
from typing import List

import pymorphy2
import pyonmttok

from augs.base_aug import BaseAug
from augs.paths import FILES_PATH
from augs.utils import remove_punctuation, remove_punctuation_with_sign, remove_whitespace


class AugOpenAbbr(BaseAug):
    """ Раскрытие аббревиатур в тексте: 'Я учусь в НГУ' -> 'Я учусь в Новосибирском государственном университете' """

    def __init__(self):
        with open(os.path.join(FILES_PATH, 'abbreviations.json'), 'r', encoding='utf-8') as abbs:
            self._abbs = json.load(abbs)
        self._morph = pymorphy2.MorphAnalyzer()
        self._tokenizer = pyonmttok.Tokenizer('aggressive')

    def apply(self, text: str) -> str:
        tokens = self._tokenizer.tokenize(text)[0]
        tokens=text.split(" ")
        for token in tokens:
            # если есть знак препинания, то убираем его из слова с которым будем работать
            oldword = token
            s = ''
            token, s = remove_punctuation_with_sign(token)
            # ищем аббревиатуру в тексте
            if token in self._abbs:
                newwords = self._abbs[token]
                # проверяем корректность падежа
                oldword_index = tokens.index(oldword)
                prword = tokens[oldword_index - 1].lower()
                # если предыдущее слово это союз, то нужно посмотреть, что было перед союзом
                if prword in {'и', 'или'}:
                    prword = tokens[oldword_index - 2]
                    # если перед союзом ещё одна аббревиатура (расшифрованная в ходе программы или нет), то
                    # выбираем падеж исходя из того, что стоит перед аббревиатурой
                    if prword.isupper() or ' ' in prword:
                        prword = tokens[oldword_index - 3].lower()
                prword_case = self._check_case(prword)
                newwordss = newwords.split(" ")
                newwlst = []
                # склоняем слова
                for w in newwordss:
                    ww = self._morph.parse(w)[0]
                    if ww.tag.case == 'nomn':
                        newword = ww.inflect({prword_case}).word
                    else:
                        newword = w
                    if w.istitle():
                        newwlst.append(newword.capitalize())
                    else:
                        newwlst.append(newword)
                newword1 = " ".join(newwlst)
                tokens[oldword_index] = newword1+s
        newtext = " ".join(tokens)
        newtext = remove_whitespace(newtext)
        return newtext

    def _check_case(self, word: str) -> str:
        case = 'nomn'
        if word in {'в', 'о'}:
            case = 'loct'
        elif word in {'за', 'над', 'под'}:
            case = 'ablt'
        elif word in {'от', 'из', 'до', 'около'} or self._morph.parse(word)[0].tag.POS == 'NOUN':
            case = 'gent'
        return case


class AugCloseAbbr(BaseAug):
    """ Схлопывание аббревиатур: 'Я учусь в Новосибирском государственном университете' -> 'Я учусь в НГУ' """

    def __init__(self):
        with open(os.path.join(FILES_PATH, 'abbreviations.json'), 'r', encoding='utf-8') as abbs:
            abbs0 = json.load(abbs)
            self._abbs = dict(zip(abbs0.values(), abbs0.keys()))
        with open(os.path.join(FILES_PATH, 'normalized_abbrs.json'), 'r', encoding='utf-8') as norm_abbrs:
            self._normalized_abbrs = json.load(norm_abbrs)
        self._morph = pymorphy2.MorphAnalyzer()
        self._tokenizer = pyonmttok.Tokenizer('aggressive')

    def apply(self, text: str) -> str:
        tokens = self._tokenizer.tokenize(text)[0]
        # создаем предложение, в котором все слова в стандартной форме, для того, чтобы позже найти расшифрованную
        # аббревиатуру
        normalized_tokens = self._normalize_text(tokens)
        normalized_text = " ".join(normalized_tokens)
        # идем по файлу с аббревиатурами, ищем расшифровку в тексте и подходящую аббревиатуру
        for normalized_abbr in self._normalized_abbrs:
            if normalized_abbr in normalized_text:
                el = self._normalized_abbrs[normalized_abbr]
                abb0 = el
                # запоминаем аббревиатуру
                newword = self._abbs[el]
                # создаем список слов аббревиатуры
                l1 = abb0.split(' ')
                l2 = []
                # ищем в исходном тексте слова, которые являются расшифровкой аббревиатуры
                for els in l1:
                    # при расшифровке аббревиатур с предложением согласуются только те слова, которые стоят в
                    # именительном падеже,
                    # если же в расшифровке присутсвуют слова в косвенном падеже, то они не меняют падеж внутри
                    # предложения
                    checking = self._morph.parse(els)[0]
                    for words in tokens:
                        words = remove_punctuation(words)
                        firstword = self._morph.parse(words)[0]
                        if checking.tag.case == 'nomn':
                            checkword = firstword.normal_form
                        else:
                            checkword = firstword.word
                        # добавляем слова из расшифровки в отдельный список
                        if checkword == els.lower():
                            l2.append(words)
                            break
                # объединяем список, чтобы получить шаблон для замены
                r = ' '.join(l2)
                print(r)
                # заменяем расшифровку на аббревиатуру
                text = text.replace(r, newword)
        return text

    def _normalize_text(self, text: List[str]) -> List[str]:
        workinglst = []
        for word in text:
            word = remove_punctuation(word)
            firstword = self._morph.parse(word)[0]
            checkword = firstword.normal_form
            workinglst.append(checkword)
        return workinglst
