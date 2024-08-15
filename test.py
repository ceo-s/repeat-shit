from src.db import Database
from src.vocabulary import Language, Translation

db = Database("db")

for t in db.vocabulary.get(Language.ENGLISH)[0].translations[Language.RUSSIAN]:
  print(t._n_sucess)
  print(t._n_repeat)
