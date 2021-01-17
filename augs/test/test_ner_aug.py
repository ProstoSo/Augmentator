import unittest

from augs.aug_ner import NERAug


class TestNERAug(unittest.TestCase):

    def setUp(self):
        self._augmentation = NERAug()

    def test_augmentation(self):
        text = 'random_text'
        augmented_true_text = 'random_text_augmented'
        text = self._augmentation.apply(text)
        self.assertEqual(augmented_true_text, text)
