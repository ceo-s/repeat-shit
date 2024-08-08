
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / \
  Path(r"/home/alex/projects/repeat_shit/build/assets/frame2")


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
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    350.0,
    84.0,
    image=image_image_1
)

canvas.create_text(
    252.0,
    202.0,
    anchor="nw",
    text="abundance",
    fill="#000000",
    font=("JetBrainsMonoRoman ExtraBold", 36 * -1)
)

canvas.create_text(
    311.0,
    146.0,
    anchor="nw",
    text="1/48",
    fill="#464646",
    font=("JetBrainsMonoRoman Regular", 32 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    352.5,
    323.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#DECBA3",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=120.0,
    y=299.0,
    width=465.0,
    height=47.0
)

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
    x=20.0,
    y=60.0,
    width=44.0,
    height=44.0
)
window.resizable(False, False)
window.mainloop()
