import unittest

from augs.aug_change_number import AugChangeNumber, AugChangeNumber2


class TestAugChangeNumber(unittest.TestCase):

    def setUp(self):
        self._augmentation = AugChangeNumber()

    def test_augmentation(self):
        text = 'У Пети было много 15 яблок.'
        augmented_text = self._augmentation.apply(text)
        self.assertNotEqual(augmented_text, text)

    # если в тексте нет числа, текст должен остаться неизменным
    def test_augmentation_2(self):
        text = 'У Пети было много яблок.'
        augmented_true_text = 'У Пети было много яблок.'
        text = self._augmentation.apply(text)
        self.assertEqual(augmented_true_text, text)


class TestAugChangeNumber2(unittest.TestCase):

    def setUp(self):
        self._augmentation = AugChangeNumber2()

    def test_augmentation(self):
        text = 'У Пети было 15 яблок.'
        augmented_text = self._augmentation.apply(text,10,20)
        self.assertNotEqual(augmented_text, text)

    # если в тексте нет числа, текст должен остаться неизменным
    def test_augmentation_2(self):
        text = 'У Пети было много яблок.'
        augmented_true_text = 'У Пети было много яблок.'
        text = self._augmentation.apply(text)
        self.assertEqual(augmented_true_text, text)
