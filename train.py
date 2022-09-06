import argparse
import json
import os
import re
import sys


class Train:
    _clear_string_regex = "[^а-яА-ЯA-Za-z ]"
    _model = {}

    def get_clear_string_regex(self) -> str:
        return self._clear_string_regex

    def set_clear_string_regex(self, regex) -> None:
        self._clear_string_regex = regex

    def generate_model_from_file(self, file_path) -> None:
        with open(file_path, "r") as file:
            for line in file.readlines():
                if line == "": continue
                line = line.lower()
                clear_string = re.sub(self._clear_string_regex, " ", line)
                words = clear_string.split(" ")
                last_word = ""
                for word in words:
                    if word == "": continue
                    if last_word == "":
                        last_word = word
                        continue
                    if last_word not in self._model:
                        self._model[last_word] = {}
                    if word not in self._model[last_word]:
                        self._model[last_word][word] = 0
                    self._model[last_word][word] += 1
                    last_word = word

    def generate_from_directory(self, dir_path) -> None:
        path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(dir_path)
        for file_or_dir in os.listdir():
            self.generate_model_from_file(file_or_dir)
        os.chdir(path)

    def save_model(self, name) -> None:
        with open(f"{name}.json", "w", encoding='utf8') as file:
            json.dump(self._model, file, ensure_ascii=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Обучение модели")
    parser.add_argument("--input-dir", dest="input_dir", type=str)
    parser.add_argument("--model", dest="model_file", default="model", type=str, required=True)
    args = parser.parse_args()

    t = Train()
    if args.input_dir is not None:
        t.generate_from_directory(args.input_dir)
    else:
        dir_name = str(hash(__file__))
        os.mkdir(dir_name)
        with open(f"{dir_name}/data.txt", "w", encoding="utf-8") as f:
            f.write(sys.stdin.read())
        t.generate_from_directory(dir_name)
        os.remove(f"{dir_name}/data.txt")
        os.removedirs(dir_name)
    t.save_model(args.model_file)
