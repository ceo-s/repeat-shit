from os import PathLike
from uuid import uuid4
from datetime import datetime
from PIL import Image
from typing import Literal

import os
import shutil

from src.extractors import EpubExtractor


class Book:
  def __init__(self, title: str, cover: Image.Image | None, path: str | PathLike):
    self.__title = title
    self.__cover = cover
    self.__creation_date = datetime.now()
    self.__path = path
    self.__pages = []
    self.__current_page_i = 0
    self.__sync_pages_with_storage()

  @property
  def title(self):
    return self.__title

  @property
  def cover(self):
    return self.__cover

  @property
  def creation_date(self):
    return self.__creation_date

  @property
  def path(self):
    return self.__path

  @property
  def current_page(self):
    return self.__current_page_i + 1

  @current_page.setter
  def current_page(self, val: int):
    val -= 1
    if val < 0:
      val = 0
    elif val >= len(self.__pages):
      val = len(self.__pages) - 1

    self.__current_page_i = val

  @property
  def max_pages(self):
    return len(self.__pages)

  def get_curr_page(self) -> str:
    return self.get_page(self.__current_page_i)

  def get_page(self, i) -> str:
    with open(f"{self.__path}/{self.__pages[i]}") as file:
      return file.read()

  def __sync_pages_with_storage(self):
    self.__pages = sorted(os.listdir(self.__path), key=lambda x: int(x.split(".")[0]))


class Library:
  def __init__(self, storage_path: str | PathLike):
    self.__books: list[Book] = []
    self.__storage_path = storage_path

  @property
  def books(self):
    return self.__books

  def delete_book(self, book: Book):
    self.__books.remove(book)
    shutil.rmtree(book.path)
    del book

  def import_book(self, path: str | PathLike):
    extractor = EpubExtractor(path)
    title = extractor.get_book_title()
    cover = extractor.get_book_cover()

    while True:
      dst_path = f"{self.__storage_path}/{uuid4()}"
      if not os.path.exists(dst_path):
        os.mkdir(dst_path)
        break

    extractor.extract(dst_path)
    book = Book(title, cover, dst_path)
    self.books.append(book)
