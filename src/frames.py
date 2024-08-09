from src.colors import *
from src.gallery import Gallery
from tkinter import Canvas, Button, Entry
from typing import Any
from os import PathLike
from abc import ABC, abstractmethod

import tkinter as tk

from src.widgets import LanguagePicker
from src.gallery import Gallery


class ExtendedFrame(ABC, tk.Frame):
  def __init__(self, parent: tk.Misc, gallery_path: str | PathLike, **kwargs: Any) -> None:
    super().__init__(parent, **kwargs)
    self._parent = parent
    self._gallery = Gallery(gallery_path)
    self._build_frame()

  def place_at_center(self) -> None:
    self.place(anchor="center", relx=.5, rely=.5)

  @abstractmethod
  def _build_frame(self):
    ...


class FrameMainMenu(ExtendedFrame):
  def __init__(self, parent: tk.Misc):
    super().__init__(parent, "assets/main_menu")
    self.configure(width=700, height=500, bg=COLOR_YELLOW)

  def _build_frame(self):
    canvas = Canvas(
        self,
        bg="#F0DBAF",
        height=500,
        width=700,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    image_1 = canvas.create_image(
        349.0,
        78.0,
        image=self._gallery["image_1.png"]
    )

    button_1 = Button(
        self,
        image=self._gallery["button_1.png"],
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_1 clicked"),
        relief="flat"
    )
    button_1.place(
        x=216.0,
        y=159.0,
        width=268.0,
        height=64.0
    )

    button_2 = Button(
        self,
        image=self._gallery["button_2.png"],
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_2 clicked"),
        relief="flat"
    )
    button_2.place(
        x=216.0,
        y=399.0,
        width=268.0,
        height=64.0
    )

    button_3 = Button(
        self,
        image=self._gallery["button_3.png"],
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_3 clicked"),
        relief="flat"
    )
    button_3.place(
        x=216.0,
        y=319.0,
        width=268.0,
        height=64.0
    )

    button_4 = Button(
        self,
        image=self._gallery["button_4.png"],
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_4 clicked"),
        relief="flat"
    )
    button_4.place(
        x=216.0,
        y=239.0,
        width=268.0,
        height=64.0
    )


class FrameConfigurateExercise(ExtendedFrame):
  def __init__(self, parent: tk.Misc):
    super().__init__(parent, "assets/configurate_exercise")
    self.configure(width=700, height=500, bg=COLOR_YELLOW)

  def _build_frame(self) -> None:

    canvas = Canvas(
        self,
        bg="#F0DBAF",
        height=500,
        width=700,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)

    button_1 = Button(
        self,
        image=self._gallery["button_1.png"],
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

    lang_picker = LanguagePicker(canvas, self._gallery["button_1.png"])
    lang_picker.place(x=107, y=138)

    canvas.create_rectangle(
        223.0,
        208.0,
        476.0,
        291.0,
        fill="#000000",
        outline="")

    image_1 = canvas.create_image(
        350.0,
        84.0,
        image=self._gallery["image_1.png"]
    )

    button_2 = Button(
        self,
        image=self._gallery["button_2.png"],
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

    button_3 = Button(
        self,
        image=self._gallery["button_3.png"],
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


class FrameSolve(ExtendedFrame):
  def __init__(self, parent: tk.Misc):
    super().__init__(parent, "assets/solve")
    self.configure(width=700, height=500, bg=COLOR_YELLOW)

  def _build_frame(self):

    canvas = Canvas(
        self,
        bg="#F0DBAF",
        height=500,
        width=700,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)

    image_1 = canvas.create_image(
        350.0,
        84.0,
        image=self._gallery["image_1.png"]
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

    entry_bg_1 = canvas.create_image(
        352.5,
        323.5,
        image=self._gallery["entry_1.png"]
    )
    entry_1 = Entry(
        self,
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

    button_1 = Button(
        self,
        image=self._gallery["button_1.png"],
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

    button_2 = Button(
        self,
        image=self._gallery["button_2.png"],
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


class FrameTranslate(ExtendedFrame):
  def __init__(self, parent: tk.Misc):
    super().__init__(parent, "assets/translate")
    self.configure(width=1000, height=500, bg=COLOR_YELLOW)

  def _build_frame(self):
    canvas = Canvas(
        self,
        bg="#F0DBAF",
        height=500,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    image_1 = canvas.create_image(
        499.0,
        84.0,
        image=self._gallery["image_1.png"]
    )

    entry_bg_1 = canvas.create_image(
        500.0,
        240.0,
        image=self._gallery["entry_1.png"]
    )
    entry_1 = Entry(
        self,
        bd=0,
        bg="#DECBA3",
        fg="#000716",
        highlightthickness=0
    )
    entry_1.place(
        x=20.0,
        y=210.0,
        width=960.0,
        height=58.0
    )

    canvas.create_text(
        31.0,
        292.0,
        anchor="nw",
        text="translation1",
        fill="#000000",
        font=("JetBrainsMonoRoman Regular", 20 * -1)
    )

    canvas.create_text(
        31.0,
        330.0,
        anchor="nw",
        text="translation2",
        fill="#000000",
        font=("JetBrainsMonoRoman Regular", 20 * -1)
    )

    button_1 = Button(
        self,
        image=self._gallery["button_1.png"],
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_1 clicked"),
        relief="flat"
    )
    button_1.place(
        x=184.0,
        y=292.0,
        width=26.0,
        height=26.0
    )

    button_2 = Button(
        self,
        image=self._gallery["button_2.png"],
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_2 clicked"),
        relief="flat"
    )
    button_2.place(
        x=184.0,
        y=330.0,
        width=26.0,
        height=26.0
    )

    canvas.create_rectangle(
        257.0,
        140.0,
        743.0,
        180.0,
        fill="#000000",
        outline="")

    button_3 = Button(
        self,
        image=self._gallery["button_3.png"],
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


class FrameVocabulary(ExtendedFrame):
  def __init__(self, parent: tk.Misc):
    super().__init__(parent, "assets/vocabulary")
    self.configure(width=1000, height=800, bg=COLOR_YELLOW)

  def _build_frame(self):
    canvas = Canvas(
        self,
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
        image=self._gallery["image_1.png"]
    )

    canvas.create_rectangle(
        50.0,
        224.0,
        950.0,
        684.0,
        fill="#DECAA2",
        outline="")

    canvas.create_text(
        723.0,
        245.0,
        anchor="nw",
        text="Accuracy:",
        fill="#000000",
        font=("JetBrainsMonoRoman Regular", 24 * -1)
    )

    button_1 = Button(
        self,
        image=self._gallery["button_1.png"],
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_1 clicked"),
        relief="flat"
    )
    button_1.place(
        x=50.0,
        y=703.0,
        width=435.0,
        height=64.0
    )

    button_2 = Button(
        self,
        image=self._gallery["button_2.png"],
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_2 clicked"),
        relief="flat"
    )
    button_2.place(
        x=515.0,
        y=703.0,
        width=435.0,
        height=64.0
    )

    canvas.create_text(
        84.0,
        245.0,
        anchor="nw",
        text="Word:",
        fill="#000000",
        font=("JetBrainsMonoRoman Regular", 24 * -1)
    )

    canvas.create_text(
        340.0,
        245.0,
        anchor="nw",
        text="Translation:",
        fill="#000000",
        font=("JetBrainsMonoRoman Regular", 24 * -1)
    )

    canvas.create_rectangle(
        74.0,
        294.0,
        925.0,
        295.0,
        fill="#000000",
        outline="")

    canvas.create_rectangle(
        257.0,
        140.0,
        743.0,
        180.0,
        fill="#000000",
        outline="")

    button_3 = Button(
        self,
        image=self._gallery["button_3.png"],
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


class FrameReader(ExtendedFrame):
  def __init__(self, parent: tk.Misc):
    super().__init__(parent, "assets/reader")
    self.configure(width=1000, height=800, bg=COLOR_YELLOW)

  def _build_frame(self):
    canvas = Canvas(
        self,
        bg="#F0DBAF",
        height=1200,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    image_1 = canvas.create_image(
        500.0,
        84.0,
        image=self._gallery["image_1.png"]
    )

    canvas.create_text(
        100.0,
        164.0,
        anchor="nw",
        text="Fusce sivel sit amet nunc. Aenean eu eros lectus. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean vitae varius risus. In auctor lacus nisi, ut lobortis diam volutpat sit amet. Sed consectetur, nibh eu euismod vulputate, lacus eros congue orci, non molestie purus ex ut justo. Ut aliquet lorem ultrices, cursus sem eget, interdum turpis.\nInteger vulputate fringilla dui maximus ornare. Cras nisl quam, tincidunt sit amet nisl ut, interdum bibendum leo. Sed tincidunt mattis nulla quis facilisis. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Proin tincidunt porta leo, at volutpat nulla imperdiet fringilla. Etiam a mollis tellus, quis malesuada ex. Integer vitae enim tempus, dapibus eros sit amet, accumsan sapien. Sed scelerisque turpis sit amet sagittis lacinia. Suspendisse fringilla egestas tempor. Suspendisse bibendum, elit vitae laoreet vulputate, tellus nisi ullamcorper erat, laoreet rhoncus tellus mi non justo. Aenean sollicitudin sed turpis a scelerisque. In pellentesque neque vitae nibh aliquam, ac mollis elit dignissim. Maecenas dictum lorem nec ante tincidunt, et rhoncus ligula varius.\nCras dolor purus, egestas vel vestibulum viverra, volutpat quis diam. Mauris tristique libero tempor quam dapibus, pulvinar egestas felis luctus. Morbi odio lectus, iaculis ut justo ac, accumsan vehicula neque. Cras libero turpis, imperdiet id volutpat vitae, vulputate nec ipsum. In luctus, ante non feugiat malesuada, metus orci sagittis justo, sit amet ornare quam dui et dolor. Proin hendrerit dui ante, vel auctor tellus luctus vel. Sed a venenatis turpis. Etiam id enim orci.\n",
        fill="#000000",
        font=("Noto Sans", 22 * -1)
    )

    button_1 = Button(
        self,
        image=self._gallery["button_1.png"],
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_1 clicked"),
        relief="flat"
    )
    button_1.place(
        x=934.0,
        y=60.0,
        width=44.0,
        height=44.0
    )

    button_2 = Button(
        self,
        image=self._gallery["button_2.png"],
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


class FrameLibrary(ExtendedFrame):
  def __init__(self, parent: tk.Misc):
    super().__init__(parent, "assets/library")
    self.configure(width=1000, height=800, bg=COLOR_YELLOW)

  def _build_frame(self):
    canvas = Canvas(
        self,
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
        image=self._gallery["image_1.png"]
    )

    button_1 = Button(
        self,
        image=self._gallery["button_2.png"],
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
        self,
        image=self._gallery["button_2.png"],
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
        self,
        image=self._gallery["button_2.png"],
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
        self,
        image=self._gallery["button_2.png"],
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
        self,
        image=self._gallery["button_1.png"],
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
        self,
        image=self._gallery["button_3.png"],
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
