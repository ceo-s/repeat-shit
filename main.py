from tkinter import Tk

import tkinter as tk

from src.colors import *
import src.frames as frames


def main() -> None:
  root = Tk()
  root.attributes('-fullscreen', True)

  root.configure(background=COLOR_YELLOW)
  root.title("RepeatShit.IO")

  frame_configurate_exercise = frames.FrameTranslate(root)
  frame_configurate_exercise.pack()
  frame_main_menu = frames.FrameLibrary(root)
  frame_main_menu.pack()

  root.mainloop()


if __name__ == "__main__":
  main()
