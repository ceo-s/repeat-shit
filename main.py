
from tkinter import Tk

import tkinter as tk
from tkinter import ttk


from src.colors import *
from src.db import Database
from src.endpoints import init_endpoints, build_main_endpoint


def main() -> None:
  db = Database("db")
  root = Tk()
  root.geometry("{x}x{y}".format(
    x=root.winfo_screenwidth(),
    y=root.winfo_screenheight()
  ))

  init_styles(root)
  init_endpoints(root)
  build_main_endpoint()

  root.mainloop()
  db.save()


def init_styles(root: Tk):
  root.configure(background=COLOR_YELLOW)
  root.title("RepeatShit.IO")
  root.option_add('*TCombobox*Listbox.background', COLOR_YELLOW)
  root.option_add('*TCombobox*Listbox.selectBackground', COLOR_BROWN)
  root.option_add('*TCombobox*Listbox.font', ("JetBrainsMonoRoman Regular", 24 * -1))

  ttk.Style(root).configure("LangPicker.TCombobox", font=(
    "JetBrainsMonoRoman Regular", 24 * -1), background='green', foreground='white')


if __name__ == "__main__":
  main()
