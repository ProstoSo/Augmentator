import unittest

from augs.aug_change_adj import AugChangeAdj


class TestAugChangeAdj(unittest.TestCase):

    def setUp(self):
        self._augmentation = AugChangeAdj()

    def test_augmentation(self):
        text = 'У неё два карандаша: красный и синий.'
        augmented_true_text = 'У неё два карандаша: синий и красный.'
        text = self._augmentation.apply(text)
        self.assertEqual(augmented_true_text, text)

    # если в тексте есть союз И но нет прилагательных текст должен остатться неизменным
    def test_augmentation_2(self):
        text = 'У неё два карандаша и три маркера.'
        augmented_true_text = 'У неё два карандаша и три маркера.'
        text = self._augmentation.apply(text)
        self.assertEqual(augmented_true_text, text)
