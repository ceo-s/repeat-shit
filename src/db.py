from os import PathLike
import os
import pickle

from src.vocabulary import Vocabulary
from src.library import Library

__all__ = ["Database"]


class Database:
  __instance = None

  def __new__(cls, path: str | PathLike | None = None):
    if cls.__instance is None:
      cls.__instance = super().__new__(cls)

    if path is not None:
      cls.__instance.__path = path
      if not os.path.exists(path):
        os.mkdir(path)
      cls.__instance.__init()

    return cls.__instance

  def __init__(self, path: str | PathLike | None = None) -> None:
    self.__path: str | PathLike
    self.__vocabulary: Vocabulary
    self.__library: Library

  @property
  def vocabulary(self):
    return self.__vocabulary

  @property
  def library(self):
    return self.__library

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

  def __init_library(self):
    library_data_path = f"{self.__path}/library.pickle"
    library_storage_path = f"{self.__path}/library_storage"

    if not os.path.exists(library_storage_path):
      os.mkdir(library_storage_path)

    if not os.path.exists(library_data_path):
      with open(library_data_path, "wb") as file:
        pickle.dump(Library(library_storage_path), file)

    with open(library_data_path, "rb") as file:
      self.__library = pickle.load(file)

  def __save_library(self):
    library_data_path = f"{self.__path}/library.pickle"

    with open(library_data_path, "wb") as file:
      pickle.dump(self.__library, file)
