from googletrans import Translator

from .base_aug import BaseAug

#аугментация, которая совершает перевод на английский язык и обратно
class AugTranslation(BaseAug):

    def __init__(self):
        self._translator = Translator()

    def apply(self, text: str):
        result0 = self._translator.translate(text, scr='ru', dest='en')
        result = self._translator.translate(result0.text, src='en', dest='ru')
        return result.text
