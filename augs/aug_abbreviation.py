from augs.base_aug import BaseAug
import pymorphy2
import json

class open_abbr(BaseAug):

    def __init__(self):
        self._geo_names = set()
        self.abbs=json.load(open("augs/files/abbreviations.json"))
        self.morph=pymorphy2.MorphAnalyzer()
    def apply(self, text: str):
        newwords = ""
        text = text.split(" ")
        for word in text:
            # ищем аббревиатуру в тексте
            if word.isupper() == True and len(word) > 1:
                firstword = self.morph.parse(word)[0]
                # запоминаем падеж аббревиатуры (хотя у аббревиатур нет падежей...)
                case = firstword.tag.case
                for el in self.abbs["abb"][0]:
                    # ищем аббревиатуру в словаре
                    if el == word:
                        # print (abbs["abb"][0][word])
                        newwords = self.abbs["abb"][0][word]
                if newwords == "":
                    return ("Аббревиатура не найдена")
                # проверяем корректность падежа

                if text[text.index(word) - 1].lower() in ["в", "о"]:
                    case = 'loct'
                if text[text.index(word) - 1].lower() in ["за", "над", "под"]:
                    case = 'ablt'
                if text[text.index(word) - 1].lower() in ["от", "из", "до", "около"] or self.morph.parse(text[text.index(word)- 1])[0].tag.POS=="NOUN" :
                    case = 'gent'
                newwordss = newwords.split(" ")
                newwlst = []
                # склоняем слова
                for w in newwordss:
                    ww = self.morph.parse(w)[0]
                    if ww.tag.case == "nomn":
                        newword = ww.inflect({case}).word
                    else:
                        newword = w
                    if w.istitle() == True:
                        newwlst.append(newword.capitalize())
                    else:
                        newwlst.append(newword)
                newword1 = " ".join(newwlst)
                n = text.index(word)
                text[n] = newword1
        newtext = " ".join(text)
        return (newtext)

class close_abbr(BaseAug):
    def __init__(self):
        self._geo_names = set()
        self.abbs=json.load(open("/content/абб.json"))
        self.morph=pymorphy2.MorphAnalyzer()

    def apply(self, text: str):
        newword = ""
        txt = text.split(" ")
        # создаем предложение, в котором все слова в именительном падеже и с большой буквы, для того, чтобы позже найти расшифрованную аббревиатуру
        workinglst = []
        for word in txt:
            firstword = self.morph.parse(word)[0]
            checkword = firstword.normal_form.capitalize()
            workinglst.append(checkword)
        worktext = " ".join(workinglst)
        # идем по файлу с аббревиатурами, ищем расшифровку в тексте и подходящую аббревиатуру
        for el in self.abbs["abb"][0]:
            abbr = self.abbs["abb"][0][el].split(" ")
            abslst = []
            for word in abbr:
                firstword = self.morph.parse(word)[0]
                checkword = firstword.normal_form.capitalize()
                abslst.append(checkword)
            workabbr = " ".join(abslst)
            if workabbr in worktext:
                abb0 = self.abbs["abb"][0][el]
                # запоминаем аббревиатуру
                newword = el
        if newword == "":
            return ("Аббревиатура не найдена")
        l1 = abb0.split(" ")
        l2 = []
        # производим замену в исходном тексте
        for els in l1:
            checking = self.morph.parse(els)[0]
            for words in txt:
                if checking.tag.case == "nomn":
                    firstword = self.morph.parse(words)[0]
                    checkword = firstword.normal_form
                else:
                    firstword = self.morph.parse(words)[0]
                    checkword = firstword.word
                # добавляем слова из расшифровки в отдельный список
                if checkword == els.lower():
                    l2.append(words)
        # объединяем список, чтобы получить шаблон для замены
        r = " ".join(l2)
        # заменяем расшифровку на аббревиатуру
        newtext = text.replace(r, newword)
        return (newtext)
