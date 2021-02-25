import pymorphy2
import pyonmttok

from augs.base_aug import BaseAug
from augs.utils import remove_whitespace


class AugChangeAdj(BaseAug):
    """ Аугментация, в которой меняются местами два прилагательных, записанных через союз 'и' """

    def __init__(self):
        self._morph = pymorphy2.MorphAnalyzer()
        self._tokenizer = pyonmttok.Tokenizer('aggressive')

    def apply(self, text: str):
        # делим текст на отдельные слова
        tokens = self._tokenizer.tokenize(text)[0]
        for i, token in enumerate(tokens):
            # ищем союз "и"
            if token == 'и':
                # запоминаем слово до союза и после
                word1 = tokens[i - 1]
                word2 = tokens[i + 1]
                s = ''
                for symb in [',', '.', '!', '?']:
                    if symb in word2:
                        word2 = word2.replace(symb, '')
                        s=symb
                firstword = self._morph.parse(word1)[0]
                secondword = self._morph.parse(word2)[0]
                # если слова - прилагательные, то меняем их местами
                if 'ADJF' in firstword.tag and 'ADJF' in secondword.tag:
                    tokens[i - 1] = word2.lower()
                    tokens[i + 1] = word1.lower() + s
        # уточняем, что предолжение начинается с заглавной буквы
        tokens[0] = tokens[0].capitalize()
        newtext = " ".join(tokens)
        newtext = remove_whitespace(newtext)
        return newtext
