class Concept:
    def __init__(self, id, parent_id, name):
        self.id = id
        self.name = name
        self.parent_id = parent_id

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


id_reference = [[y.strip() for y in x.split(";")] for x in open("../id_reference.csv", "r").readlines()]
id_index = {x[0]: Concept(*x) for x in id_reference[1:]}
name_index = {x[2]: Concept(*x) for x in id_reference[1:]}
kanji_index = {}
for concept in id_index:
    if concept.parent_id == "489":
        match = re.search("from ([a-zA-z ,+) produce (.+)")