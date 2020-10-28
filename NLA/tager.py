import abc
import json
import re

import requests
import spacy

URL = "http://ws.clarin-pl.eu/nlprest2/base/process"
LPMN = "any2txt|wcrft2"


# LPMN = "any2txt|morphoDita"


class TaggerClass(abc.ABC):
    pass

    @abc.abstractmethod
    def tag(self, text):
        pass


class ClarinTagger(TaggerClass):
    def __init__(self, url=URL, lpmn=LPMN, email_address="myemail@email.com"):
        self.url = url
        self.lpmn = lpmn
        self.email_address = email_address

    def tag(self, text):
        doc = {
            "lpmn": self.lpmn,
            "text": text,
            "user": self.email_address
        }
        doc = json.dumps(doc)
        results = requests.post(self.url, data=doc)
        return results.text


class SpacyTagger(TaggerClass):
    def __init__(self):
        self.nlp = spacy.load(
            'pl_core_news_md',
            disable=["ner", "parser", "entity_linker", "textcat",
                     "entity_ruler"]
        )

    def tag(self, text):
        doc = self.nlp(text)
        results = []
        for token in doc:
            results.append({"text": token.text, "tag": token.tag_})
        return results


if __name__ == '__main__':
    with open('lem2.txt', 'r', encoding='utf-8') as f:
        text = f.read().replace('\n', ' ').replace('  ', ' ')
    text = re.sub(r"\[\w\d*\]", '', text)
    tagger = ClarinTagger()
    r = tagger.tag(text)
    print(r)
