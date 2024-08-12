from os import PathLike
import os
import pickle

from src.vocabulary import *

__all__ = ["Database"]


class Database:
  __instance = None

  def __new__(cls, path: str | PathLike | None = None):
    if cls.__instance is None:
      cls.__instance = super().__new__(cls)

    if path is not None:
      cls.__instance.__path = path
      cls.__instance.__init()

    return cls.__instance

  def __init__(self, path: str | PathLike | None = None) -> None:
    self.__path: str | PathLike
    self.__vocabulary: Vocabulary

  def __init(self):
    for p in dir(Database):
      if isinstance(getattr(Database, p), property):
        getattr(self, f"_Database__init_{p}")()

  def save(self):
    for p in dir(Database):
      if isinstance(getattr(Database, p), property):
        getattr(self, f"_Database__save_{p}")()

  def __init_vocabulary(self):
    vocabulary_data_path = f"{self.__path}/vocabulary.pickle"
    if not os.path.exists(vocabulary_data_path):
      with open(vocabulary_data_path, "wb") as file:
        pickle.dump(Vocabulary(), file)

    with open(vocabulary_data_path, "rb") as file:
      self.__vocabulary = pickle.load(file)

  def __save_vocabulary(self):
    vocabulary_data_path = f"{self.__path}/vocabulary.pickle"

    with open(vocabulary_data_path, "wb") as file:
      pickle.dump(self.__vocabulary, file)

  @property
  def vocabulary(self):
    return self.__vocabulary
