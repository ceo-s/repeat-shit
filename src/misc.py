from typing import Callable
import tkinter as tk
import threading
import functools
from types import MethodType
import time


def add_scroll_linux(widget: tk.Widget):
  widget.bind_all("<Button-4>", lambda e: widget._parent_canvas.yview("scroll", -1, "units"))
  widget.bind_all("<Button-5>", lambda e: widget._parent_canvas.yview("scroll", 1, "units"))


class debounce:

  def __init__(self, timeout: float) -> None:
    self.__timeout = timeout
    self.__timer = threading.Timer(timeout, lambda: None)

  def __call__(self, func: Callable) -> Callable:

    @functools.wraps(func)
    def wrap(*args, **kwargs):
      self.__timer.cancel()
      self.__timer = threading.Timer(self.__timeout, func, args=args, kwargs=kwargs)
      self.__timer.start()

    return wrap
