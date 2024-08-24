from abc import abstractmethod, ABC
from typing import Literal

import requests
import bs4
import googletrans as gt


class BaseTranslator(ABC):

  @classmethod
  @abstractmethod
  def is_connected(cls) -> bool:
    ...

  @classmethod
  @abstractmethod
  def translate(cls, word: str, lang_from: str, lang_to: str) -> list[str]:
    ...


class Translator(BaseTranslator):

  GOOGLE_TRANSLATOR = gt.Translator()

  @classmethod
  def is_connected(cls) -> bool:
    try:
      requests.head("https://google.com", timeout=2)
      return True
    except:
      return False

  @classmethod
  def translate(cls, word: str, lang_from: str, lang_to: str) -> list[str]:
    """
    Raises:
      ConnectionError: if requests could not connect to the endpoint
      RuntimeError: if bs4 could not find required tag in html
    """
    translations = []

    resp = requests.get(f"https://glosbe.com/{lang_from}/{lang_to}/{word}", timeout=5)

    if resp.status_code == 200:
      soup = bs4.BeautifulSoup(resp.text, features="html.parser")

      cls.__extract_main(soup, translations)
      cls.__extract_adds(soup, translations)

    if len(translations) == 0:
      translations.append(cls.translate_with_google(word, lang_from, lang_to))

    return translations

  @classmethod
  def __extract_main(cls, soup: bs4.BeautifulSoup, translations: list[str]):
    el = soup.find("ul", class_="pr-1")
    if el is not None:
      els = el.find_all(class_="translation__item__pharse")
      for el in els:
        if isinstance(el, bs4.Tag):
          translations.append(el.text.strip().lower())

  @classmethod
  def __extract_adds(cls, soup: bs4.BeautifulSoup, translations: list[str]):
    el = soup.find("ul", id="less-frequent-translations-container-0")
    if el is not None:
      el = el.li
      if el is not None:
        el = el.ul

    if el is not None:
      if isinstance(el, bs4.Tag):
        for item in el.children:
          if isinstance(item, bs4.NavigableString):
            continue
          translations.append(item.text.strip().lower())

  @classmethod
  def translate_with_google(cls, word: str, lang_from: str | None, lang_to: str) -> str:
    if lang_from is None:
      lang_from = "auto"
    return cls.GOOGLE_TRANSLATOR.translate(word, lang_to, lang_from).text

  @classmethod
  def detect_language(cls, word: str) -> tuple[str, float]:
    d = cls.GOOGLE_TRANSLATOR.detect(word)
    return d.lang, d.confidence
