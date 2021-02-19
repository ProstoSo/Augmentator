import unittest

from augs.aug_random_change import AugRandomChangeWords, AugChangeLetters


class TestAugRandomChange(unittest.TestCase):

    def setUp(self):
        self._augmentation = AugRandomChangeWords()

    def test_augmentation(self):
        text = 'Сегодня хороший день.'
        augmented_text = self._augmentation.apply(text)
        self.assertNotEqual(augmented_text, text)


class TestAugRandomChange2(unittest.TestCase):

    def setUp(self):
        self._augmentation = AugChangeLetters()

    def test_augmentation(self):
        text = 'Сегодня хороший день.'
        augmented_text = self._augmentation.apply(text)
        self.assertCountEqual(augmented_text, text)
