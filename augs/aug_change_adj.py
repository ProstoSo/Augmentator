from augs.base_aug import BaseAug
import pymorphy2

class Aug_change_adj(BaseAug):

    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()

    def apply(self, text: str):
        text = text.split(" ")
        for ws in text:
            if ws == "и":
                word1 = text[text.index(ws) - 1]
                word2 = text[text.index(ws) + 1]

                firstword = self.morph.parse(word1)[0]
                secondword = self.morph.parse(word2)[0]
                if "ADJF" in firstword.tag and "ADJF" in secondword.tag:
                    text[text.index(ws) - 1] = word2.lower()
                    text[text.index(ws) + 1] = word1.lower()
        text[0] = text[0].capitalize()
        newtext = " ".join(text)
        return newtext
