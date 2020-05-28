import json

frequency = json.loads(open("frequency.json", "r").read())
notes = [x.split(";") for x in open("kanji_notes_needed.txt", "r").readlines()]
note_to_kanji = {x[0]: x for x in notes}
final_list = []
for elem in frequency[1:]:
    if elem[0] in note_to_kanji.keys():
        final_list.append(note_to_kanji[elem[0]])
with open("reordered_kanji_notes.txt", "w+") as file:
    file.write("".join([";".join(x) for x in final_list]))