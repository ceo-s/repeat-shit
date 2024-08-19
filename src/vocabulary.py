from typing import Union
from collections import defaultdict
from dataclasses import dataclass, field
import random

from src.multienum import MultiEnum

__all__ = ["Language", "Translation", "Word", "Vocabulary"]


class Language(MultiEnum):
  AFRIKAANS = 'af', 'afrikaans'
  ALBANIAN = 'sq', 'albanian'
  AMHARIC = 'am', 'amharic'
  ARABIC = 'ar', 'arabic'
  ARMENIAN = 'hy', 'armenian'
  AZERBAIJANI = 'az', 'azerbaijani'
  BASQUE = 'eu', 'basque'
  BELARUSIAN = 'be', 'belarusian'
  BENGALI = 'bn', 'bengali'
  BOSNIAN = 'bs', 'bosnian'
  BULGARIAN = 'bg', 'bulgarian'
  CATALAN = 'ca', 'catalan'
  CEBUANO = 'ceb', 'cebuano'
  CHICHEWA = 'ny', 'chichewa'
  CHINESE_SIMPLIFIED = 'zh-cn', 'chinese (simplified)'
  CHINESE = 'zh-tw', 'chinese (traditional)'
  CORSICAN = 'co', 'corsican'
  CROATIAN = 'hr', 'croatian'
  CZECH = 'cs', 'czech'
  DANISH = 'da', 'danish'
  DUTCH = 'nl', 'dutch'
  ENGLISH = 'en', 'english'
  ESPERANTO = 'eo', 'esperanto'
  ESTONIAN = 'et', 'estonian'
  FILIPINO = 'tl', 'filipino'
  FINNISH = 'fi', 'finnish'
  FRENCH = 'fr', 'french'
  FRISIAN = 'fy', 'frisian'
  GALICIAN = 'gl', 'galician'
  GEORGIAN = 'ka', 'georgian'
  GERMAN = 'de', 'german'
  GREEK = 'el', 'greek'
  GUJARATI = 'gu', 'gujarati'
  HAITIAN = 'ht', 'haitian creole'
  HAUSA = 'ha', 'hausa'
  HAWAIIAN = 'haw', 'hawaiian'
  HEBREW = 'iw', 'hebrew'
  HEBREW_ = 'he', 'hebrew'
  HINDI = 'hi', 'hindi'
  HMONG = 'hmn', 'hmong'
  HUNGARIAN = 'hu', 'hungarian'
  ICELANDIC = 'is', 'icelandic'
  IGBO = 'ig', 'igbo'
  INDONESIAN = 'id', 'indonesian'
  IRISH = 'ga', 'irish'
  ITALIAN = 'it', 'italian'
  JAPANESE = 'ja', 'japanese'
  JAVANESE = 'jw', 'javanese'
  KANNADA = 'kn', 'kannada'
  KAZAKH = 'kk', 'kazakh'
  KHMER = 'km', 'khmer'
  KOREAN = 'ko', 'korean'
  KURDISH = 'ku', 'kurdish (kurmanji)'
  KYRGYZ = 'ky', 'kyrgyz'
  LAO = 'lo', 'lao'
  LATIN = 'la', 'latin'
  LATVIAN = 'lv', 'latvian'
  LITHUANIAN = 'lt', 'lithuanian'
  LUXEMBOURGISH = 'lb', 'luxembourgish'
  MACEDONIAN = 'mk', 'macedonian'
  MALAGASY = 'mg', 'malagasy'
  MALAY = 'ms', 'malay'
  MALAYALAM = 'ml', 'malayalam'
  MALTESE = 'mt', 'maltese'
  MAORI = 'mi', 'maori'
  MARATHI = 'mr', 'marathi'
  MONGOLIAN = 'mn', 'mongolian'
  MYANMAR_BURMESE = 'my', 'myanmar (burmese)'
  NEPALI = 'ne', 'nepali'
  NORWEGIAN = 'no', 'norwegian'
  ODIA = 'or', 'odia'
  PASHTO = 'ps', 'pashto'
  PERSIAN = 'fa', 'persian'
  POLISH = 'pl', 'polish'
  PORTUGUESE = 'pt', 'portuguese'
  PUNJABI = 'pa', 'punjabi'
  ROMANIAN = 'ro', 'romanian'
  RUSSIAN = 'ru', 'russian'
  SAMOAN = 'sm', 'samoan'
  SCOTS = 'gd', 'scots gaelic'
  SERBIAN = 'sr', 'serbian'
  SESOTHO = 'st', 'sesotho'
  SHONA = 'sn', 'shona'
  SINDHI = 'sd', 'sindhi'
  SINHALA = 'si', 'sinhala'
  SLOVAK = 'sk', 'slovak'
  SLOVENIAN = 'sl', 'slovenian'
  SOMALI = 'so', 'somali'
  SPANISH = 'es', 'spanish'
  SUNDANESE = 'su', 'sundanese'
  SWAHILI = 'sw', 'swahili'
  SWEDISH = 'sv', 'swedish'
  TAJIK = 'tg', 'tajik'
  TAMIL = 'ta', 'tamil'
  TELUGU = 'te', 'telugu'
  THAI = 'th', 'thai'
  TURKISH = 'tr', 'turkish'
  UKRAINIAN = 'uk', 'ukrainian'
  URDU = 'ur', 'urdu'
  UYGHUR = 'ug', 'uyghur'
  UZBEK = 'uz', 'uzbek'
  VIETNAMESE = 'vi', 'vietnamese'
  WELSH = 'cy', 'welsh'
  XHOSA = 'xh', 'xhosa'
  YIDDISH = 'yi', 'yiddish'
  YORUBA = 'yo', 'yoruba'
  ZULU = 'zu', 'zulu'

  @property
  def short(self) -> str:
    return self._all_values[0]

  @property
  def full(self) -> str:
    return self._all_values[1]


@dataclass
class Translation:
  translation: "Word"
  _n_sucess: int = field(default=0, init=False, compare=False)
  _n_repeat: int = field(default=0, init=False, compare=False)

  @property
  def accuracy(self) -> float:
    return self._n_sucess / (self._n_repeat + 0.0001)

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

  def __hash__(self) -> int:
    return hash(self.word + self.language.short)


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

    stats = [stat[2] for stat in stats[:n]]
    random.shuffle(stats)
    return stats

  def print(self):
    print("Vocabulary:")
    for lang, words in self.__data.items():
      print(f"  {lang.value}:")
      for word in words:
        print(
          f"    {word} -> {", ".join([f'{l.value}: {[str(t.translation) for t in lst]}' for l, lst in word.translations.items()])}")

  def __str__(self) -> str:
    return f"Vocabulary{self.__data}"

  def __contains__(self, word: Word) -> bool:
    return word in self.__data[word.language]
