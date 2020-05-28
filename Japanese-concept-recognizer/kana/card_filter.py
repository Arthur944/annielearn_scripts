cards = [x.strip().split(";") for x in open("outcards.txt", "r").readlines()]
cards = [[x[0], x[1], x[2].split(" ")] for x in cards]
cards = list(sorted(cards, key=lambda x: len(x[2]), reverse=True))
concepts = {}
real_cards = []
for card in cards:
    ids = card[2]
    i = 0
    while i < len(ids) and not (ids[i] not in concepts.keys() or concepts[ids[i]] < 8):
        i += 1
    if i < len(ids):
        real_cards.append(card)
        for id in ids:
            if id not in concepts.keys():
                concepts[id] = 1
            else:
                concepts[id] += 1
to_write = ""
for card in real_cards:
    to_write += card[0] + ";" + card[1] + ";" + " ".join(card[2]) + "\n"
open("filtered_cards.txt", "w+").write(to_write.strip())
for line in list(sorted([[x, concepts[x]] for x in concepts.keys()], key=lambda x: x[1], reverse=True)):
    print(line)
print(len(concepts.keys()))