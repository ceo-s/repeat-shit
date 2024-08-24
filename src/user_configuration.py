from dataclasses import dataclass
from src.vocabulary import Language


@dataclass
class UserConfiguration:
  reader_font_size: int = 18
  reader_lang_to: Language = Language.ENGLISH
