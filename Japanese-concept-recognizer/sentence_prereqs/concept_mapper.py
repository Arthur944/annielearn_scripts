import re
import grammar_recognizer as gr
import importlib
from grammar_recognizer import recognize_grammar, pos_tag, encode_tags
from consts import pos_tag_translations, pos_tag_encodings, grammars
from sents import *
import romkan
from functools import reduce
from japanese_text_extractor.japanese_text_extractor import extract_japanese_text


class Concept:
    def __init__(self, id, parent_id, name):
        self.id = id
        self.name = name
        self.parent_id = parent_id

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class WordConcept:
    def __init__(self, read, produce, stem):
        self.read = read
        self.produce = produce
        self.stem = stem

    def __str__(self):
        return self.stem

    def __repr__(self):
        return self.__str__()


class ConceptMapper:
    def __init__(self, server, id_reference_file, kanji_id, word_id):
        self.server = server
        id_reference = [[y.strip() for y in x.split(";")] for x in open(id_reference_file, "r").readlines()]
        self.id_index = {x[0]: Concept(*x) for x in id_reference[1:]}
        self.name_index = {x[2]: Concept(*x) for x in id_reference[1:]}
        self.grammar_index = {x: self.id_index[str(grammars[x])] for x in grammars.keys()}
        self.kanji_index = self.fill_collection_dic({}, kanji_id)
        self.word_index = self.fill_collection_dic({}, word_id)
        self.word_index["この"] = {
            "read": [self.word_index["これ"]["read"], self.grammar_index["the の particle"]],
            "produce": [self.word_index["これ"]["produce"], self.grammar_index["the の particle"]]
        }

    def pos_tag(self, sent):
        return pos_tag(sent, self.server)

    def recognize_grammar(self, sent):
        return recognize_grammar(sent, self.server)

    def analyze_sent(self, sent):
        pos_tags = self.pos_tag(sent)
        encoded = encode_tags(pos_tags)
        found_words = self.find_words_in_sent(pos_tags)
        found_grammars = [{
            **x,
            "coords": [{
                "start": encoded_index_to_pos_index(y["start"], encoded),
                "end": encoded_index_to_pos_index(y["end"], encoded) if encoded_index_to_pos_index(y['end'], encoded) != 0 else 0
            } for y in x["coords"]]
        } for x in self.recognize_grammar(sent)]
        grammar_coords = []
        for grammar in found_grammars:
            for coord in grammar["coords"]:
                grammar_coords.append([coord["start"], coord["end"]])
        coords = [[x["coords"], x["coords"] + 1] for x in found_words] + grammar_coords
        missing_tags = calc_missing_tags(coords + [[len(pos_tags)-1, len(pos_tags)]])
        return {
            "found_words": [WordConcept(**self.word_index[x["stem"]], stem=x["stem"]) for x in found_words],
            "found_grammars": [self.grammar_index[x["name"]] for x in found_grammars if x["name"] in self.grammar_index],
            "missing": self.filter_real_missing(missing_tags, pos_tags),
            "verbose_found_words": [[x['stem'], x['coords']] for x in found_words],
            "verbose_found_grammars": [[x["name"], x["coords"]] for x in found_grammars]
        }

    def filter_real_missing(self, missing_tags, pos_tags):
        tags = reduce(lambda acc, curr_value: acc + [pos_tags[curr_value]], missing_tags, [])
        tags = [x for x in tags if "number" not in x[1] and "symbol" not in x[1]]
        return tags

    def find_words_in_sent(self, pos_tags):
        stems = [x[0] for x in pos_tags]
        words = []
        for i in range(len(stems)):
            if stems[i] in self.word_index.keys():
                words.append({"stem": stems[i], "coords": i})
        return words

    def fill_collection_dic(self, dic, parent_id):
        for key in self.id_index.keys():
            concept = self.id_index[key]
            if concept.parent_id == parent_id and concept.name != "Primitives":
                match = re.search("from (.+) produce (.+)", concept.name)
                if not re.search("[A-Za-z]+", match.group(1)):
                    symbol, meaning = match.group(1), match.group(2)
                    if symbol not in dic:
                        dic[symbol] = {"read": None, "produce": None}
                    dic[symbol]["read"] = concept
                else:
                    meaning, symbol = match.group(1), match.group(2)
                    if symbol not in dic:
                        dic[symbol] = {"read": None, "produce": None}
                    dic[symbol]["produce"] = concept
        return dic


def calc_missing_tags(coords):
    length = max(coords, key=lambda x: x[1])[1]
    section = [0] * length
    for coord in coords:
        if coord[1] != coord[0]:
            section[coord[0]:coord[1]] = [1] * (coord[1] - coord[0])
    missing = []
    for i in range(0, len(section)):
        if section[i] == 0:
            missing.append(i)
    return missing


def encoded_index_to_pos_index(encoded_index, encoded):
    text = encoded[:encoded_index]
    return len(re.findall("ő[^ú]+ú", text))


