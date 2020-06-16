# -*- coding: utf-8 -*-
# Загружаем корпус и делим его на предложения

f = open("ru_syntagrus-ud-train.conllu.txt", "r")
fn = f.read()
fnn = fn.split("\n\n")

for el in fnn:
    if el == "":
        fnn.remove(el)
    # удаляем пустые строки из корпуса, чтобы не было ошибок


# создаём класс токенов, экземплярами которого будут токены из предложений
class Token0():
    def __init__(self):
        self.token_id = ""  # номер слова в предложении
        self.form = ""  # форма слова
        self.lemma = ""  # лемма слова
        self.upos = ""  # часть речи
        self.xpos = ""  # дополнительные характеристики части речи
        self.feats = ""  # грамматические характеристики
        self.featslst = ["", "", "", "",
                         ""]  # список грамматических характеристик слова, создающийся функцией createfeats()
        self.head = ""  # главное слово
        self.deprel = ""  # отношение зависимости
        self.deps = ""  # граф зависимости
        self.misc = ""  # примечания (например отсутствие пробела после слова указывается здесь)

    # функция, создающая список, содержащий все теги слова
    def create(self, l):
        l = l.split("\t")
        self.token_id = l[0]
        self.form = l[1]
        self.lemma = l[2]
        self.upos = l[3]
        self.xpos = l[4]
        self.feats = l[5]
        self.head = l[6]
        self.deprel = l[7]
        self.deps = l[8]
        self.misc = l[9]
        self._createfeats()

    # функция, создающая список морфологических и грамматических характеристик
    def _createfeats(self):
        f = self.feats.split("|")
        for elem in f:
            if "Animacy" in elem:
                self.featslst[0] = elem
            if "Case" in elem:
                self.featslst[1] = elem
            if "Gender" in elem:
                self.featslst[2] = elem
            if "Number" in elem:
                self.featslst[3] = elem
            if "Person" in elem:
                self.featslst[4] = elem


# Класс предложений, экземплярами которого будут обработанные предложения из корпуса
class Sentence():
    def __init__(self):
        self.text = ""  # текст предложения
        self.sent_id = ""  # номер предложения в корпусе
        self.tokens = []  # список токенов предложения, состоящий из экземпляров класса Token

    # функция обработки предложения. Получает на вход предложение из корпуса, делит на составляющие
    def make_structure(self, sent):
        sent = sent.split("\n")
        for token in sent[0:2]:  # вычленяем номер и текст предложения
            token = token.split(" ")
        self.sent_id = sent[0].replace("# sent_id = ", "")  # id предложения
        self.text = sent[1].replace("# text = ", "")  # текст предложения
        for tok in sent[2:]:  # создаём токены
            token = Token0()
            token.create(tok)
            self.tokens.append(token)

    # функция обновления текста предложения. Создаёт новый текст на основе элементов списка self.tokens
    def make_text(self):
        text = ""
        for el in self.tokens:
            if el.misc == "SpaceAfter=No":
                text = text + el.form
            else:
                text = text + el.form + " "
        text = text[:-1]
        return text


# создаём экземпляры класса Sentence // нужно обновлять перед каждым применением аугментаций
corpus = []
for sentence in fnn:
    sent = Sentence()
    sent.make_structure(sentence)
    corpus.append(sent)
print(len(corpus))


# создаём класс базовой аугментации, которая содержит в себе все необходимые данные для реализации конкретных аугментаций
class BaseAugmentation:

    def __init__(self):
        self.results = []

    # функция, которая проверяет нумерацию токенов и правильное оформление предложения.
    def correct(self, sentence):
        num = 200
        era = 0
        # исправляем нумерацию токенов
        while era < 2:
            for elem in sentence.tokens:
                tok_id = elem.token_id
                if tok_id != str(num + 1):
                    for toks in sentence.tokens:
                        # ищем зависимые слова
                        head = toks.head
                        if head == tok_id:
                            # исправляем нумерацию
                            toks.head = str(num + 1)
                            deps = toks.deps
                            parts = deps.split(":")
                            if tok_id == parts[0]:
                                toks.deps = deps.replace(tok_id, str(num + 1))
                    # устанавливаем новый номер
                    elem.token_id = str(num + 1)
                num = num + 1
            num = 0
            era += 1
        # обеспечиваем написание первого слова в предложении с заглавной буквы.
        # (если предложение начинается, например, с тире, то с заглавной буквы будет написано второе слово)
        if sentence.tokens[0].upos != "PUNCT":
            sentence.tokens[0].form = sentence.tokens[0].form.capitalize()
        else:
            sentence.tokens[1].form = sentence.tokens[1].form.capitalize()
        return sentence


# Первая аугментация. Замена подлежащего-существительного на местоимение

class FirstAugmentation(BaseAugmentation):

    def __init__(self):
        self._pron_list = self._get_pronouns()

    # функция, обрабатывающая список местоимений.
    def _get_pronouns(self):
        pron_list = []
        pronouns0 = open("pronouns.txt", "r")
        pronouns = pronouns0.read()
        pronouns = pronouns.split("\n")
        for line in pronouns:
            line = line.replace("'", "")
            line = line.replace("[", "")
            line = line.replace("]", "")
            line = line.split(", ")
            if line != [""]:
                pron_list.append(line)
        return pron_list

    # алгоритм аугментации
    def run(self, s0):  # получаем на вход элемент класса Sentence
        import random
        for w in s0.tokens:
            if w != "None":  # если слово не пустое
                if w.upos == "NOUN" and w.deprel == "nsubj" or w.upos == "NOUN" and w.deprel == "nsubj:pass" and \
                        w.featslst[
                            1] == "Case=Nom" or w.upos == "PROPN" and w.deprel == "nsubj" or w.upos == "PROPN" and w.deprel == "nsubj:pass" and \
                        w.featslst[1] == "Case=Nom":  # ищем подлежащее
                    wf = w.feats  # получаем список грамматических характеристик
                    random.shuffle(self._pron_list)
                    for pron in self._pron_list:
                        feats = pron[5]
                        if w.featslst[3] in feats:
                            if w.featslst[0] in feats or w.featslst[0] == '' or "Animacy" not in feats:
                                if w.featslst[2] in feats or w.featslst[3] == "Number=Plur":
                                    # если нашли подходящее по грамматическим формам местоимение
                                    w.feats = feats

                                    last = ""
                                    for elem in s0.tokens:
                                        # print(elem)
                                        if elem != "None":
                                            if elem.deps == str(w.token_id) + ":nmod" or elem.deps == str(
                                                    w.token_id) + ":amod" or elem.deps == str(w.token_id) + ":appos":
                                                # print("мы нашли зависимое слово", elem.token_id, elem.form, w.form)

                                                # print("прошлый корень:", last)
                                                zz = elem.token_id
                                                t = 0
                                                while zz != "":
                                                    if zz == last:
                                                        zz = ""
                                                        continue
                                                        # print ("ищем зависимое слово от слова", zz)
                                                    for el in s0.tokens:
                                                        if el != "None":
                                                            # print (zz, el.head, el.token_id)
                                                            if el.head == zz and el.upos != "PUNCT":
                                                                last = zz
                                                                # print("перешли на новый уровень. Прошлый корень", last)
                                                                # print ("ЗАВИСИМОСТЬ",el.form, el.token_id)
                                                                zz = el.token_id
                                                                # print("мы удаляем слово", el.form)
                                                                if el.misc == "SpaceAfter=No":
                                                                    # print ("Нужно удалить пробел")
                                                                    ind = int(el.token_id) - 2
                                                                    if s0.tokens[ind] != "None":
                                                                        s0.tokens[ind].misc = "SpaceAfter=No"
                                                                    else:
                                                                        ind = ind - 1
                                                                        s0.tokens[ind].misc = "SpaceAfter=No"
                                                                        # print ("мы заменяем слово", el.form, el.token_id, s0.tokens[int(el.token_id)-1].form)
                                                                s0.tokens[int(el.token_id) - 1] = "None"
                                                        if t == 3:
                                                            zz = last
                                                            t = 0
                                                            continue
                                                        if el != "None" and el.form == s0.tokens[-1].form:
                                                            t = t + 1
                                                            continue

                                                if elem.misc == "SpaceAfter=No":
                                                    ind = int(elem.token_id) - 2

                                                    while True:
                                                        try:
                                                            form = s0.tokens[ind].form
                                                        except AttributeError:
                                                            ind = ind - 1
                                                            continue
                                                        break
                                                    # print ("надо удалить пробел")
                                                    s0.tokens[ind].misc = "SpaceAfter=No"
                                                    # print ("мы удалили пробел")
                                                # print ("мы заменили слово", elem.token_id, s0.tokens[int(elem.token_id)-1].form)
                                                s0.tokens[int(elem.token_id) - 1] = "None"
                                    w.form = pron[1]  # перезаписываем форму существительного на форму местоимения
                                    w.lemma = pron[2]  # перезаписываем лемму существительного на форму местоимения
                                    w.upos = "PRON"
                                    # break
        newtokens = []
        for elems in s0.tokens:
            if elems != "None":
                newtokens.append(elems)
        s0.tokens = newtokens

        self.correct(s0)
        s0.text = s0.make_text()
        self.results.append(s0)
        return s0


# Вторая аугментация. Замена подлежащего-местоимения на существительное
class Second_augmantation(BaseAugmentation):
    def __init__(self):
        self._femnames_list = self._get_femnames()
        self._mascnames_list = self._get_mascnames()

    # функция обработки списка женских имён
    def _get_femnames(self):
        names_list = []
        pronouns0 = open("femnames_.txt", "r")
        pronouns = pronouns0.read()
        pronouns = pronouns.split("\n")
        for line in pronouns:
            line = line.replace("'", "")
            line = line.replace("[", "")
            line = line.replace("]", "")
            line = line.split(", ")
            if line != [""]:
                names_list.append(line)
        return names_list

    # функция обработки списка мужских имён
    def _get_mascnames(self):
        names_list = []
        pronouns0 = open("mascnames_.txt", "r")
        pronouns = pronouns0.read()
        pronouns = pronouns.split("\n")
        for line in pronouns:
            line = line.replace("'", "")
            line = line.replace("[", "")
            line = line.replace("]", "")
            line = line.split(", ")
            if line != [""]:
                names_list.append(line)
        return names_list

    def run(self, s0):
        import random
        for w in s0.tokens:
            # print (w.form,w.upos,w.deprel,w.featslst)
            if w.featslst[3] == "Number=Sing" and w.upos == "PRON" and w.deprel == "nsubj" or w.featslst[
                3] == "Number=Sing" and w.upos == "PRON" and w.deprel == "nsubj:pass":  # ищем подлежащее
                wf = w.feats  # получаем список грамматических характеристик
                if w.featslst[2] == "Gender=Neut":
                    continue
                if w.featslst[2] == "Gender=Fem":
                    newword = random.choice(self._femnames_list)
                if w.featslst[2] == "Gender=Masc":
                    newword = random.choice(self._mascnames_list)
                    # если нашли подходящее по грамматическим формам местоимение
                w.feats = newword[5]
                w._createfeats()
                w.form = newword[1]  # перезаписываем форму существительного на форму местоимения
                w.lemma = newword[2]  # перезаписываем лемму существительного на форму местоимения
                w.upos = "PROPN"
            # break
        newtokens = []
        for elems in s0.tokens:
            newtokens.append(elems)
        s0.tokens = newtokens
        s0.text = s0.make_text()
        self.results.append(s0)
        return s0


# Третья аугментация. Меняет местами два прилагательных.
class ThirdAugmentation(BaseAugmentation):

    def __init__(self):
        # pronouns information
        pass

    def run(self, s0):
        adjindex = -1
        for w in s0.tokens:
            adjindex += 1
            if w != "None":  # если слово не пустое
                if w.upos == "ADJ" and w.deprel == "amod":  # ищем прилагательное
                    nounindex = -1
                    head = w.head
                    if adjindex == "1":
                        w.form = w.form.lower()
                    for noun in s0.tokens:
                        nounindex += 1
                        if noun.token_id == head:
                            if noun.token_id == "1" and noun.upos != "PRON":
                                noun.form = noun.form.lower()
                            if noun.misc == "SpaceAfter=No" and w.misc == "_":
                                w.misc = "SpaceAfter=No"
                                noun.misc = "_"
                            elif w.misc == "SpaceAfter=No" and noun.misc == "_":
                                noun.misc = "SpaceAfter=No"
                                w.misc = "_"

                            s0.tokens[adjindex] = noun
                            s0.tokens[nounindex] = w
                            self.correct(s0)
                            continue

        self.correct(s0)
        s0.text = s0.make_text()
        return s0


class FourthAugmentation(BaseAugmentation):

    def __init__(self):
        self._introduction_words_list = self._get_introduction_words()

    def _get_introduction_words(self):
        words_list = []
        words0 = open("introduction_words.txt", "r")
        words = words0.read()
        words = words.split("\n")
        for line in words:
            line = line.replace("'", "")
            line = line.replace("[", "")
            line = line.replace("]", "")
            line = line.replace(", ", "\t")
            intr_word = Token0()
            intr_word.create(line)
            words_list.append(intr_word)
        return words_list

    def run(self, s0):
        import random
        for w in s0.tokens:
            if w.deprel == "root":  # ищем корень предложения
                head = w.token_id  # получаем номер корневого слова
        newword = random.choice(self._introduction_words_list)
        count = len(s0.tokens) - 1
        place = random.randint(0, count)
        newword.token_id = str(place)
        newword.head = head
        newword.deps = head + ":parataxis"
        comma01 = "\t".join(['', ',', ',', 'PUNCT', '_', '_', '', '', 'None', '_'])
        comma02 = "\t".join(['', ',', ',', 'PUNCT', '_', '_', '', '', 'None', '_'])
        comma_1 = Token0()
        comma_1.create(comma01)
        comma_2 = Token0()
        comma_2.create(comma02)
        com = 0  # отклонение для запятых
        if place == 0 and s0.tokens[0].upos == "PUNCT":
            place += 1
            # print ("ой, на месте тире нельзя, смещаемся", place)
        if place <= count and s0.tokens[place].upos != "PUNCT":
            comma2 = "True"
            # print ("второй запятой быть!", place)
        else:
            # print ("второй запятой не быть!", s0.tokens[place-2].form)
            if place - 2 >= 0:
                newword.misc = s0.tokens[place - 1].misc
                # print ("теперь после слова - ", newword.misc)
            comma2 = "False"
        if place == 0 and s0.tokens[0].upos != "PUNCT":
            comma1 = "False"
            # print ("первой запятой не быть, потому что мы в начале предложения!")
        elif place >= 1 and s0.tokens[place - 1].upos != "PUNCT":
            comma1 = "True"
            # print ("первой запятой быть!", s0.tokens[place-1].upos, "не знак препинания")
        else:
            comma1 = "False"
            # print ("первой запятой не быть")

        # print (s0.tokens[place-1].upos, place, s0.tokens[place].upos, count)
        if s0.tokens[place].form.istitle():
            # print ("Оу, да у нас тут слово с большой буквы")
            if s0.tokens[place].upos != "PROPN":
                s0.tokens[place].form = s0.tokens[place].form.lower()
                newword.form = newword.form.capitalize()
        else:
            newword.form = newword.form.lower()

        if comma2 == "True":
            s0.tokens.insert(place, comma_2)
            s0.tokens[place].token_id = str(102)
            s0.tokens[place].head = str(101)
            s0.tokens[place].deps = str(101) + ":punct"
        # print (comma_2.token_id, comma_2.form, comma_2.lemma, comma_2.upos, comma_2.xpos, comma_2.feats, comma_2.head, comma_2.deprel, comma_2.deps, comma_2.misc)
        s0.tokens.insert(place, newword)
        s0.tokens[place].token_id = str(101)
        if comma1 == "True":
            s0.tokens.insert(place, comma_1)
            s0.tokens[place - 1].misc = "SpaceAfter=No"
            s0.tokens[place].token_id = str(100)
            s0.tokens[place].head = str(101)
            s0.tokens[place].deps = str(101) + ":punct"
            # print (comma_1.token_id, comma_1.form, comma_1.lemma, comma_1.upos, comma_1.xpos, comma_1.feats, comma_1.head, comma_1.deprel, comma_1.deps, comma_1.misc)

        self.correct(s0)
        s0.text = s0.make_text()

        return s0


class FifthAugmentation(BaseAugmentation):

    def __init__(self):
        self.time_words = ["вчера", "завтра", "послезавтра", "позавчера", "назад", "через" "неделе" "в прошл", "скоро"]

    def run(self, s0):
        import random
        import pymorphy2
        morph = pymorphy2.MorphAnalyzer()
        s_base = s0.text  # исходный текст предложения
        answer = ""
        for els in s0.tokens:
            for ws in self.time_words:
                if ws in els.form.lower():
                    answer = "stop"

        if answer != "stop":
            for w in s0.tokens:
                if w.upos == "VERB" and w.featslst[6] == "VerbForm=Fin":  # ищем корень предложения
                    # print ("это то, что нужно заменить", w.form)#получаем номер корневого слова
                    # print(w.token_id, w.featslst)
                    gender = w.featslst[1].lower().replace("gender=", "")
                    number = w.featslst[3].lower().replace("number=", "")
                    person = w.featslst[4].lower().replace("person=", "")
                    subj = ""
                    for words in s0.tokens:
                        if words.deps == w.token_id + ":nsubj":
                            # print  ("подлежащее:", words.form, words.featslst)
                            subj = words.form
                            if words.upos == "PROPN" or words.upos == "NOUN":
                                gender = words.featslst[1]
                                person = "3"
                            if words.upos == "PRON":
                                gender = words.featslst[1]
                                person = words.featslst[4]
                    if subj == "":
                        continue
                    if gender == "":
                        gender = "masc"
                    # print (w.form, gender, number, person)
                    word = morph.parse(w.lemma)[0]
                    v = word.lexeme
                    random.shuffle(v)
                    for elems in v:  # учесть плюралис
                        if elems.word == w.form.lower():
                            # print ("ups")
                            continue
                        tags = str(elems.tag)
                        if "VERB" in tags and "past" in tags and gender in tags and number in tags:
                            # print (elems.word, tags)
                            w.form = elems.word
                            w.featslst[5] = "Tense=Past"
                            break
                        elif "VERB" in tags and "pres" in tags and person in tags and number in tags:
                            # print (elems.word, tags)
                            w.form = elems.word
                            w.featslst[5] = "Tense=Pres"
                            break
                        elif "VERB" in tags and "futr" in tags and person in tags and number in tags:
                            # print (elems.word, tags)
                            w.form = elems.word
                            w.featslst[5] = "Tense=Fut"
                            break
                    w.correctfeats()

        self.correct(s0)
        s0.text = s0.make_text()
        return s0


class SixthAugmentation(BaseAugmentation):
    def __init__(self):
        self._adj_list = self._get_adj()

    def _get_adj(self):
        synonyms_list = []
        pronouns0 = open("adj_synonyms.txt", "r")
        pronouns = pronouns0.read()
        pronouns = pronouns.split("],")
        for line in pronouns:
            line = line.replace("'", "")
            line = line.replace("[", "")
            line = line.replace("]", "")
            line = line.replace(" ", "")
            line = line.split(",")
            if line != [""]:
                synonyms_list.append(line)
        return synonyms_list

    def run(self, s0):
        import random
        import pymorphy2
        morph = pymorphy2.MorphAnalyzer()
        for w in s0.tokens:
            newword = ""
            newlemma = ""
            # print (w.form,w.upos,w.deprel,w.featslst)
            if w.upos == "ADJ":  # ищем прилагательное
                wf = w.feats  # получаем список грамматических характеристик
                # print ("слово которое заменяем",w.form, w.lemma, w.feats)
                random.shuffle(self._adj_list)
                synonyms = []
                for elems in self._adj_list:
                    if w.lemma in elems:
                        synonyms = elems
                        # print ("нашли синонимы",synonyms, type(synonyms))
                        synonyms.remove(w.lemma)
                        # print ("удалили наше слово",synonyms, type(synonyms))
                        break
                if len(synonyms) <= 0:
                    # print ("нет синонимов")
                    break
                newword = random.choice(synonyms)
                synonyms.append(w.lemma)
                # print("это наш синоним",newword)
                # print (w.form)
                word0 = morph.parse(w.form)
                # print ("2", w.form)
                for forms in word0:
                    if "ADJF" in str(forms.tag) and w.featslst[1].lower().replace("case=", "") in str(forms.tag):
                        word0 = forms
                        res = "+"
                        break
                    else:
                        res = "-"
                if res == "-":
                    break

                word_new = morph.parse(newword)[0]
                v = word_new.lexeme
                # print ("характеристики исходного слова",word0, "\n лексема синонима", v)
                for elems in v:
                    if str(elems.tag) == str(word0.tag):
                        newword = elems.word
                        newlemma = elems.normal_form
                if newword == "" or newlemma == "":
                    # print ("нет подходящей формы")
                    continue
                # print ("это наше новое слова и его лемма",newword, newlemma)
                w.form = newword
                w.lemma = newlemma
                # print ("c этим словом закончили")
        newtokens = []
        for elems in s0.tokens:
            newtokens.append(elems)
        s0.tokens = newtokens
        self.correct(s0)
        s0.text = s0.make_text()

        return s0
