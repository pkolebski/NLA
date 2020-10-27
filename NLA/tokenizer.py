import re
from typing import List
import morfeusz2

import regex


class Tokenizer:
    def __init__(self):
        self.morf = morfeusz2.Morfeusz()

    def morf_analysis(self, text):
        if ' ' in text:
            return None
        return self.morf.generate(text)

    def sentencize(self, text: str) -> List[str]:
        text = re.sub(r"\[\w\d*\]", '', text)
        # get im. acronym, e. g. Gimnazjum im. Mikołaja Kopernika
        text = re.sub(r"([A-Z][a-z]*\sim\.)", r"\1<A>", text)
        text = re.sub(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', '<S>', text)
        text = text.replace('<A>', '')
        text = text.split('<S>')
        return text

    def tokenize(self, text: str) -> List[str]:
        text = re.sub(r"(\.{3})", r" <D>\1<D>", text)  # capturing ellpsis
        text = re.sub(r"(\()", r"\1 ", text)  # add whitespace after (
        text = re.sub(r"(\))", r" \1", text)  # add whitespace before )
        text = re.sub(
            r"(\.$|\,)", r" \1", text)  # add whtiespace before , and .

        date_regex = r"\d+\s(?:stycznia|lutego|marca|kwietnia|maja|czerwca|lipca|sierpnia|września|października|listopada|grudnia)+\s?\d*"
        for s in re.findall(date_regex, text):
            s_new = re.sub(r"\s", "<D>", s)
            text = text.replace(s, s_new)

        street_regex = r"(?:przy|na)\sulicy\s[A-Z][a-z]+\s?\d?"
        # print(re.findall(street_regex, text))
        for s in re.findall(street_regex, text):
            s_new = re.sub(r"\s", "<D>", s)
            text = text.replace(s, s_new)

        # captures e.g. II Państwowego Gimnazjum im. Karola Szajnochy as well as Wysoki Zamek
        capitals_regex = r"(?:[A-Z]\p{L}+\s*)+(?:\sim\.)?(?:\s[A-Z]\p{L}+)+"
        for s in regex.findall(capitals_regex, text):
            s_new = re.sub(r"\s", "<D>", s)
            text = text.replace(s, s_new)

        places_regex = r"(?:w|we)\s\p{Lu}[a-z]*"
        for s in regex.findall(places_regex, text):
            s_new = re.sub(r"\s", "<D>", s)
            text = text.replace(s, s_new)

        text = text.split()
        for i, t in enumerate(text):
            text[i] = t.replace("<D>", " ").strip()
        text = ["<SOS>"] + text + ["<EOS>"]
        return text


if __name__ == '__main__':
    with open('lem2.txt', 'r', encoding='utf-8') as f:
        text = f.read().replace('\n', ' ').replace('  ', ' ')

    tokenizer = Tokenizer()
    sentences = tokenizer.sentencize(text)

    for i, sent in enumerate(sentences):
        print(f"Sentence ({i}): {sent}")
        tokens = tokenizer.tokenize(sent)
        for i, t in enumerate(tokens):
            print(f"Token ({i}): {t} - {tokenizer.morf_analysis(t)}")
        print()
