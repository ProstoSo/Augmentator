import re
from typing import Tuple


def remove_punctuation(word: str) -> str:
    for els in {',', '.', '!', '?'}:
        if els in word:
            word = word.replace(els, '')
    return word

def remove_quote(word:str) -> Tuple[str,str,str]:
    s_starts = ''
    s_ends = ''
    for q in ['"',"'"]:
        if word.startswith(q):
            s_starts = q
            word = word[1:]
        if word.endswith(q):
            s_ends = q
            word = word.replace(q,'')
    return word, s_starts, s_ends

def remove_punctuation_with_sign(word: str) -> Tuple[str, str]:
    reg=re.compile('[^\w\'"]\W*|\.')
    s = ''
    result = re.search(reg, word)
    if result is not None:
        match = result.group()
        res = word.endswith(match)
        if res == True:
            word = word.replace(match, '')
            s = match
    return word, s


def remove_whitespace(text: str) -> str:
    for els in {',', '.', '!', '?', ':', ';'}:
        text = text.replace(f' {els}', els)
    return text
