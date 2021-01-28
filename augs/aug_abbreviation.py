import json

import pymorphy2

from augs.base_aug import BaseAug


class AugOpenAbbr(BaseAug):

    def __init__(self):
        with open("augs/files/abbreviations.json") as abbs:
            self._abbs=json.load(abbs)
        self._morph=pymorphy2.MorphAnalyzer()
        
        def check_case(self, word):
            case="nomn"
            f word in ["в", "о"]:
                    case = 'loct'
            elif word in ["за", "над", "под"]:
                    case = 'ablt'
            elif word in ["от", "из", "до", "около"] or self._morph.parse(word)[0].tag.POS=="NOUN" :
                    case = 'gent
            return(case)
        
    def apply(self, text: str):        
        text = text.split(" ")
        for word in text:
            newwords = ""
            #если есть знак препинания, то убираем его из слова с которым будем работать
            oldword=word
            for els in [",",".","!","?"]:
              if els in word:
                word=word.replace(els,"")
            # ищем аббревиатуру в тексте
            if word.isupper() and len(word) > 1:
                firstword = self._morph.parse(word)[0]
                for el in self._abbs:
                    # ищем аббревиатуру в словаре
                    if el == word:
                        newwords = self._abbs[word]
               if newwords == "":
                    continue
                # проверяем корректность падежа
                prword= text[text.index(oldword) - 1].lower()
                #если предыдущее слово это союз, то нужно посмотреть, что было перед союзом
                if prword=="и":
                    prword =text[text.index(oldword) - 2]
                    #если перед союзом ещё одна аббревиатура (расшифрованная в ходе программы или нет), то 
                    #выбираем падеж исходя из того, что стоит перед аббревиатурой
                    if prword.isupper() or " " in prword2:
                        prword=text[text.index(oldword) - 3].lower()                 
                self.check_case(prword)
                newwordss = newwords.split(" ")
                newwlst = []
                # склоняем слова
                for w in newwordss:
                    ww = self._morph.parse(w)[0]
                    if ww.tag.case == "nomn":
                        newword = ww.inflect({case}).word
                    else:
                        newword = w
                    if w.istitle() == True:
                        newwlst.append(newword.capitalize())
                    else:
                        newwlst.append(newword)
                newword1=" ".join(newwlst)
                n =text.index(oldword)
                text[n] = text[n].replace(word,newword1)
        newtext = " ".join(text)
        return newtext

    
class Aug_close_abbr(BaseAug):
    def __init__(self):
        with open("augs/files/abbreviations.json") as abbs:
            abbs0=json.load(abbs)
            self._abbs=dict(zip(abbs0.values(), abbs0.keys()))
        self._morph=pymorphy2.MorphAnalyzer()

    def apply(self, text: str):
        txt = text.split(" ")
        # создаем предложение, в котором все слова в стандартной форме, для того, чтобы позже найти расшифрованную аббревиатуру
        workinglst = []
        for word in txt:
            newword = ""
            for els in [",",".","!","?"]:
                if els in kword:
                word=word.replace(els,"")
            firstword = self._morph.parse(word)[0]            
            checkword = firstword.normal_form
            workinglst.append(checkword)
        worktext = " ".join(workinglst)
        # идем по файлу с аббревиатурами, ищем расшифровку в тексте и подходящую аббревиатуру
        for el in self._abbs:
            abbr = el.split(" ")
            abslst = []
            #создаем список где все слова аббревиатуры в стандартной форме
            for word in abbr:
              firstword = morph.parse(word)[0]
              checkword = firstword.normal_form
              abslst.append(checkword)       
            workabbr = " ".join(abslst)
            #ищем расшифровку в тексте
            if workabbr in worktext:
                abb0 = el
                # запоминаем аббревиатуру
                newword = self._abbs[el]
                #создаем список слов аббревиатуры
                l1 = abb0.split(" ")
                l2 = []
                # ищем в исходном тексте слова, которые являются расшифровкой аббревиатуры
                for els in l1:
                    #при расшифровке аббревиатур с предложением согласуются только те слова, которые стоят в именительном падеже,  
                     #если же в расшифровке присутсвуют слова в косвенном падеже, то они не меняют падеж внутри предложения
                    checking = self._morph.parse(els)[0]
                    for words in txt:
                        if checking.tag.case == "nomn":
                            firstword = self._morph.parse(words)[0]
                            checkword = firstword.normal_form
                        else:
                            firstword = self._morph.parse(words)[0]
                            checkword = firstword.word
                        # добавляем слова из расшифровки в отдельный список
                        if checkword == els.lower():
                            l2.append(words)
            # объединяем список, чтобы получить шаблон для замены
            r = " ".join(l2)
            # заменяем расшифровку на аббревиатуру
            text = text.replace(r, newword)
        return text
