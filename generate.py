import argparse
import json
import random


class Generator:
    _length = 0
    _model = {}

    def __init__(self, prefix):
        self._prefix = prefix

    def set_length(self, length) -> None:
        self._length = length

    def get_length(self) -> int:
        return self._length

    def load_model(self, file_path) -> None:
        with open(file_path, "r") as file:
            self._model = json.load(file)

    def generate(self, block_duplicates) -> str:
        """
        bool:param block_duplicates: Запрещяет дублировать слова
        """
        last_word = random.choice(list(self._model.keys()))
        phrase = []
        if self._prefix[0] != "":
            last_word = self._prefix[-1]
            for i in self._prefix: phrase.append(i)
        for index in range(0, self._length - len(self._prefix)):
            if last_word not in self._model: raise Exception("У меня просто нет слов")
            next_words = sorted(self._model[last_word].items(), key=lambda i: i[1], reverse=True)
            next_word = next_words[0][0]
            now = 0
            all_words = len(next_words)
            while block_duplicates and next_word in phrase:
                now += 1
                if now >= all_words:
                    break
                next_word = next_words[now][0]
            phrase.append(next_word)
            last_word = next_word
        return ' '.join(phrase)


parser = argparse.ArgumentParser(description="Генерация слов")
parser.add_argument("--prefix", dest="prefix", default="", type=str)
parser.add_argument("--length", dest="length", default=10, type=int)
parser.add_argument("--no-repeat", dest="no_repeat", default=False, nargs='?', const=True)
parser.add_argument("--model", dest="model_file", default="model", type=str, required=True)
args = parser.parse_args()

g = Generator(args.prefix.split(" "))
g.load_model(args.model_file)
g.set_length(args.length)
print(g.generate(args.no_repeat))
