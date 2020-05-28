# Create cards from the supplied words
from jap_prereq_creator import ConceptMapper, hiragana, muddy_katakana, muddy_hiragana, katakana

mapper = ConceptMapper('id_reference.csv', kanji_id="293")
words = open("jap_words.csv", "r", encoding="utf-8").readlines()
words = [x.strip() for x in words]
words = list(set(words))
to_write = ""
for word in words:
    in_romanji = mapper.word_to_romanji(word)
    to_write += "How do you pronounce " + word.strip() + "?;" + in_romanji + ";"\
                    + " ".join(mapper.word_prereqs(word)).strip() + "\n"
    if word[0] in hiragana or word[0] in muddy_hiragana:
        print(word)
        print(mapper.word_prereqs(word.strip()))
        print([mapper.reverse_concept(x) for x in mapper.word_prereqs(word)])
        to_write += "Write in hiragana:** " + in_romanji + "** !;" + word.strip() + ";" \
                    + " ".join([mapper.reverse_concept(x) for x in mapper.word_prereqs(word)]).strip() + "\n"
    else:
        to_write += "Write in katakana: **" + in_romanji + "** !;" + word.strip() + ";" \
                    + " ".join([mapper.reverse_concept(x) for x in mapper.word_prereqs(word)]).strip() + "\n"
to_write = to_write.strip()
with open("outcards.txt", "w+", encoding="utf-8") as file:
    file.write(to_write)

