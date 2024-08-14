from typing import Union
from collections import defaultdict
from dataclasses import dataclass, field
import random

from src.multienum import MultiEnum

__all__ = ["Language", "Translation", "Word", "Vocabulary"]


class Language(MultiEnum):
  RUSSIAN = "russian", "ru"
  ENGLISH = "english", "en"
  ITALIAN = "italian", "it"
  FRENCH = "french", "fr"


@dataclass
class Translation:
  translation: "Word"
  _n_sucess: int = field(default=0, init=False, compare=False)
  _n_repeat: int = field(default=0, init=False, compare=False)

  @property
  def accuracy(self) -> float:
    return self._n_repeat / (self._n_repeat + 0.0001)

  def repeat(self, sucess: bool):
    self._n_repeat += 1
    self._n_sucess += int(sucess)

  def __str__(self) -> str:
    return f"{self.translation}"

  def __eq__(self, other: Union[str, "Translation", "Word"]) -> bool:
    if isinstance(other, (str, Word)):
      return self.translation == other
    return self.translation == other.translation


@dataclass
class Word:
  word: str
  language: Language
  translations: dict[Language, list[Translation]] = field(default_factory=lambda: defaultdict(list), init=False)

  def get_translations_string(self, language: Language):
    return ", ".join([translation.translation.word for translation in self.translations[language]])

  def __str__(self):
    return f"Word<{self.word}>"

  def __eq__(self, other: Union[str, "Word"]):
    if isinstance(other, str):
      return self.word == other
    return self.word == other.word and self.language == other.language

  def __lt__(self, other: Union[str, "Word"]):
    if isinstance(other, str):
      return self.word < other
    return self.word < other.word

  def __le__(self, other: Union[str, "Word"]):
    if isinstance(other, str):
      return self.word <= other
    return self.word <= other.word


class Vocabulary:
  def __init__(self):
    self.__data: dict[Language, list[Word]] = defaultdict(list)

  def add_word(self, word: Word):
    lst = self.__data[word.language]
    if word not in lst:
      lst.append(word)

  def add_translation(self, word: "Word", translation: "Word"):
    word = self.get_word(word)
    translation = self.get_word(translation)

    lst = word.translations[translation.language]
    lst2 = translation.translations[word.language]

    if translation not in lst:
      lst.append(Translation(translation))

    if word not in lst2:
      lst2.append(Translation(word))

  def get_word(self, word: Word):
    lst = self.__data[word.language]
    if word not in lst:
      raise KeyError(f"Vocabulary does not contain this word!")
    return lst[lst.index(word)]

  def delete_word(self, word: Word):
    lst = self.__data[word.language]
    if word not in lst:
      return

    w_i = lst.index(word)
    word = lst[w_i]
    for _, ts in word.translations.items():
      for t in ts:
        t_i = [x.translation for x in t.translation.translations[word.language]].index(word)
        t.translation.translations[word.language].pop(t_i)

    del self
    lst.pop(w_i)

  def get(self, language: Language) -> list[Word]:
    return self.__data[language].copy()

  def size(self, language: Language) -> int:
    return len(self.__data[language])

  def get_words_to_repeat(self, n: int, lang_from: Language, lang_to: Language) -> list[Word]:
    if n == len(self.get(lang_from)):
      words = self.get(lang_from).copy()
      random.shuffle(words)
      return words

    stats = []
    for word in self.get(lang_from):
      if len(word.translations[lang_to]) == 0:
        continue

      max_accuracy = max([t.accuracy for t in word.translations[lang_to]])
      repeat_count = sum([t._n_repeat for t in word.translations[lang_to]])
      stats.append((max_accuracy, repeat_count, word))

    stats.sort()

    return [stat[2] for stat in stats[:n]]

  def print(self):
    print("Vocabulary:")
    for lang, words in self.__data.items():
      print(f"  {lang.value}:")
      for word in words:
        print(
          f"    {word} -> {", ".join([f'{l.value}: {[str(t.translation) for t in lst]}' for l, lst in word.translations.items()])}")

  def __str__(self) -> str:
    return f"Vocabulary{self.__data}"

  def __in__(self, word: Word) -> bool:
    return word in self.__data[word.language]
