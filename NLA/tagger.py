import abc
import json

import click
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


class KrnntTagger(TaggerClass):
    def __init__(self):
        self.url = "http://localhost:9003/?output_format=xces"

    def tag(self, text):
        results = requests.post(self.url, data=text.encode('utf-8'))
        return results.text


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


@click.command()
@click.option('--file-path', '-fp',
              type=click.STRING,
              default="data/test-raw.txt",
              # default="/home/pkolebski/Projects/semester2/nla/NLA/NLA/wiki_data/wiki_train_34_categories_data/Albania_59.txt",
              help="Path to the file you want to tag")
@click.option('--lpmn', '-l',
              type=click.STRING,
              default=LPMN,
              help="LPMN for the tagger API - use any2txt|wcrft2 or "
                   "any2txt|morphoDita")
def run_tagger(file_path, lpmn):
    with open(file_path, encoding='utf-8') as f:
        text = f.read()
    tagger = KrnntTagger()
    tagged_text = tagger.tag(text)
    # print(tagged_text)
    with open("xd.ccl", "w") as f:
        f.write(tagged_text)


if __name__ == '__main__':
    run_tagger()
