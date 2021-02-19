import unittest

from augs.aug_change_date import AugChangeDate, AugChangeTime


class TestAugChangeDate(unittest.TestCase):

    def setUp(self):
        self._augmentation = AugChangeDate()

    def test_augmentation(self):
        text = 'Я родился 12.06.1999, а она в феврале 2004, а Павел 13/04/1995.'
        augmented_text = self._augmentation.apply(text)
        self.assertNotEqual(augmented_text, text)

    # если в тексте нет даты, текст должен остаться неизменным
    def test_augmentation_2(self):
        text = 'Она родилась вчера.'
        augmented_true_text = 'Она родилась вчера.'
        text = self._augmentation.apply(text)
        self.assertEqual(augmented_true_text, text)


class TestAugChangeTime(unittest.TestCase):

    def setUp(self):
        self._augmentation = AugChangeTime()

    def test_augmentation(self):
        text = 'Завтра в 16:00 будет собрание.'
        augmented_text = self._augmentation.apply(text)
        self.assertNotEqual(augmented_text, text)

    # если в тексте нет времени, текст должен остаться неизменным
    def test_augmentation_2(self):
        text = 'Завтра будет собрание.'
        augmented_true_text = 'Завтра будет собрание.'
        text = self._augmentation.apply(text)
        self.assertEqual(augmented_true_text, text)
