import unittest

from augs.aug_random_del import AugRandomDelLetter, AugRandomDelWord


class TestAugRandomDel(unittest.TestCase):

    def setUp(self):
        self._augmentation = AugRandomDelLetter()

    def test_augmentation(self):
        text = 'Сегодня хороший день.'
        augmented_text = self._augmentation.apply(text)
        self.assertNotEqual(augmented_text, text)


class TestAugRandomDel2(unittest.TestCase):

    def setUp(self):
        self._augmentation = AugRandomDelWord()

    def test_augmentation(self):
        text = 'Сегодня хороший день.'
        augmented_text = self._augmentation.apply(text)
        self.assertNotEqual(augmented_text, text)