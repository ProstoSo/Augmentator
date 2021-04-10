import re
from typing import Tuple


def remove_punctuation(word: str) -> str:
    for els in {',', '.', '!', '?'}:
        if els in word:
            word = word.replace(els, '')
    return word

def remove_quote(word:str) -> Tuple[str,str]:
    s = ''
    for q in ['"',"'"]:
        if word.startswith(q):
            s = q
            word = word.replace(q, "")
    return word, s

def remove_punctuation_with_sign(word: str) -> Tuple[str, str]:
    reg=re.compile('\W+')
    s = ''
    result = re.search(reg, word)
    if result is not None:
        match = result.group()
        res = word.endswith(match)
        if res == True:
            word = word.replace(match, "")
            s = match
    return word, s


def remove_whitespace(text: str) -> str:
    for els in {',', '.', '!', '?', ':', ';'}:
        text = text.replace(f' {els}', els)
    return text
