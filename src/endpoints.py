from src.colors import *
from src.gallery import Gallery
from tkinter import Canvas, Button, Entry
from typing import Any, Type
from abc import ABC, abstractmethod

import tkinter as tk
import customtkinter as ctk

from src.widgets import LanguagePicker, VocabularyTable, WordCountSlider, ExerciseWidget
from src.gallery import Gallery
from src.db import Database
from src.vocabulary import Vocabulary, Word, Translation, Language


def init_endpoints(root: tk.Tk):
  BaseEndpoint.PARENT = root
  BaseEndpoint.SHARED_GALLERY = Gallery("assets/shared")
  EndpointMainMenu.init()
  EndpointConfigurateExercise.init()
  EndpointSolve.init()
  EndpointVocabulary.init()


def build_main_endpoint():
  # EndpointMainMenu.enter()
  EndpointConfigurateExercise.enter()


class BaseEndpoint(ABC):
  PARENT: tk.Tk
  SHARED_GALLERY: Gallery
  GALLERY: Gallery
  canvas: Canvas

  @classmethod
  @abstractmethod
  def init(cls):
    ...

  @classmethod
  @abstractmethod
  def enter(cls):
    ...

  @classmethod
  def leave(cls):
    cls.canvas.place_forget()


class EndpointMainMenu(BaseEndpoint):

  @classmethod
  def init(cls):
    cls.GALLERY = Gallery("assets/main_menu")
    cls.canvas = Canvas(
        cls.PARENT,
        bg="#F0DBAF",
        height=500,
        width=700,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    cls.button_exercise = Button(
        cls.canvas,
        image=cls.GALLERY["button_1.png"],
        borderwidth=0,
        highlightthickness=0,
        command=lambda: cls.leave() or EndpointConfigurateExercise.enter(),
        relief="flat"
    )

    cls.button_read = Button(
        cls.canvas,
        image=cls.GALLERY["button_4.png"],
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_read clicked"),
        relief="flat"
    )

    cls.button_translate = Button(
        cls.canvas,
        image=cls.GALLERY["button_3.png"],
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_translate clicked"),
        relief="flat"
    )

    cls.button_vocabulary = Button(
        cls.canvas,
        image=cls.GALLERY["button_2.png"],
        borderwidth=0,
        highlightthickness=0,
        command=lambda: cls.leave() or EndpointVocabulary.enter(),
        relief="flat"
    )

  @classmethod
  def enter(cls):
    cls.canvas.place(anchor='center', relx=.5, rely=.5)

    image_1 = cls.canvas.create_image(
        349.0,
        78.0,
        image=cls.GALLERY["image_1.png"]
    )

    cls.button_exercise.place(
        x=216.0,
        y=159.0,
        width=268.0,
        height=64.0
    )

    cls.button_read.place(
        x=216.0,
        y=239.0,
        width=268.0,
        height=64.0
    )

    cls.button_translate.place(
        x=216.0,
        y=319.0,
        width=268.0,
        height=64.0
    )

    cls.button_vocabulary.place(
        x=216.0,
        y=399.0,
        width=268.0,
        height=64.0
    )


class EndpointConfigurateExercise(BaseEndpoint):

  @classmethod
  def init(cls):
    cls.GALLERY = Gallery("assets/configurate_exercise")
    cls.canvas = Canvas(
        cls.PARENT,
        bg="#F0DBAF",
        height=560,
        width=700,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    cls.start_button = Button(
        cls.canvas,
        image=cls.GALLERY["button_1.png"],
        borderwidth=0,
        highlightthickness=0,
        command=cls.start_exercise,
        relief="flat"
    )

    cls.lang_picker = LanguagePicker(cls.canvas)
    cls.word_count_slider = WordCountSlider(cls.canvas)

    cls.add_new_word_variable = ctk.IntVar(value=0)
    cls.add_new_word_checkbox = ctk.CTkCheckBox(cls.canvas, 200, 60,
                                                text="Add new random words",
                                                text_color=COLOR_PINK1,
                                                font=("JetBrainsMonoRoman ExtraBold", 22 * -1),
                                                variable=cls.add_new_word_variable,
                                                onvalue=1,
                                                offvalue=0,
                                                checkbox_width=40, checkbox_height=40,
                                                corner_radius=10,
                                                border_width=3,
                                                bg_color=COLOR_YELLOW,
                                                fg_color=COLOR_PINK1,
                                                hover_color=COLOR_PINK3,
                                                border_color=COLOR_PINK1)

    cls.button_back = Button(cls.canvas,
                             image=cls.SHARED_GALLERY["button_back.png"],
                             borderwidth=0,
                             highlightthickness=0,
                             command=lambda: cls.leave() or EndpointMainMenu.enter(),
                             relief="flat"
                             )

  @classmethod
  def enter(cls) -> None:
    cls.canvas.place(anchor='center', relx=.5, rely=.5)

    cls.lang_picker.place(anchor="center", relx=.5, rely=.33)
    cls.lang_picker.add_callback(cls.__set_word_count_at_lang_change)
    cls.lang_picker.build()
    cls.word_count_slider.place(anchor="center", relx=.5, rely=.58)
    cls.__set_word_count_at_lang_change("")
    cls.word_count_slider.build()

    image_1 = cls.canvas.create_image(
        350.0,
        84.0,
        image=cls.GALLERY["image_1.png"]
    )

    cls.add_new_word_checkbox.place(anchor="center", relx=.5, rely=.75)

    cls.start_button.place(anchor="center", relx=.5, rely=.9)

    cls.button_back.place(
        x=20.0,
        y=60.0,
        width=44.0,
        height=44.0
    )

  @classmethod
  def leave(cls):
    cls.word_count_slider.delete("all")
    super().leave()

  @classmethod
  def start_exercise(cls):
    print("Starting exercise!")
    cls.leave()
    lang_from, lang_to = cls.lang_picker.get_lang_pair()
    word_count = cls.word_count_slider.get()
    new_words = bool(cls.add_new_word_variable.get())

    EndpointSolve.initialize_exercise(Database().vocabulary.get(Language(lang_from)), Language(lang_to))
    EndpointSolve.enter()

  @classmethod
  def __set_word_count_at_lang_change(cls, _: str):
    lang_from, lang_to = cls.lang_picker.get_lang_pair()
    count = 0
    for word in Database().vocabulary.get(lang_from):
      count += len(word.translations[lang_to])
    cls.word_count_slider.set_max(count)


class EndpointSolve(BaseEndpoint):
  @classmethod
  def init(cls):
    cls.GALLERY = Gallery("assets/solve")

    cls.canvas = Canvas(
        cls.PARENT,
        bg=COLOR_YELLOW,
        height=550,
        width=800,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    cls.button_back = Button(
        cls.canvas,
        image=cls.SHARED_GALLERY["button_back.png"],
        borderwidth=0,
        highlightthickness=0,
        command=lambda: cls.leave() or EndpointConfigurateExercise.enter(),
        relief="flat"
    )

    cls.exercise_widget = ExerciseWidget(cls.canvas)

  @classmethod
  def enter(cls):
    cls.canvas.place(anchor='center', relx=.5, rely=.5)

    image_1 = cls.canvas.create_image(
        350.0,
        84.0,
        image=cls.GALLERY["image_1.png"]
    )

    entry_bg_1 = cls.canvas.create_image(
        352.5,
        323.5,
        image=cls.GALLERY["entry_1.png"]
    )

    cls.button_back.place(
        x=20.0,
        y=60.0,
        width=44.0,
        height=44.0
    )

    cls.exercise_widget.place(anchor="s", relx=.5, rely=1)
    cls.exercise_widget.build()

  @classmethod
  def initialize_exercise(cls, words: list[Word], lang_to: Language):
    cls.exercise_widget.initialize_exercise(words, lang_to)


class EndpointVocabulary(BaseEndpoint):
  @classmethod
  def init(cls):
    cls.GALLERY = Gallery("assets/vocabulary")
    cls.canvas = Canvas(
        cls.PARENT,
        bg="#F0DBAF",
        height=800,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    cls.button_add_word = Button(
        cls.canvas,
        image=cls.GALLERY["button_1.png"],
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_add_word clicked"),
        relief="flat"
    )

    cls.button_import = Button(
        cls.canvas,
        image=cls.GALLERY["button_2.png"],
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_import clicked"),
        relief="flat"
    )

    cls.button_back = Button(
        cls.canvas,
        image=cls.SHARED_GALLERY["button_back.png"],
        borderwidth=0,
        highlightthickness=0,
        command=lambda: cls.leave() or EndpointMainMenu.enter(),
        relief="flat"
    )
    # cls.language_picker = LanguagePicker(cls.canvas)
    cls.vocabulary_widget = VocabularyTable(cls.canvas)

  @classmethod
  def enter(cls):
    cls.canvas.place(anchor='center', relx=.5, rely=.5)

    cls.vocabulary_widget.build()

    image_1 = cls.canvas.create_image(
        500.0,
        84.0,
        image=cls.GALLERY["image_1.png"]
    )

    cls.button_add_word.place(
        x=50.0,
        y=703.0,
        width=435.0,
        height=64.0
    )

    cls.button_import.place(
        x=515.0,
        y=703.0,
        width=435.0,
        height=64.0
    )

    cls.canvas.create_rectangle(
        257.0,
        140.0,
        743.0,
        180.0,
        fill="#000000",
        outline="")

    cls.button_back.place(
        x=20.0,
        y=60.0,
        width=44.0,
        height=44.0
    )

    cls.vocabulary_widget.place(x=50, y=224, anchor='nw')
