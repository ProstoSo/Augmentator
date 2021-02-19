import unittest

from augs.aug_translation import AugTranslation


class TestAugTranslation(unittest.TestCase):

    def setUp(self):
        self._augmentation = AugTranslation()

    def test_augmentation(self):
        text = 'Сегодня мог бы быть хороший день.'
        augmented_text = self._augmentation.apply(text)
        self.assertNotEqual(augmented_text, text)
