from os import PathLike
from PIL import Image, ImageTk

import os
import sys


def get_resource_path(relative_path: str | PathLike):
  base_path = getattr(
      sys,
      '_MEIPASS',
      None)

  if base_path is None:
    base_path = getattr(
      sys,
      '_MEIPASS2',
      os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

  return os.path.join(base_path, relative_path)


class Gallery:
  __instances = {}

  def __new__(cls, path: str | PathLike):
    path = get_resource_path(path)
    if path not in cls.__instances:
      cls.__instances[path] = super().__new__(cls)
      cls.__instances[path].__init(path)
    return cls.__instances[path]

  def __init(self, path: str | PathLike) -> None:
    self.data = {}
    if not os.path.exists(path):
      print(f"Gallery.__init : path \"{path}\" does not exist")
      return

    for image_path in os.listdir(path):
      img = Image.open(os.path.join(path, image_path))
      self.data[image_path] = ImageTk.PhotoImage(img)

  def __getitem__(self, __key: str) -> ImageTk.PhotoImage:
    return self.data[__key]
