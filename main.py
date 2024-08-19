
# from tkinter import CTk
from customtkinter import CTk

import tkinter as tk
from tkinter import ttk


from src.consts import *
from src.db import Database
from src.endpoints import init_endpoints, build_main_endpoint


def main() -> None:
  db = Database("db")
  root = CTk(fg_color=COLOR_YELLOW)
  root.geometry("{x}x{y}".format(
    x=root.winfo_screenwidth(),
    y=root.winfo_screenheight()
  ))
  root.resizable(False, False)

  init_styles(root)
  init_endpoints(root)
  build_main_endpoint()

  root.mainloop()
  db.save()


def init_styles(root: CTk):
  root.configure(background=COLOR_YELLOW)
  root.title("RepeatShit.IO")
  root.option_add('*TCombobox*Listbox.background', COLOR_YELLOW)
  root.option_add('*TCombobox*Listbox.selectBackground', COLOR_BROWN)
  root.option_add('*TCombobox*Listbox.font', FONT(24))

  style = ttk.Style(root)
  style.configure("LangPicker.TCombobox",
                  font=FONT(24),
                  background='green',
                  foreground='white',
                  )

  style.configure("Treeview.Heading",
                  font=FONT(28, weight=FONT_WEIGHT_BOLD),
                  padding=(10, 10),
                  background=COLOR_BROWN,
                  relief="flat",
                  )

  style.configure("Treeview",
                  highlightthickness=0,
                  bd=0,
                  rowheight=34,
                  font=FONT(15),
                  background=COLOR_BROWN,
                  foreground=COLOR_GRAY,
                  )
  style.map("Treeview",
            background=[("selected", COLOR_YELLOW)],
            foreground=[("selected", COLOR_BLACK)],
            )
  style.map("Treeview.Heading",
            background=[("active", COLOR_BROWN)],
            foreground=[("active", COLOR_GRAY)],
            )
  style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])


if __name__ == "__main__":
  main()
