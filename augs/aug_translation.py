from augs.base_aug import BaseAug
import googletrans
from googletrans import Translator

class Aug_translation(BaseAug):

    def __init__(self):
        pass

    def apply(self, text: str):
        translator = Translator()
        result0 = translator.translate(text, scr='ru', dest='en')
        result = translator.translate(result0.text, src='en', dest='ru')
        return (result.text)