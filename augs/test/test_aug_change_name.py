import unittest

from augs.aug_change_name import AugChangeName


class TestAugChangeName(unittest.TestCase):

    def setUp(self):
        self._augmentation = AugChangeName()

    def test_augmentation(self):
        text = 'Маргарита Александровна умная женщина.'
        augmented_text = self._augmentation.apply(text)
        self.assertNotEqual(augmented_text, text)

    # если в тексте есть иностранное имя, оно тоже должно быть изменено
    def test_augmentation_1(self):
        text = 'Эминем обогнал Леди Гагу по "лайкам"'
        augmented_text = self._augmentation.apply(text)
        self.assertNotEqual(augmented_text, text)

    # если в тексте нет имени, текст должен остаться неизменным
    def test_augmentation_2(self):
        text = 'Он сел в машину.'
        augmented_true_text = 'Он сел в машину.'
        text = self._augmentation.apply(text)
        self.assertEqual(augmented_true_text, text)
