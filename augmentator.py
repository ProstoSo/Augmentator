from typing import Dict
from random import random

from augs.aug_ner import NERAug
from augs.aug_abbreviation import AugOpenAbbr , AugCloseAbbr
from augs.aug_change_adj import Aug_change_adj
from augs.aug_change_date import Aug_change_date, Aug_change_time
from augs.aug_change_geox import Aug_change_geox
from augs.aug_change_name import Aug_change_name
from augs.aug_change_number import Aug_change_number, Aug_change_number_2
from augs.aug_import_letter import Aug_add_letter
from augs.aug_introduction_words import Aug_introduction_words
from augs.aug_misprint import Aug_misprint
from augs.aug_random_change import Aug_change_letter, Aug_random_change_words
from augs.aug_random_del import Aug_random_del_letter, Aug_random_del_word
from augs.aug_translation import Aug_translation
from augmentations import FirstAugmentation, Second_augmantation, ThirdAugmentation, FourthAugmentation, FifthAugmentation, SixthAugmentation

AUGMENTATIONS = {
    'ner_aug': NERAug
    
}


class Augmentator:

    def __init__(self, augmentations: Dict[str, float], n_aug: int = 1):
        self._augmentations = dict()
        for aug, prob in augmentations.items():
            if aug in AUGMENTATIONS:
                self._augmentations[AUGMENTATIONS[aug]()] = prob
            else:
                print(f'{aug} is not available')
        print(f'Initialized {len(self._augmentations)} augmentations')
        self._n_aug = n_aug

    def augment(self, text: str) -> str:
        applied_counter = 0
        for augmentation, prob in self._augmentations.items():
            aug_prob = random()
            if aug_prob < prob:
                text = augmentation.apply(text)
                applied_counter += 1
                if applied_counter == self._n_aug:
                    break
        return text
