from typing import Dict
from random import random, shuffle

from augs.aug_abbreviation import AugOpenAbbr , AugCloseAbbr
from augs.aug_change_adj import AugChangeAdj
from augs.aug_change_date import AugChangeDate, AugChangeTime
from augs.aug_change_geox import AugChangeGeox
from augs.aug_change_name import AugChangeName
from augs.aug_change_number import AugChangeNumber, AugChangeNumber2
from augs.aug_import_letter import AugAddLetter
from augs.aug_introduction_words import AugIntroductionWords
from augs.aug_misprint import AugMisprint
from augs.aug_random_change import AugChangeLetters, AugRandomChangeWords
from augs.aug_random_del import AugRandomDelLetter, AugRandomDelWord
from augs.aug_translation import AugTranslation
from augmentations import FirstAugmentation, Second_augmantation, ThirdAugmentation, FourthAugmentation, FifthAugmentation, SixthAugmentation

AUGMENTATIONS = {
    'open_abbreviation_aug':AugOpenAbbr,
    'close_abbreviation_aug':AugCloseAbbr,
    'change_date_aug':AugChangeDate,
    'change_adj_aug' :AugChangeAdj,
    'change_time_aug': AugChangeTime,
    'change_geox_aug':AugChangeGeox,
    'change_name_aug' :AugChangeName,
    'change_number_aug': AugChangeNumber,
    'change_number_2_aug': AugChangeNumber2,
    'import_letter_aug' : AugAddLetter,
    'introduction_words_aug': AugIntroductionWords,
    'misprint_aug': AugMisprint,
    'random_change_letters_aug' : AugChangeLetters,
    'random_change_words_aug': AugRandomChangeWords,
    'random_del_letters_aug': AugRandomDelLetter,
    'random_del_word_aug': AugRandomDelWord,
    'translation_aug': AugTranslation,
    'first_synt_aug': FirstAugmentation,
    'second_synt_aug':Second_augmantation,
    'third_synt_aug':ThirdAugmentation,
    'fourth_synt_aug':FourthAugmentation,
    'fifth_synt_aug': FifthAugmentation,
    'sixth_synt_aug': SixthAugmentation
    
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
        keys_list=list(self._augmentations.keys())
        shuffle(keys_list)

        for augmentation in keys_list:
            aug_prob = random()
            if aug_prob < self._augmentations[augmentation]:
                text = augmentation.apply(text)
                applied_counter += 1
                if applied_counter == self._n_aug:
                    break
        return text
