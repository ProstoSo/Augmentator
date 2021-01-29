import googletrans
from googletrans import Translator

from augs.base_aug import BaseAug

#аугментация, которая совершает перевод на английский язык и обратно
class AugTranslation(BaseAug):

    ##никаких атрибутов в этой функции не требуется, но я не знаю, можно ли писать так или нужно удалить def __init__ совсем
    def __init__(self):
        pass

    def apply(self, text: str):
        translator = Translator()
        result0 = translator.translate(text, scr='ru', dest='en')
        result = translator.translate(result0.text, src='en', dest='ru')
        return result.text
