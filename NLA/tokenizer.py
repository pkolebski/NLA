import re
from typing import List


class Tokenizer:
    def sentencize(self, text: str) -> List[str]:
        text = re.sub(r"\[\w\d*\]", '', text)
        text = re.sub(r"([A-Z][a-z]*\sim\.)", r"\1<A>", text)
        text = re.sub(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', '<S>', text)
        text = text.replace('<A>', '')
        text = text.split('<S>')
        return text

    def tokenize(self, text: str) -> List[str]:
        token_pat = r"(?=\W)|(?<=\W)|\s+"
        text = re.sub(token_pat, "<T>", text)
        text = [x for x in text.split("<T>") if x]
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
            print(f"Token ({i}): {t}")
        print()
