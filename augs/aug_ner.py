from .base_aug import BaseAug


class NERAug(BaseAug):

    def __init__(self):
        self._geo_names = set()

    def apply(self, text: str):
        return f'{text}_augmented'
