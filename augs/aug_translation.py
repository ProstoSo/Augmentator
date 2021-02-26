from googletrans import Translator

from augs.base_aug import BaseAug


class AugTranslation(BaseAug):
    """ Аугментация, которая совершает перевод на английский язык и обратно """

    def __init__(self):
        self._translator = Translator()

    def apply(self, text: str) -> str:
        result0 = self._translator.translate(text, scr='ru', dest='en')
        result = self._translator.translate(result0.text, src='en', dest='ru')
        return result.text
