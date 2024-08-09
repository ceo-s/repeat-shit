from os import PathLike
from PIL import Image, ImageTk

import os


class Gallery:
  def __init__(self, path: str | PathLike) -> None:
    self.data = {}
    if not os.path.exists(path):
      print(f"Gallery.__init__ : path \"{path}\" does not exist")
      return

    for image_path in os.listdir(path):
      img = Image.open(os.path.join(path, image_path))
      self.data[image_path] = ImageTk.PhotoImage(img)

  def __getitem__(self, __key: str):
    return self.data[__key]
