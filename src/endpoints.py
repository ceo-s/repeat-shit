from src.consts import *
from src.gallery import Gallery
from tkinter import ttk, Canvas, Button, Entry
from tkinter.filedialog import askopenfilename
from typing import Literal
from abc import ABC, abstractmethod
from PIL import Image, ImageTk
from functools import partial

import tkinter as tk
import customtkinter as ctk

from src.widgets import LanguagePicker, WordCountSlider, ExerciseWidget
from src.widgets import TranslatorWidget, ReaderConfigurationWidget
from src.widgets import ImportFromFilePopUP, AddNewWordPopUp
from src.gallery import Gallery
from src.db import Database
from src.vocabulary import Word, Language
from src.library import Book
from src.misc import add_scroll_linux, debounce
from src.translator import Translator


def init_endpoints(root: ctk.CTk):
  BaseEndpoint.PARENT = root
  BaseEndpoint.SHARED_GALLERY = Gallery("assets/shared")
  for c in BaseEndpoint.__subclasses__():
    c.init()


def build_main_endpoint():
  EndpointMainMenu.enter()


class BaseEndpoint(ABC):
  PARENT: ctk.CTk
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
    cls.canvas.delete("all")


class EndpointMainMenu(BaseEndpoint):

  @classmethod
  def init(cls):
    cls.GALLERY = Gallery("assets/main_menu")
    cls.canvas = Canvas(
        cls.PARENT,
        bg=COLOR_YELLOW,
        height=500,
        width=700,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    cls.canvas.pack_propagate(False)

    cls.button_exercise = Button(
        cls.canvas,
        image=cls.GALLERY["button_1.png"],
        background=COLOR_YELLOW,
        activebackground=COLOR_PINK,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: cls.leave() or EndpointConfigurateExercise.enter(),
        relief="flat"
    )

    cls.button_read = Button(
        cls.canvas,
        image=cls.GALLERY["button_4.png"],
        background=COLOR_YELLOW,
        activebackground=COLOR_PINK,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: cls.leave() or EndpointLibrary.enter(),
        relief="flat"
    )

    cls.button_translate = Button(
        cls.canvas,
        image=cls.GALLERY["button_3.png"],
        background=COLOR_YELLOW,
        activebackground=COLOR_PINK,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: cls.leave() or EndpointTranslator.enter(),
        relief="flat"
    )

    cls.button_vocabulary = Button(
        cls.canvas,
        image=cls.GALLERY["button_2.png"],
        background=COLOR_YELLOW,
        activebackground=COLOR_PINK,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: cls.leave() or EndpointVocabulary.enter(),
        relief="flat"
    )
    cls.button_exercise.pack(side=tk.TOP, pady=(180, 0))
    cls.button_read.pack(side=tk.TOP, pady=(5, 0))
    cls.button_translate.pack(pady=(5, 0))
    cls.button_vocabulary.pack(pady=(5, 0))

  @classmethod
  def enter(cls):
    cls.canvas.place(anchor='center', relx=.5, rely=.5)

    image_1 = cls.canvas.create_image(
        349.0,
        78.0,
        image=cls.GALLERY["image_1.png"]
    )


class EndpointConfigurateExercise(BaseEndpoint):

  @classmethod
  def init(cls):
    cls.GALLERY = Gallery("assets/configurate_exercise")
    cls.canvas = Canvas(
        cls.PARENT,
        bg=COLOR_YELLOW,
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
                                                text_color=COLOR_PINK,
                                                font=FONT(22, weight=FONT_WEIGHT_BOLD),
                                                variable=cls.add_new_word_variable,
                                                onvalue=1,
                                                offvalue=0,
                                                checkbox_width=40, checkbox_height=40,
                                                corner_radius=10,
                                                border_width=3,
                                                bg_color=COLOR_YELLOW,
                                                fg_color=COLOR_PINK,
                                                hover_color=COLOR_PINK_LIGHT,
                                                border_color=COLOR_PINK)

    cls.button_back = Button(cls.canvas,
                             image=cls.SHARED_GALLERY["button_back.png"],
                             borderwidth=0,
                             highlightthickness=0,
                             command=lambda: cls.leave() or EndpointMainMenu.enter(),
                             relief="flat"
                             )

    cls.lang_picker.place(anchor="center", relx=.5, rely=.33)
    cls.lang_picker.bind("<<LangChange>>", lambda e: cls.__set_word_count_at_lang_change())
    cls.lang_picker.bind("<<LangSwap>>", lambda e: cls.__set_word_count_at_lang_change())
    cls.lang_picker.build()
    cls.word_count_slider.place(anchor="center", relx=.5, rely=.58)
    cls.__set_word_count_at_lang_change()
    cls.word_count_slider.build()

    cls.add_new_word_checkbox.place(anchor="center", relx=.5, rely=.75)

    cls.start_button.place(anchor="center", relx=.5, rely=.9)

    cls.button_back.place(
        x=20.0,
        y=60.0,
        width=44.0,
        height=44.0
    )

  @classmethod
  def enter(cls) -> None:
    cls.canvas.place(anchor='center', relx=.5, rely=.5)

    image_1 = cls.canvas.create_image(
        350.0,
        84.0,
        image=cls.GALLERY["image_1.png"]
    )

  @classmethod
  def leave(cls):
    cls.word_count_slider.delete("all")
    super().leave()

  @classmethod
  def start_exercise(cls):
    cls.leave()
    lang_from, lang_to = cls.lang_picker.get_lang_pair()
    word_count = cls.word_count_slider.get()
    new_words = bool(cls.add_new_word_variable.get())

    EndpointSolve.initialize_exercise(
      Database().vocabulary.get_words_to_repeat(
          word_count,
          lang_from,
          lang_to),
        Language(lang_to))

    EndpointSolve.enter()

  @classmethod
  def __set_word_count_at_lang_change(cls):
    lang_from, lang_to = cls.lang_picker.get_lang_pair()
    count = 0
    for word in Database().vocabulary.get(lang_from):
      count += bool(len(word.translations[lang_to]))
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

    cls.button_back.place(
        x=20.0,
        y=60.0,
        width=44.0,
        height=44.0
    )

    cls.exercise_widget.place(anchor="s", relx=.5, rely=1)
    cls.exercise_widget.bind("<<FinishExercise>>", cls.__go_to_results)

  @classmethod
  def enter(cls):
    cls.canvas.place(anchor='center', relx=.5, rely=.5)

    image_1 = cls.canvas.create_image(
        350.0,
        84.0,
        image=cls.GALLERY["image_1.png"]
    )

    cls.exercise_widget.build()

  @classmethod
  def initialize_exercise(cls, words: list[Word], lang_to: Language):
    cls.exercise_widget.initialize_exercise(words, lang_to)

  @classmethod
  def leave(cls):
    cls.exercise_widget.delete("all")
    super().leave()

  @classmethod
  def __go_to_results(cls, e: tk.Event):
    cls.leave()
    EndpointExerciseResult.initialize_table(*cls.exercise_widget.get_results())
    EndpointExerciseResult.enter()


class EndpointExerciseResult(BaseEndpoint):
  @classmethod
  def init(cls):
    cls.canvas = Canvas(
        cls.PARENT,
        bg=COLOR_YELLOW,
        height=1000,
        width=1200,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    cls.stats = ctk.CTkLabel(cls.canvas,
                             font=FONT(30, weight=FONT_WEIGHT_BOLD),
                             fg_color=COLOR_YELLOW,
                             text_color=COLOR_GRAY,
                             )

    cls.button_finish = ctk.CTkButton(cls.canvas,
                                      height=40,
                                      width=200,
                                      text="Finish",
                                      text_color=COLOR_WHITE,
                                      anchor="s",
                                      font=FONT(28, weight=FONT_WEIGHT_BOLD),
                                      corner_radius=4,
                                      bg_color=COLOR_YELLOW,
                                      fg_color=COLOR_BLUE,
                                      hover_color=COLOR_PINK,
                                      command=lambda: cls.leave() or EndpointMainMenu.enter())

    cls.table_container = tk.Frame(cls.canvas, height=460, width=900, background=COLOR_BLUE)
    cls.table_container.pack_propagate(False)
    cls.table = ttk.Treeview(cls.table_container,
                             columns=("word", "answer", "translation", "accuracy"),
                             selectmode="extended",
                             padding=10,
                             show="headings"
                             )

    cls.table.heading("word", text="Word")
    cls.table.heading("answer", text="Answer")
    cls.table.heading("translation", text="Translation")
    cls.table.heading("accuracy", text="%")
    cls.table.tag_configure("right", background="green")
    cls.table.tag_configure("wrong", background="red")

    cls.table_scrollbar = ctk.CTkScrollbar(
      cls.table_container,
      bg_color=COLOR_YELLOW,
      fg_color=COLOR_YELLOW,
      button_color=COLOR_BROWN,
      button_hover_color=COLOR_GRAY,
      orientation="vertical",
      command=cls.table.yview
    )

    cls.table.configure(yscrollcommand=cls.table_scrollbar.set)
    cls.stats.pack()
    cls.table_container.pack()
    cls.table_scrollbar.pack(side="right", fill=tk.Y)
    cls.table.pack(side="right", fill="both", expand=True)
    cls.button_finish.pack()

  @classmethod
  def enter(cls):
    cls.canvas.place(anchor="center", relx=.5, rely=.5)

  @classmethod
  def initialize_table(cls, words: list[Word], user_translations: list[Word]):
    cls.table.delete(*cls.table.get_children())
    lang_to = user_translations[0].language
    right_answers = 0

    for word, translation in zip(words, user_translations):
      tag: Literal["right", "wrong"] = "wrong"
      try:
        translation = Database().vocabulary.get_word(translation)
      except KeyError:
        pass

      for t in word.translations[lang_to]:
        if t.translation == translation:
          tag = "right"
          break

      right_answers += int(tag == "right")
      t.repeat(tag == "right")
      cls.table.insert('',
                       tk.END,
                       values=(
                           word.word,
                           translation.word,
                           word.get_translations_string(lang_to),
                           f"{int(100 * max([t.accuracy for t in word.translations[lang_to]]))}%"
                          ),
                       tags=(tag,)
                       )

    cls.stats.configure(True, text=f"{right_answers}/{len(words)}")


class EndpointVocabulary(BaseEndpoint):
  @classmethod
  def init(cls):
    cls.GALLERY = Gallery("assets/vocabulary")
    cls.canvas = Canvas(
        cls.PARENT,
        bg=COLOR_YELLOW,
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
        command=cls.__open_add_word_pop_up,
        relief="flat"
    )

    cls.button_import = Button(
        cls.canvas,
        image=cls.GALLERY["button_2.png"],
        borderwidth=0,
        highlightthickness=0,
        command=cls.__open_import_pop_up,
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

    cls.lang_picker = LanguagePicker(cls.canvas)
    cls.lang_picker.bind("<<LangChange>>", lambda e: cls.__update_table())
    cls.lang_picker.bind("<<LangSwap>>", lambda e: cls.__update_table())
    cls.table_container = tk.Frame(cls.canvas, height=460, width=900, background=COLOR_BLUE)
    cls.table_container.pack_propagate(False)
    cls.table = ttk.Treeview(cls.table_container,
                             columns=("word", "translation", "accuracy"),
                             selectmode="extended",
                             padding=10,
                             show="headings"
                             )

    cls.table.heading("word", text="Word")
    cls.table.heading("translation", text="Translation")
    cls.table.heading("accuracy", text="✅")
    cls.table_scrollbar = ctk.CTkScrollbar(
      cls.table_container,
      bg_color=COLOR_YELLOW,
      fg_color=COLOR_YELLOW,
      button_color=COLOR_BROWN,
      button_hover_color=COLOR_GRAY,
      orientation="vertical",
      command=cls.table.yview
    )

    cls.table.configure(yscrollcommand=cls.table_scrollbar.set)
    cls.table.bind("<<TreeviewSelect>>", cls.__handle_items_selection)

    cls.row_buttons = tk.Frame(cls.canvas, background=COLOR_YELLOW)

    cls.delete_words_button = ctk.CTkButton(cls.row_buttons, text="DEL", width=30,
                                            height=30, command=cls.__delete_words)
    cls.delete_words_button.pack(side=tk.LEFT)

    cls.table.column(0, anchor="w", width=300, minwidth=300, stretch=False)
    cls.table.column(1, anchor="w", width=500, minwidth=500, stretch=False)
    cls.table.column(2, anchor="center", width=100, minwidth=400, stretch=False)

    cls.lang_picker.build()

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

    cls.button_back.place(
        x=20.0,
        y=60.0,
        width=44.0,
        height=44.0
    )

    cls.lang_picker.place(anchor="center", relx=.5, rely=.2)
    cls.table_container.place(x=50, y=224, anchor='nw')
    cls.table_scrollbar.pack(side="right", fill=tk.Y)
    cls.table.pack(side="right", fill="both", expand=True)

  @classmethod
  def enter(cls):
    cls.canvas.place(anchor='center', relx=.5, rely=.5)

    image_1 = cls.canvas.create_image(
        500.0,
        84.0,
        image=cls.GALLERY["image_1.png"]
    )

    cls.__update_table()

  @classmethod
  def __update_table(cls):
    cls.table.delete(*cls.table.get_children())
    lang_from, lang_to = cls.lang_picker.get_lang_pair()

    for word in Database().vocabulary.get(lang_from):
      if len(word.translations[lang_to]) > 0:
        cls.table.insert('',
                         tk.END,
                         values=(
                             word.word,
                             word.get_translations_string(lang_to),
                             f"{int(100 * max([t.accuracy for t in word.translations[lang_to]]))}%"
                          )
                         )

  @classmethod
  def __open_add_word_pop_up(cls):
    cls.popup_add = AddNewWordPopUp()
    cls.popup_add.bind("<Destroy>", cls.__add_word)

  @classmethod
  def __open_import_pop_up(cls):
    cls.popup_import = ImportFromFilePopUP()
    cls.popup_import.bind("<Destroy>", cls.__import_from_file)

  @classmethod
  def __add_word(cls, e: tk.Event):
    if e.widget != e.widget.winfo_toplevel():
      return

    if (word := cls.popup_add.word) is None or (translations := cls.popup_add.translations) is None:
      return

    db = Database()
    lang_from, lang_to = cls.lang_picker.get_lang_pair()
    word = Word(word, lang_from)
    db.vocabulary.add_word(word)
    word = db.vocabulary.get_word(word)

    for translation in translations:
      translation = Word(translation, lang_to)
      db.vocabulary.add_word(translation)
      translation = db.vocabulary.get_word(translation)
      db.vocabulary.add_translation(word, translation)

    cls.table.insert('',
                     tk.END,
                     values=(
                         word.word,
                         word.get_translations_string(lang_to),
                         f"{int(100 * max([t.accuracy for t in word.translations[lang_to]]))}%"
                     )
                     )

  @classmethod
  def __import_from_file(cls, e: tk.Event):
    if e.widget != e.widget.winfo_toplevel():
      return

    if cls.popup_import.file_path is None or not cls.popup_import.file_path:
      return

    with open(cls.popup_import.file_path) as file:
      lang_from, lang_to = cls.lang_picker.get_lang_pair()

      db = Database()
      for line in file:
        word, translations = line.split("|")
        word = Word(word.strip().lower(), lang_from)
        db.vocabulary.add_word(word)
        word = db.vocabulary.get_word(word)

        translations = list(map(lambda x: Word(x.strip().lower(), lang_to), translations.split(',')))
        for translation in translations:
          db.vocabulary.add_word(translation)
          translation = db.vocabulary.get_word(translation)
          db.vocabulary.add_translation(word, translation)
        cls.__update_table()

  @classmethod
  def __handle_items_selection(cls, e: tk.Event):
    if cls.table.selection():
      cls.row_buttons.place(anchor="center", relx=.8, rely=.25)
    else:
      cls.row_buttons.place_forget()

  @classmethod
  def __delete_words(cls):
    item_ids = cls.table.selection()

    for s in cls.table.selection():
      lang_from, _ = cls.lang_picker.get_lang_pair()
      word = Word(cls.table.item(s)["values"][0], lang_from)
      word = Database().vocabulary.get_word(word)
      Database().vocabulary.delete_word(word)

    cls.table.delete(*item_ids)


class EndpointTranslator(BaseEndpoint):

  @classmethod
  def init(cls):
    cls.GALLERY = Gallery("assets/translate")
    cls.canvas = Canvas(
        cls.PARENT,
        bg=COLOR_YELLOW,
        height=800,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    cls.button_back = Button(
        cls.canvas,
        image=cls.SHARED_GALLERY["button_back.png"],
        borderwidth=0,
        highlightthickness=0,
        command=lambda: cls.leave() or EndpointMainMenu.enter(),
        relief="flat"
    )

    cls.button_back.place(
      x=20,
      y=60,
      height=44,
      width=44,
    )

    cls.translator = TranslatorWidget(cls.canvas)
    cls.translator.initialize_translator(Database().vocabulary)
    cls.translator.build()
    cls.translator.pack(pady=(160, 0))

  @classmethod
  def enter(cls):
    cls.canvas.place(anchor='center', relx=.5, rely=.5)

    image_1 = cls.canvas.create_image(
        400,
        84,
        image=cls.GALLERY["image_1.png"]
    )

  @classmethod
  def leave(cls):
    cls.translator.clear()
    super().leave()


class EndpointLibrary(BaseEndpoint):

  @classmethod
  def init(cls):
    cls.GALLERY = Gallery("assets/library")
    cls.canvas = Canvas(
        cls.PARENT,
        bg=COLOR_YELLOW,
        height=800,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    cls.canvas.pack_propagate(False)

    cls.button_back = Button(
        cls.canvas,
        image=cls.SHARED_GALLERY["button_back.png"],
        borderwidth=0,
        highlightthickness=0,
        command=lambda: cls.leave() or EndpointMainMenu.enter(),
        relief="flat"
    )

    cls.button_back.place(
      x=20,
      y=60,
      height=44,
      width=44,
    )

    cls.button_add_book = ctk.CTkButton(cls.canvas,
                                        width=200,
                                        height=60,
                                        corner_radius=12,
                                        text="Add book",
                                        font=FONT(24, weight=FONT_WEIGHT_BOLD),
                                        hover_color=COLOR_BROWN,
                                        text_color=COLOR_PINK,
                                        fg_color=COLOR_YELLOW,
                                        border_color=COLOR_PINK,
                                        border_width=3,
                                        command=cls.__import_book,
                                        )
    cls.button_add_book.pack(side=tk.TOP, pady=(120, 0))
    cls.books_container = ctk.CTkScrollableFrame(cls.canvas,
                                                 width=800,
                                                 height=560,
                                                 fg_color=COLOR_BLUE,
                                                 scrollbar_button_color=COLOR_BROWN,
                                                 scrollbar_button_hover_color=COLOR_GRAY,
                                                 )

    add_scroll_linux(cls.books_container)
    cls.books_container.columnconfigure((0, 1, 2, 3), weight=1)
    cls.books_container.pack(side=tk.TOP, pady=(20, 0))
    cls.nbooks = 0

  @classmethod
  def enter(cls):
    cls.canvas.place(anchor='center', relx=.5, rely=.5)

    image_1 = cls.canvas.create_image(
        500,
        84,
        image=cls.GALLERY["image_1.png"]
    )
    cls.__render_books()

  @classmethod
  def __render_books(cls):
    for child in list(cls.books_container.children.values()):
      child.destroy()

    cls.nbooks = 0
    for book in Database().library.books:
      cls.__place_book(book)

  @classmethod
  def __place_book(cls, book: Book):
    ri, ci = cls.nbooks // 4, cls.nbooks % 4
    cls.nbooks += 1
    book_frame = ctk.CTkFrame(cls.books_container,
                              height=282,
                              width=174,
                              bg_color=COLOR_YELLOW,
                              fg_color=COLOR_YELLOW,
                              border_width=4,
                              border_color=COLOR_PINK_DARK,
                              )
    book_frame.pack_propagate(False)
    title = book.title if len(book.title) <= 15 else book.title[:15] + "..."
    book_title_label = ctk.CTkLabel(book_frame,
                                    text=title,
                                    text_color=COLOR_GRAY,
                                    bg_color=COLOR_YELLOW,
                                    font=FONT(20),
                                    )
    book_title_label.pack(side=tk.BOTTOM, pady=(0, 4))

    onclick_callback = partial(cls.__open_book, book)

    if book.cover is not None:
      cover = book.cover
      cover = cover.resize((174, 250))
      book_cover_image = ImageTk.PhotoImage(cover)
      book_cover_label = ctk.CTkLabel(book_frame,
                                      text="",
                                      image=book_cover_image,
                                      bg_color=COLOR_YELLOW,
                                      )
      book_cover_label.pack(side=tk.BOTTOM, expand="yes")
      book_cover_label.bind("<1>", onclick_callback)

    book_frame.grid(row=ri, column=ci, pady=10)
    book_frame.bind("<1>", onclick_callback)
    book_title_label.bind("<1>", onclick_callback)

  @classmethod
  def __open_book(cls, book: Book, e: tk.Event):
    cls.leave()
    EndpointReader.initialize_reader(book)
    EndpointReader.enter()

  @classmethod
  def __import_book(cls):
    path = askopenfilename()
    Database().library.import_book(path)
    cls.__render_books()


class EndpointReader(BaseEndpoint):

  @classmethod
  def init(cls):
    cls.GALLERY = Gallery("assets/reader")
    cls.canvas = Canvas(
        cls.PARENT,
        bg=COLOR_BLUE,
        height=800,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    cls.canvas.pack_propagate(False)

    text = ""
    cls.page_container = tk.Frame(cls.canvas,
                                  width=850,
                                  height=640,
                                  )
    cls.page_container.pack_propagate(False)
    cls.page_container.pack(pady=(120, 0))
    cls.page = tk.Text(cls.page_container,
                       width=100,
                       height=42,
                       borderwidth=0,
                       selectborderwidth=0,
                       bd=0,
                       highlightthickness=0,
                       bg=COLOR_PINK_LIGHT,
                       foreground=COLOR_GRAY,
                       wrap=tk.WORD,
                       font=FONT(Database().user_configuration.reader_font_size),
                       )
    cls.page.insert(1.0, text)
    cls.page.configure(state=tk.DISABLED)
    cls.page.tag_add("all", 1.0, tk.END)
    cls.page.tag_configure("all", justify="center")
    cls.page.bind("<<Selection>>", cls.__translate_selected)
    cls.page.pack(fill="both", expand=True)

    cls.button_back = Button(
        cls.canvas,
        image=cls.SHARED_GALLERY["button_back.png"],
        borderwidth=0,
        highlightthickness=0,
        command=lambda: cls.leave() or EndpointLibrary.enter(),
        relief="flat"
    )

    cls.button_back.place(anchor="center", relx=.05, rely=.1)

    arrow_img = Image.open("assets/shared/arrow.png")
    arrow_to_left_img = arrow_img.rotate(270.)
    arrow_to_right_img = arrow_img.rotate(90.)
    cls.arrow_to_left = ImageTk.PhotoImage(arrow_to_left_img)
    cls.arrow_to_right = ImageTk.PhotoImage(arrow_to_right_img)

    cls.button_prev_page = Button(
        cls.canvas,
        image=cls.arrow_to_left,
        borderwidth=0,
        highlightthickness=0,
        command=cls.__render_prev_page,
        relief="flat",
        background=COLOR_YELLOW,
        activebackground=COLOR_YELLOW,
    )

    cls.button_next_page = Button(
        cls.canvas,
        image=cls.arrow_to_right,
        borderwidth=0,
        highlightthickness=0,
        command=cls.__render_next_page,
        relief="flat",
        background=COLOR_YELLOW,
        activebackground=COLOR_YELLOW,
    )

    cls.button_prev_page.place(anchor="center", relx=.05, rely=.5)
    cls.button_next_page.place(anchor="center", relx=.95, rely=.5)

    cls.translation_frame = ctk.CTkFrame(cls.canvas,
                                         fg_color=COLOR_BROWN,
                                         bg_color=COLOR_BROWN,
                                         width=300,
                                         )
    cls.translation_frame.pack_propagate(False)
    cls.translation_checkbox = ctk.CTkCheckBox(cls.translation_frame,
                                               text="",
                                               text_color=COLOR_BLACK,
                                               font=FONT(24),
                                               border_color=COLOR_PINK,
                                               hover_color=COLOR_PINK_LIGHT,
                                               fg_color=COLOR_PINK,
                                               text_color_disabled=COLOR_GRAY,
                                               command=cls.__on_translation_toggle,
                                               onvalue=1,
                                               offvalue=0,
                                               )
    cls.translation_checkbox.pack(pady=6)
    cls.translation_text = tk.Text(cls.translation_frame,
                                   width=40,
                                   height=10,
                                   borderwidth=0,
                                   selectborderwidth=0,
                                   bd=0,
                                   highlightthickness=0,
                                   bg=COLOR_BROWN,
                                   foreground=COLOR_GRAY,
                                   wrap=tk.WORD,
                                   font=FONT(16),
                                   )
    cls.translation_text.pack()

    cls.open_configuration_button = Button(
      cls.canvas,
        borderwidth=0,
        highlightthickness=0,
        image=cls.GALLERY["button_1.png"],
        relief="flat",
        background=COLOR_YELLOW,
        activebackground=COLOR_YELLOW,
        command=lambda: cls.configuration_widget.place(anchor="ne", relx=.98, rely=.05),
    )
    cls.open_configuration_button.place(anchor="center", relx=.95, rely=.1)

    cls.configuration_widget = ReaderConfigurationWidget(cls.canvas)
    cls.configuration_widget.initialize_configuration(
      Database().user_configuration.reader_font_size,
      Database().user_configuration.reader_lang_to,
        )
    cls.configuration_widget.build()
    cls.configuration_widget.bind("<<ConfigurationChange>>", cls.__on_conf_change)
    cls.configuration_widget.bind("<<BookDeleted>>", lambda e: cls.__delete_book())

    cls.canvas.bind("<1>", cls.__close_conf_if_clicked_outside)
    cls.button_back.bind("<1>", cls.__close_conf_if_clicked_outside)
    cls.page.bind("<1>", cls.__close_conf_if_clicked_outside)
    cls.button_prev_page.bind("<1>", cls.__close_conf_if_clicked_outside)
    cls.button_next_page.bind("<1>", cls.__close_conf_if_clicked_outside)
    cls.book: Book
    cls.page_text: str

  @classmethod
  def enter(cls):
    cls.canvas.place(anchor='center', relx=.5, rely=.5)

    image_1 = cls.canvas.create_image(
        500,
        84,
        image=cls.GALLERY["image_1.png"]
    )
    cls.__render_page()

  @classmethod
  def initialize_reader(cls, book: Book):
    cls.book = book

  @classmethod
  def __render_prev_page(cls):
    cls.book.current_page -= 1
    cls.__render_page()

  @classmethod
  def __render_next_page(cls):
    cls.book.current_page += 1
    cls.__render_page()

  @classmethod
  def __render_page(cls):
    cls.page.configure(state="normal")
    cls.page.delete(1.0, tk.END)
    cls.page.insert(tk.END, cls.book.get_curr_page())
    cls.page.configure(state="disabled")

  @classmethod
  def __translate_selected(cls, e: tk.Event):
    if not cls.page.tag_ranges(tk.SEL):
      cls.translation_frame.place_forget()
      return
    cls.__perform_translation()

  @classmethod
  @debounce(1)
  def __perform_translation(cls):
    selection = cls.page.get(tk.SEL_FIRST, tk.SEL_LAST)
    translation = Translator.translate_with_google(selection.lower().strip(),
                                                   None,
                                                   cls.configuration_widget.conf_lang_to.short)
    cls.__display_translation(translation.strip().lower())

  @classmethod
  def __display_translation(cls, translation: str):
    translation_word = Word(translation, cls.configuration_widget.conf_lang_to)
    try:
      translation_word = Database().vocabulary.get_word(translation_word)
      cls.translation_checkbox.select()
      cls.translation_checkbox.configure(True, state=tk.DISABLED, text="Already in vocabulary")
    except KeyError:
      cls.translation_checkbox.deselect()
      cls.translation_checkbox.configure(True, state=tk.NORMAL, text="Add to vocabulary")
    cls.translation_text.configure(state="normal")
    cls.translation_text.delete(1.0, tk.END)
    cls.translation_text.insert(tk.END, translation)
    cls.translation_text.configure(state="disabled")
    cls.translation_frame.place(anchor="center", relx=.5, rely=.5)

  @classmethod
  def __on_translation_toggle(cls):
    func = cls.__on_translation_add if cls.translation_checkbox.get() else cls.__on_translation_del
    selection = cls.page.get(tk.SEL_FIRST, tk.SEL_LAST).lower().strip()
    lang_short, confidence = Translator.detect_language(selection)
    lang_from = Language(lang_short)
    lang_to = cls.configuration_widget.conf_lang_to
    translation_text = cls.translation_text.get(1.0, tk.END).lower().strip()
    word = Word(selection, lang_from)
    translation = Word(translation_text, lang_to)

    func(word, translation)

  @classmethod
  def __on_translation_add(cls, word: Word, translation: Word):
    db = Database()
    db.vocabulary.add_word(word)

    try:
      translation = db.vocabulary.get_word(translation)
    except KeyError:
      db.vocabulary.add_word(translation)

    word = db.vocabulary.get_word(word)
    translation = db.vocabulary.get_word(translation)

    db.vocabulary.add_translation(word, translation)
    cls.translation_checkbox.configure(True, text="Delete from vocabulary")

  @classmethod
  def __on_translation_del(cls, word: Word, translation: Word):
    db = Database()
    try:
      word = db.vocabulary.get_word(word)
      translation = db.vocabulary.get_word(translation)
    except KeyError:
      print("That should not happen, but still...")
      return

    db.vocabulary.delete_word(translation)
    cls.translation_checkbox.configure(True, text="Add to vocabulary")

  @classmethod
  def __on_conf_change(cls, e: tk.Event):
    cls.page.configure(font=FONT(cls.configuration_widget.conf_font_size))
    Database().user_configuration.reader_font_size = cls.configuration_widget.conf_font_size
    Database().user_configuration.reader_lang_to = cls.configuration_widget.conf_lang_to

  @classmethod
  def __close_conf_if_clicked_outside(cls, e: tk.Event):
    cls.configuration_widget.place_forget()

  @classmethod
  def __delete_book(cls):
    Database().library.delete_book(cls.book)
    cls.leave()
    EndpointLibrary.enter()
