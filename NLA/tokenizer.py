from typing import List


class Tokenizer:
    def __init__(self, end_of_sentence_marks: List[str] = None):
        if end_of_sentence_marks is not None:
            self.end_of_sentence_marks = end_of_sentence_marks
        else:
            self.end_of_sentence_marks = ['.', '?', '!']

    def tokenize(self, text: str):
        output = list()
        text = [text]
        for mark in self.end_of_sentence_marks:
            output.extend([sentence.split(mark) for sentence in text])
            text, ouput = output[0], []
        return text


if __name__ == '__main__':
    text = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. " \
           "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, " \
           "when an unknown printer took a galley of type and scrambled it to make a type " \
           "specimen book. It has survived not only five centuries, but also the leap into " \
           "electronic typesetting, remaining essentially unchanged. It was popularised in " \
           "the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, " \
           "and more recently with desktop publishing software like Aldus PageMaker " \
           "including versions of Lorem Ipsum."
    print(Tokenizer().tokenize(text))
