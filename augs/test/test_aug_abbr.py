import unittest

from augs.aug_abbreviation import AugCloseAbbr, AugOpenAbbr


class TestAugCloseAbbr(unittest.TestCase):

    def setUp(self):
        self._augmentation = AugCloseAbbr()

    def test_augmentation(self):
        text = 'Я учусь в Новосибирском государственном университете!'
        augmented_true_text = 'Я учусь в НГУ!'
        text = self._augmentation.apply(text)
        self.assertEqual(augmented_true_text, text)

 #если в тексте нет аббревиатуры, текст должен остаться неизменным
    def test_augmentation_2(self):
        text = 'Ты ходил за молоком.'
        augmented_true_text = 'Ты ходил за молоком.'
        text = self._augmentation.apply(text)
        self.assertEqual(augmented_true_text, text)

class TestAugOpenAbbr(unittest.TestCase):

    def setUp(self):
        self._augmentation = AugOpenAbbr()

    def test_augmentation(self):
        text = 'Я учусь в НГУ!'
        augmented_true_text = 'Я учусь в Новосибирском государственном университете!'
        text = self._augmentation.apply(text)
        self.assertEqual(augmented_true_text, text)

    #если в тексте есть аббревиатура, но её нет в словаре, предложение дложно остаться неизменным
    def test_augmentation_2(self):
        text = 'Он служил в ОГВ.'
        augmented_true_text = 'Он служил в ОГВ.'
        text = self._augmentation.apply(text)
        self.assertEqual(augmented_true_text, text)

    #если в тексте нет аббревиатуры, текст должен остаться неизменным
    def test_augmentation_3(self):
        text = 'Ты ходил за молоком.'
        augmented_true_text = 'Ты ходил за молоком.'
        text = self._augmentation.apply(text)
        self.assertEqual(augmented_true_text, text)

    #если в тексте две аббревиатуры, они обе дложны быть расшифрованы
    def test_augmentation_4(self):
        text = 'Я хотел бы учиться в МГУ или в НГУ!'
        augmented_true_text = 'Я хотел бы учиться в Московском государственном университете или в Новосибирском государственном университете!'
        text = self._augmentation.apply(text)
        self.assertEqual(augmented_true_text, text)