import unittest

from augs.aug_import_letter import AugAddLetter


class TestAugImportLetter(unittest.TestCase):

    def setUp(self):
        self._augmentation = AugAddLetter()

    def test_augmentation(self):
        text = 'Сегодня хороший день.'
        augmented_text = self._augmentation.apply(text)
        self.assertNotEqual(augmented_text, text)
