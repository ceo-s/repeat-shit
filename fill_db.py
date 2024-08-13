from src.db import Database
from src.vocabulary import Vocabulary, Word, Translation, Language

db = Database("db")

# w1 = Word("hello", Language("en"))
# w2 = Word("bye", Language("en"))
# w3 = Word("hi", Language("en"))
# w4 = Word("привет", Language("ru"))
# w5 = Word("пока", Language("ru"))
# w6 = Word("здравствуйте", Language("ru"))
# w7 = Word("salve", Language("it"))
# db.vocabulary.delete_word(w1)
# db.vocabulary.delete_word(w2)
# db.vocabulary.delete_word(w3)
# db.vocabulary.delete_word(w4)
# db.vocabulary.delete_word(w5)
# db.vocabulary.delete_word(w6)
# db.vocabulary.add_word(w1)
# db.vocabulary.add_word(w2)
# db.vocabulary.add_word(w3)
# db.vocabulary.add_word(w4)
# db.vocabulary.add_word(w5)
# db.vocabulary.add_word(w6)
# db.vocabulary.add_word(w7)
# db.vocabulary.add_translation(w1, w4)
# db.vocabulary.add_translation(w1, w6)
# db.vocabulary.add_translation(w2, w5)
# db.vocabulary.add_translation(w3, w4)
# db.vocabulary.add_translation(w1, w7)
# db.vocabulary.add_translation(w4, w7)
# db.vocabulary.add_translation(w6, w7)

db.vocabulary.print()
print(db.vocabulary.get_word(Word("hello", Language.ENGLISH)).get_translations_string(Language.RUSSIAN))
print(db.vocabulary.get_word(Word("hello", Language.ENGLISH)).get_translations_string(Language.ITALIAN))
db.vocabulary.get_words_to_repeat(1, Language.ENGLISH, Language.RUSSIAN)
print(Word("AA", Language.ENGLISH) < Word("AB", Language.ENGLISH))
print(Word("AA", Language.ENGLISH) <= Word("AB", Language.ENGLISH))
print(Word("AA", Language.ENGLISH) > Word("AB", Language.ENGLISH))
print(Word("AA", Language.ENGLISH) >= Word("AB", Language.ENGLISH))
print("AA" < "AB")
# print(db.vocabulary)
db.save()
