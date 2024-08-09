from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Button, Entry

from src.widgets import LanguagePicker
from src.gallery import Gallery


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / \
  Path(r"/home/alex/projects/repeat_shit/assets/library")


def relative_to_assets(path: str) -> Path:
  return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1000x1200")
window.configure(bg="#F0DBAF")


FRAME_GALLERY = Gallery(ASSETS_PATH)


canvas = Canvas(
    window,
    bg="#F0DBAF",
    height=800,
    width=1000,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)

image_1 = canvas.create_image(
    500.0,
    84.0,
    image=FRAME_GALLERY["image_1.png"]
)


button_1 = Button(
    image=FRAME_GALLERY["button_2.png"],
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=124.0,
    y=473.0,
    width=226.0,
    height=280.0
)


button_2 = Button(
    image=FRAME_GALLERY["button_2.png"],
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=387.0,
    y=158.0,
    width=226.0,
    height=280.0
)


button_3 = Button(
    image=FRAME_GALLERY["button_2.png"],
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=650.0,
    y=158.0,
    width=226.0,
    height=280.0
)


button_4 = Button(
    image=FRAME_GALLERY["button_2.png"],
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=387.0,
    y=473.0,
    width=226.0,
    height=280.0
)

button_5 = Button(
    image=FRAME_GALLERY["button_1.png"],
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat"
)
button_5.place(
    x=124.0,
    y=158.0,
    width=226.0,
    height=280.0
)

button_6 = Button(
    image=FRAME_GALLERY["button_3.png"],
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_6 clicked"),
    relief="flat"
)
button_6.place(
    x=20.0,
    y=60.0,
    width=44.0,
    height=44.0
)
window.resizable(False, False)
window.mainloop()
