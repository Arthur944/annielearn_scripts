import re

csv = open("id_reference.csv", "r").read()
csv = [x.split(';') for x in csv.splitlines()]
csv = csv[1:]


class Concept:
    def __init__(self, name, id, symbol):
        self.id = id
        self.name = name
        self.symbol = symbol


def get_primitives(csv):
    primitives = {}
    for line in csv:
        if line[1] == "47956":
            names = line[2]
            for name in names.split(','):
                if name.strip() != '':
                    primitives[name.strip()] = Concept(name, line[0], name)
    return primitives


def get_kanji_concepts(csv):
    kanji = {}
    for line in csv:
        if line[1] == "293":
            kanji[line[2]] = Concept(line[2], line[0], line[2])
    return kanji


primitives = get_primitives(csv)
kanji_concepts = get_kanji_concepts(csv)

kanji_components = [[y.strip() for y in x.split(";")] for x in open("kanji_components.csv", "r").read().splitlines()]

out_list = []
for line in kanji_components:
    cur_primitive_names = [x.strip() for x in line[1].split(',')]
    cur_primitives = []
    for name in cur_primitive_names:
        if name in primitives.keys():
            cur_primitives.append(primitives[name].id)
    cur_primitives = list(set(cur_primitives))
    print(line[0])
    if line[0] in kanji_concepts:
        out_list.append([kanji_concepts[line[0]].id, cur_primitives])

print(primitives)

to_write = ""
for line in out_list:
    if len(line[1]) > 0:
        to_write += line[0] + ";" + " ".join(line[1]) + "\n"
open("kanji_component_ids.csv", "w+").write(to_write.strip())






