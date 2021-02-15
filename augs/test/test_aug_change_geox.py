import unittest

from augs.aug_change_geox import AugChangeGeox


class TestAugChangeGeox(unittest.TestCase):

    def setUp(self):
        self._augmentation = AugChangeGeox()

    def test_augmentation(self):
        text = 'Он живет в Новосибирске.'
        augmented_text = self._augmentation.apply(text)
        self.assertNotEqual(augmented_text, text)

    # если в тексте есть географическое название, но его нет в словаре, текст должен остаться неизменным
    def test_augmentation_2(self):
        text = 'Он живет в Кардиффе.'
        augmented_true_text = 'Он живет в Кардиффе.'
        text = self._augmentation.apply(text)
        self.assertEqual(augmented_true_text, text)

    # если в тексте нет географического названия, текст должен остаться неизменным
    def test_augmentation_3(self):
        text = 'Он живет в другой стране.'
        augmented_true_text = 'Он живет в другой стране.'
        text = self._augmentation.apply(text)
        self.assertEqual(augmented_true_text, text)
