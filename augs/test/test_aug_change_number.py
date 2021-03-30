import unittest

from augs.aug_change_number import AugChangeNumber, AugChangeNumberWithRange


class TestAugChangeNumber(unittest.TestCase):

    def setUp(self):
        self._augmentation = AugChangeNumber()

    def test_augmentation(self):
        text = 'У Пети было много 15 яблок.'
        augmented_text = self._augmentation.apply(text)
        self.assertNotEqual(augmented_text, text)

    def test_augmentation_0(self):
        text = 'У Пети было три шоколадки, но 2 растаяло.'
        augmented_text = self._augmentation.apply(text)
        print (augmented_text)
        self.assertNotEqual(augmented_text, text)

    # если число связано с иностранным словом, то оно всё равно должно быть изменено.
    def test_augmentation_1(self):
        text = 'Сайт выставки Gamescom рассказал о Half-Life 3'
        augmented_text = self._augmentation.apply(text)
        self.assertNotEqual(augmented_text, text)

    # если в тексте нет числа, текст должен остаться неизменным
    def test_augmentation_2(self):
        text = 'У Пети было много яблок.'
        augmented_true_text = 'У Пети было много яблок.'
        text = self._augmentation.apply(text)
        self.assertEqual(augmented_true_text, text)


class TestAugChangeNumberWithRange(unittest.TestCase):

    def setUp(self):
        self._augmentation = AugChangeNumberWithRange()

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

