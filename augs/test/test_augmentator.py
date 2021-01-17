import unittest

from augmentator import Augmentator


class TestAugmentator(unittest.TestCase):

    def test_augmentator(self):
        augmetations = {'ner_aug': 1.0}  # вероятность 1.0 - чтобы аугментация точно сработала
        augmentator = Augmentator(augmentations=augmetations)

        text = 'random_text'
        augmented_true_text = 'random_text_augmented'
        text = augmentator.augment(text)
        self.assertEqual(augmented_true_text, text)
