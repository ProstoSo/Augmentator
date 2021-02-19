import pymorphy2

from augs.base_aug import BaseAug


# аугментация, в которой мы меняем местами два прилагательных, записанных через союз "и"
class AugChangeAdj(BaseAug):

    def __init__(self):
        self._morph = pymorphy2.MorphAnalyzer()

    def apply(self, text: str):
        # делим текст на отдельные слова
        text = text.split(" ")
        for ws in text:
            # ищем союз "и"
            if ws == "и":
                # запоминаем слово до союза и после
                word1 = text[text.index(ws) - 1]
                word2 = text[text.index(ws) + 1]
                s=""
                for symb in [",", ".", "!", "?"]:
                    if symb in word2:
                        word2 = word2.replace(symb, "")
                        s=symb
                firstword = self._morph.parse(word1)[0]
                secondword = self._morph.parse(word2)[0]
                # если слова - прилагательные, то меняем их местами
                if "ADJF" in firstword.tag and "ADJF" in secondword.tag:
                    text[text.index(ws) - 1] = word2.lower()
                    text[text.index(ws) + 1] = word1.lower()+s
        # уточняем, что предолжение начинается с заглавной буквы
        text[0] = text[0].capitalize()
        newtext = " ".join(text)
        return newtext
