import unittest

from augs.aug_introduction_words import AugIntroductionWords


class TestAugIntroductionsWords(unittest.TestCase):

    def setUp(self):
        self._augmentation = AugIntroductionWords()

    def test_augmentation(self):
        text = 'Сегодня хороший день.'
        augmented_text = self._augmentation.apply(text)
        self.assertNotEqual(augmented_text, text)
