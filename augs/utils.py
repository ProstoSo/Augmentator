def remove_punctuation(word: str) -> str:
    for els in {',', '.', '!', '?'}:
        if els in word:
            word = word.replace(els, '')
    return word


def remove_whitespace(text: str) -> str:
    for els in {',', '.', '!', '?', ':', ';'}:
        text = text.replace(f' {els}', els)
    return text
