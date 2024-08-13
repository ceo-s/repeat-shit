
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

  style = ttk.Style(root)
  style.configure("LangPicker.TCombobox",
                  font=("JetBrainsMonoRoman Regular", 24 * -1),
                  background='green',
                  foreground='white',
                  )

  style.configure("Treeview.Heading",
                  font=('JetBrainsMonoRoman ', 28, 'bold'),
                  padding=(10, 10),
                  background=COLOR_BROWN,
                  relief="flat",
                  )

  style.configure("Treeview",
                  highlightthickness=0,
                  bd=0,
                  rowheight=34,
                  font=('JetBrainsMonoRoman Regular', 15),
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
