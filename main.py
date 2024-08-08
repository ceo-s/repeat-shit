from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

from src.widgets import LanguagePicker


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / \
  Path(r"/home/alex/projects/repeat_shit/build/assets/frame1")


def relative_to_assets(path: str) -> Path:
  return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("700x500")
window.configure(bg="#F0DBAF")


canvas = Canvas(
    window,
    bg="#F0DBAF",
    height=500,
    width=700,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
canvas.create_rectangle(
    107.0,
    138.0,
    593.0,
    178.0,
    fill="#000ff0",
    outline="")


button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=216.0,
    y=393.0,
    width=268.0,
    height=64.0
)


lang_picker = LanguagePicker(canvas, button_image_1)
lang_picker.place(x=107, y=138)

canvas.create_rectangle(
    223.0,
    208.0,
    476.0,
    291.0,
    fill="#000000",
    outline="")

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    350.0,
    84.0,
    image=image_image_1
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=208.0,
    y=327.0,
    width=30.0,
    height=30.0
)

canvas.create_text(
    250.0,
    329.0,
    anchor="nw",
    text="Add new random words",
    fill="#DC8686",
    font=("JetBrainsMonoRoman ExtraBold", 20 * -1)
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=20.0,
    y=60.0,
    width=44.0,
    height=44.0
)
window.resizable(False, False)
window.mainloop()
