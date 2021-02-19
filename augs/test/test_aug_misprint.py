import unittest

from augs.aug_misprint import AugMisprint


class TestAugMisprint(unittest.TestCase):

    def setUp(self):
        self._augmentation = AugMisprint()

    def test_augmentation(self):
        text = 'Сегодня хороший день.'
        augmented_text = self._augmentation.apply(text)
        self.assertNotEqual(augmented_text, text)
