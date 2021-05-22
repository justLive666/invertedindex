DEFAULT_PATH_DOCUMENT = r'wikipedia_sample'
DEFAULT_PATH_STOP_WORDS = r'stop_words_en.txt'

import re
import json
import argparse
from functools import reduce


class InvertedIndex:
    def __init__(self, inverted_index: dict):
        self.inverted_index = {i: k for i, k in inverted_index.items()}

    def dump(self, filepath):
        print("Запись в json файл...")
        self.json_object = json.dumps(self.inverted_index)

        with open(file=filepath, mode='w') as json_file:
            json_file.write(self.json_object)

    def query(self, words: list):
        print("Поиск пересечений слов...")
        self.all_lists = []
        self.words = words
        for list in self.words:
            try:
                self.all_lists.append(self.inverted_index[list])# [[1,2,3],[1,2,3]]
            except:
                pass
        try:
            self.crossing_obj = set.intersection(*map(set, self.all_lists)) # {1,2}
        except:
            self.crossing_obj = {}
        self.crossing_arr = []
        for i in self.crossing_obj:
            self.crossing_arr.append(i)  # [1,2]
        return self.crossing_arr

    def save_query(self, original_wiki_path, save_path, cross_lines):
        print("Запись пересечений в файл...")
        self.original = load_documents(original_wiki_path)
        self.lines_index_in_file = [] # [12,44] -> [0,2]
        for i in cross_lines:
            for j in enumerate(self.original[1]):
                if i == j[1]:
                    self.lines_index_in_file.append(j[0])
        with open(file=save_path, encoding='utf-8', mode='w') as file:
            for line in enumerate(self.lines_index_in_file):
                file.write(f"{cross_lines[line[0]]} {' '.join(self.original[0][line[1]])}\n")

    @classmethod
    def load(cls, filepath):
        print("Загрузка json файла...")
        with open(file=filepath, encoding='utf-8', mode='r') as file:
            new_obj = json.load(file)
        return InvertedIndex(new_obj)


def build_inverted_index(document_filepath=DEFAULT_PATH_DOCUMENT, stop_words_filepath=DEFAULT_PATH_STOP_WORDS):
    document = load_documents(document_filepath)  # [['two', 'one', 'hello'], ['b', 'one']]    [1, 2]
    stop_words = load_stop_words(stop_words_filepath)

    document = clear_stop_words(document, stop_words)
    dictionary = {}
    print("Создание словаря...")
    for line in enumerate(document[0]):
        for word in line[1]:
            if word not in dictionary:
                dictionary[word] = [document[1][line[0]]]
            else:
                if document[1][line[0]] not in dictionary[word]:
                    dictionary[word].append(document[1][line[0]])
    return InvertedIndex(dictionary)


def load_stop_words(filepath):
    with open(file=filepath, encoding='utf-8', mode='r') as file:
        stop_words = file.read().strip('\n').split('\n')
        return stop_words


def load_documents(filepath):
    print("Загрузка документа...")
    with open(file=filepath, encoding='utf-8', mode='r') as file:
        doc = file.read().strip().split('\n')
        words = []
        index = []
        for line in doc:
            new_line = ' '.join(line.split()).split(' ', maxsplit=1)
            index.append(int(new_line[0]))
            words.append(new_line[1].split(' '))

        return words, index


def clear_stop_words(document, stop_words):
    print("Очистка...")
    for line in enumerate(document[0]):
        str = re.sub(pattern='[^a-zA-Z ]', repl='', string=" ".join(line[1]))
        str = [word for word in str.strip().split(' ') if word not in stop_words]
        document[0][line[0]] = str
    return document


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-file_path', '--w', type=str, default=DEFAULT_PATH_DOCUMENT, help='Enter wiki_sample path')
    parser.add_argument('-json_path', '--j', type=str, default="dictionary.json",
                        help='Enter json file path to save it')
    parser.add_argument('-stop_path', '--s', type=str, default=DEFAULT_PATH_STOP_WORDS, help='Enter stop words path')
    parser.add_argument('-load_index', '--l', type=str, default="", help='Enter index file path to load it')
    parser.add_argument('-query', '--q', nargs='+', default="", help='Enter words to query them')
    parser.add_argument('-q_save', '--q_s', type=str, default="crossing.txt", help='Enter path to save crossing lines')

    flags = parser.parse_args()
    return flags


def main():
    flags = create_parser()

    if len(flags.l) > 0:
        ii = InvertedIndex.load(flags.l)
    else:
        ii = build_inverted_index(flags.w, flags.s)
        ii.dump(flags.j)
    if len(flags.q) > 0:
        crossing = ii.query(flags.q)
        print(crossing)
        if len(flags.q_s) > 0:
            ii.save_query(flags.w,flags.q_s,crossing)


if __name__ == '__main__':
    main()
