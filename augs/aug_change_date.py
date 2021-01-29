import re
import random

import pymorphy2

from augs.base_aug import BaseAug


#аугментация в которой меняем месяц, год или дату в формате дд мм гггг
class AugChangeDate(BaseAug):

    def __init__(self):
        self._morph=pymorphy2.MorphAnalyzer()
        self._months=["январь", "февраль","март","апрель","май","июнь","июль","август","сентябрь","октябрь","ноябрь","декабрь"]
        self._date = re.compile('\d{2}(.|-|/)\d{2}(.|-|/)\d{4}')
        self._year=re.compile("\d{4}")

    def apply(self, text: str):
        txt = text.split(" ")
        for el in txt:
            if el.endswith(",") or el.endswith("."):
                elem = el[:-1]
            else:
                elem = el
                # заменяем только год
            if re.match(self._year, elem) != None:
                y = random.randint(1600, 2022)
                text = text.replace(elem, str(y))
            # заменяем дату в формате дд.мм.гггг дд/мм/гггг дд-мм-гггг
            if re.match(self._date, elem) != None:
                if "." in elem:
                    p = "."
                elif "-" in elem:
                    p = "-"
                elif "/" in elem:
                    p = "/"
                else:
                    p=" "
                y = random.randint(1600, 2022)
                m = random.randint(1, 12)
                if m in [1, 3, 5, 7, 8, 10, 12]:
                    day = random.randint(1, 31)
                elif m in [4, 6, 9, 11]:
                    day = random.randint(1, 30)
                elif m == 2:
                    day = random.randint(1, 28)
                else:
                    day=0
                #для одинарных чисел приписываем 0
                # 1.1.2020 -> 01.01.2020
                if len(str(m)) == 1:
                    m = "0" + str(m)
                if len(str(day)) == 1:
                    day = "0" + str(day)
                newdate = str(day) + p + str(m) + p + str(y)
                text = text.replace(elem, newdate)
                # заменяем месяц
            element=self._morph.parse(elem)[0]
            elemnomn = element.normal_form
            case = element.tag.case
            if elemnomn in self._months:
                newmonth_0 = random.choice(self._months)
                newmonth = self._morph.parse(newmonth_0)[0].inflect({case}).word
                text = text.replace(elem, newmonth)
        return text


#аугментация, которая меняет время в формате чч:мм
class AugChangeTime(BaseAug):

    def __init__(self):
        self._time=re.compile("(([0,1][0-9])|(2[0-3])):[0-5][0-9]")

    def apply(self, text: str):
        txt = text.split(" ")
        for el in txt:
            if el.endswith(",") or el.endswith("."):
                elem = el[:-1]
            else:
                elem = el
            if re.match(self._time, elem) != None:
                hour=random.randint(0,24)
                minute=random.randint(0,59)
                if len(str(hour))==1:
                    hour="0"+str(hour)
                if len(str(minute))==1:
                    minute="0"+str(minute)
                newtime=str(hour)+":"+str(minute)
                text=text.replace(elem,newtime)
        return text
