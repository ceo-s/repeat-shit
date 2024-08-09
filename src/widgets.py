from tkinter import ttk
from typing import Callable

import tkinter as tk


class LanguagePicker(ttk.Frame):
  LANG_LIST = ["Russian", "English", "Italian", "French"]

  def __init__(self, parent: tk.Misc, button_image: tk.PhotoImage):
    super().__init__(parent, height=50, width=400, style='DarkStyle.TFrame')
    choose_lang_from = ttk.Combobox(self,
                                    values=self.LANG_LIST,
                                    state='readonly')
    choose_lang_from.current(0)

    choose_lang_to = ttk.Combobox(self,
                                  values=self.LANG_LIST,
                                  state='readonly')
    choose_lang_to.current(1)

    exchange_button = ttk.Button(self,
                                 image=button_image,
                                 command=self.__swap_picker_values)
    choose_lang_from.pack(side=tk.LEFT)
    exchange_button.pack(side=tk.LEFT)
    choose_lang_to.pack(side=tk.LEFT)

    self.__choose_lang_from = choose_lang_from
    self.__choose_lang_to = choose_lang_to
    self.__exchange_button = exchange_button

  def __swap_picker_values(self):
    from_val = self.__choose_lang_from.get()
    self.__choose_lang_from.set(self.__choose_lang_to.get())
    self.__choose_lang_to.set(from_val)

  def get_lang_pair(self) -> tuple[str, str]:
    return self.__choose_lang_from.get(), self.__choose_lang_to.get()

  def on_lang_change(callback: Callable[[], None]):
    ...


class WordCountSlider(ttk.Frame):

  def __init__(self, parent: tk.Misc, word_count: int):
    super().__init__(parent, height=50, width=100, style='DarkStyle.TFrame')
    label_string = tk.StringVar(value=f"{1}/{word_count}")
    label = ttk.Label(self, textvariable=label_string)
    slider = ttk.Scale(self, from_=1, to=word_count,
                       length=200, command=self.__update_label_value)
    label.pack()
    slider.pack()

    self.__label_string = label_string
    self.__label = label
    self.__slider = slider

  def __update_label_value(self, value: float):
    self.__label_string.set(f"{int(float(value))}/100")


class ExerciseWidget(ttk.Frame):
  def __init__(self, parent: ttk.Frame):
    super().__init__(self, parent)
    label_string = tk.StringVar()
    label = ttk.Label(self, textvariable=label_string)
    label.pack()

    self.__label_string = label_string
    self.__label = label
