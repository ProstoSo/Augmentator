from typing import Dict
from random import random

from augs.aug_ner import NERAug

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
