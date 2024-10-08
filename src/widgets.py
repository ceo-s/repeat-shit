from tkinter import ttk
from tkinter.filedialog import askopenfilename
from abc import abstractmethod, ABC
from os import PathLike
from typing import Iterable
from functools import partial

import tkinter as tk
import customtkinter as ctk

from src.consts import *
from src.gallery import Gallery
from src.vocabulary import Word, Language, Vocabulary, LANGUAGES_FULL
from src.scrollable_dropdown import CTkScrollableDropdown
from src.translator import Translator
from src.misc import add_scroll_linux, debounce


class BaseWidget(tk.Canvas, ABC):
  def __init__(self, parent: tk.Canvas):
    super().__init__(parent)
    self.parent = parent
    self.pack_propagate(False)
    self.init()

  @abstractmethod
  def init(self):
    ...

  @abstractmethod
  def build(self):
    ...


class BasePopUp(ctk.CTkToplevel, ABC):
  def __init__[**P](self):
    super().__init__(fg_color=COLOR_YELLOW)
    self.build()

  @abstractmethod
  def build(self):
    ...

  def destroy(self):
    super().destroy()


class LanguagePicker(BaseWidget):
  LANG_LIST = LANGUAGES_FULL

  def init(self):
    self.event_add("<<LangSwap>>", "None")
    self.event_add("<<LangChange>>", "None")
    self.pack_propagate(True)
    self.configure(height=50, width=400, background=COLOR_YELLOW, highlightthickness=0, relief='ridge')
    self.__choose_lang_from = ctk.CTkOptionMenu(self, 180, 50, 6,
                                                font=FONT(20, weight=FONT_WEIGHT_BOLD),
                                                dropdown_font=FONT(20),
                                                values=self.LANG_LIST,
                                                fg_color=COLOR_PINK,
                                                text_color=COLOR_YELLOW,
                                                dropdown_text_color=COLOR_PINK,
                                                dropdown_hover_color=COLOR_BROWN,
                                                dropdown_fg_color=COLOR_YELLOW,
                                                button_color=COLOR_PINK_DARK,
                                                button_hover_color=COLOR_PINK_DARK,
                                                )
    CTkScrollableDropdown(self.__choose_lang_from,
                          id_="from",
                          values=self.LANG_LIST,
                          command=lambda s: self.__swap_if_both_same(s) or self.__on_lang_change(),
                          button_color=COLOR_PINK,
                          text_color=COLOR_YELLOW,
                          scrollbar_button_color=COLOR_PINK_DARK,
                          fg_color=COLOR_YELLOW,
                          frame_border_width=0,
                          frame_corner_radius=40,
                          scrollbar_button_hover_color=COLOR_PINK_DARK,
                          hover_color=COLOR_PINK_DARK,
                          )

    self.__choose_lang_to = ctk.CTkOptionMenu(self, 180, 50, 6,
                                              font=FONT(20, weight=FONT_WEIGHT_BOLD),
                                              dropdown_font=FONT(20),
                                              values=self.LANG_LIST,
                                              fg_color=COLOR_PINK,
                                              text_color=COLOR_YELLOW,
                                              dropdown_text_color=COLOR_PINK,
                                              dropdown_hover_color=COLOR_BROWN,
                                              dropdown_fg_color=COLOR_YELLOW,
                                              button_color=COLOR_PINK_DARK,
                                              button_hover_color=COLOR_PINK_DARK,
                                              )

    CTkScrollableDropdown(self.__choose_lang_to,
                          id_="to",
                          values=self.LANG_LIST,
                          command=lambda s: self.__swap_if_both_same(s) or self.__on_lang_change(),
                          button_color=COLOR_PINK,
                          text_color=COLOR_YELLOW,
                          scrollbar_button_color=COLOR_PINK_DARK,
                          fg_color=COLOR_YELLOW,
                          frame_border_width=0,
                          frame_corner_radius=40,
                          scrollbar_button_hover_color=COLOR_PINK_DARK,
                          hover_color=COLOR_PINK_DARK,
                          )
    self.__choose_lang_to.set(self.LANG_LIST[1])

    self.__exchange_button = tk.Button(self,
                                       image=Gallery("assets/shared")["swap.png"],
                                       width=40,
                                       height=40,
                                       background=COLOR_YELLOW,
                                       activebackground=COLOR_BROWN,
                                       borderwidth=0,
                                       highlightthickness=0,
                                       activeforeground=COLOR_YELLOW,
                                       command=self.__swap_picker_values,
                                       relief="flat")

    self.__val_from = self.__choose_lang_from.get()
    self.__val_to = self.__choose_lang_to.get()

  def build(self):
    self.__choose_lang_from.pack(side=tk.LEFT, padx=20)
    self.__exchange_button.pack(side=tk.LEFT, padx=20)
    self.__choose_lang_to.pack(side=tk.LEFT, padx=20)

  def __swap_picker_values(self):
    from_val = self.__choose_lang_from.get()
    self.__choose_lang_from.set(self.__choose_lang_to.get())
    self.__choose_lang_to.set(from_val)
    self.__val_from = self.__choose_lang_from.get()
    self.__val_to = self.__choose_lang_to.get()
    self.__on_lang_swap()

  def get_lang_pair(self) -> tuple[Language, Language]:
    return Language(self.__choose_lang_from.get().lower().strip()), Language(self.__choose_lang_to.get().lower().strip())

  def __on_lang_change(self) -> None:
    self.event_generate("<<LangChange>>")

  def __on_lang_swap(self) -> None:
    self.event_generate("<<LangSwap>>")

  def __swap_if_both_same(self, val: str) -> None:
    id_, val = val.split(":")

    if id_ == "from":
      if self.__val_to == val:
        self.__choose_lang_to.set(self.__val_from)
        self.__val_to = self.__val_from
      self.__val_from = val

    if id_ == "to":
      if self.__val_from == val:
        self.__choose_lang_from.set(self.__val_to)
        self.__val_from = self.__val_to
      self.__val_to = val


class WordCountSlider(BaseWidget):

  def __init__(self, parent: tk.Canvas):
    super().__init__(parent)
    self.__max_value = 0
    self.__text_id: int = 0

  def init(self):
    self.configure(width=500, height=110, bg=COLOR_YELLOW, highlightthickness=0, relief='ridge')

    self.__slider = ctk.CTkSlider(self, from_=0, to=1,
                                  command=self.__update_label_value,
                                  fg_color=COLOR_PINK_LIGHT,
                                  height=30,
                                  width=360,
                                  progress_color=COLOR_BLUE,
                                  button_color=COLOR_PINK,
                                  button_hover_color=COLOR_PINK_DARK,
                                  )

    self.__label = ctk.CTkLabel(self,
                                text="",
                                text_color=COLOR_GRAY,
                                font=FONT(54, weight=FONT_WEIGHT_BOLD),
                                )

  def build(self):
    self.__label.place(anchor="center", relx=.5, rely=.24)
    self.__slider.place(anchor="center", relx=.5, rely=.7)

  def set(self, value: int | float):
    self.__slider.set(float(value))

  def get(self) -> int:
    return int(self.__slider.get())

  def set_max(self, num: int):
    if num == 0:
      self.__slider.configure(state="disabled")
      self.__slider.configure(to=1)
    else:
      self.__slider.configure(state="normal")
      self.__slider.configure(to=num)

    current = int(self.get())
    current = current if current < num else num
    self.__label.configure(text=f"{current}/{num}")
    self.__slider.set(self.get())
    self.__max_value = num

  def __update_label_value(self, value: float):
    self.__label.configure(text=f"{int(value)}/{self.__max_value}")


class ExerciseWidget(BaseWidget):

  def init(self):
    self.event_add("<<FinishExercise>>", "None")
    self.__initialized = False
    self.configure(width=800, height=400, background=COLOR_YELLOW, highlightthickness=0)
    self.__entry = ctk.CTkEntry(
        self,
        placeholder_text="Enter translation here:",
        placeholder_text_color=COLOR_GRAY,
        text_color=COLOR_GRAY,
        font=FONT(24, weight=FONT_WEIGHT_REGULAR),
        height=60,
        width=480,
        corner_radius=6,
        border_width=0,
        bg_color=COLOR_BROWN,
        fg_color=COLOR_BROWN,
    )

    self.__button_confirm = tk.Button(self,
                                      image=Gallery("assets/solve")["button_1.png"],
                                      borderwidth=0,
                                      highlightthickness=0,
                                      activebackground=COLOR_BROWN,
                                      background=COLOR_YELLOW,
                                      command=self.__handle_submit,
                                      relief="flat"
                                      )

  def build(self):
    if not self.is_initialized():
      raise Exception("ExerciseWidget should be initialized before calling build!")

    self.__word_id = self.create_text(
        400,
        150,
        anchor="center",
        text=self.__words[0].word,
        fill=COLOR_BLACK,
        font=FONT(44, weight=FONT_WEIGHT_BOLD)
    )

    self.__counter_string_id = self.create_text(
        400,
        70.0,
        anchor="center",
        text=f"{self.__i_word + 1}/{self.__n_words}",
        fill=COLOR_GRAY,
        font=FONT(38)
    )

    self.__entry.place(anchor="center", relx=.5, rely=.65)
    self.__button_confirm.place(anchor="center", relx=.5, rely=.9)

  def is_initialized(self):
    return self.__initialized

  def initialize_exercise(self, words: list[Word], language_to: Language):
    self.__words = words
    self.__language_to = language_to
    self.__n_words = len(words)
    self.__results = []
    self.__i_word = 0
    self.__initialized = True

  def get_results(self) -> tuple[list[Word], list[Word]]:
    return self.__words, self.__results

  def __handle_submit(self):
    translation = self.__entry.get()
    self.__check_translation(translation)
    self.__i_word += 1
    if self.__i_word >= self.__n_words:
      self.__initialized = False
      self.__entry.delete(0, tk.END)
      self.event_generate("<<FinishExercise>>")
      return
    self.__render_next_word()

  def __check_translation(self, translation: str):
    self.__results.append(Word(translation, self.__language_to))

  def __render_next_word(self):
    self.itemconfig(self.__word_id, text=self.__words[self.__i_word].word)
    self.itemconfig(self.__counter_string_id, text=f"{self.__i_word + 1}/{self.__n_words}")
    self.__entry.delete(0, ctk.END)


class TranslatorWidget(BaseWidget):

  def init(self):
    self.configure(width=800, height=600, background=COLOR_YELLOW, highlightthickness=0)
    self.event_add("<<TranslateComplete>>", "None")
    self.bind("<Button-1>", lambda event: event.widget.focus_set())
    self.__lang_picker = LanguagePicker(self)
    self.__lang_picker.build()
    self.__lang_picker.bind("<<LangSwap>>", lambda e: self.__translate())
    self.__lang_picker.bind("<<LangChange>>", lambda e: self.__translate())

    self.__entry_text = ""
    self.__entry = ctk.CTkEntry(self,
                                width=800,
                                height=80,
                                fg_color=COLOR_BROWN,
                                text_color=COLOR_BLACK,
                                placeholder_text="Enter word to translate",
                                placeholder_text_color=COLOR_GRAY,
                                corner_radius=2,
                                border_width=0,
                                )
    self.__translations_container = ctk.CTkScrollableFrame(self,
                                                           height=420,
                                                           width=800,
                                                           bg_color=COLOR_YELLOW,
                                                           fg_color=COLOR_YELLOW,
                                                           scrollbar_button_color=COLOR_BROWN,
                                                           scrollbar_button_hover_color=COLOR_GRAY,
                                                           )
    add_scroll_linux(self.__translations_container)
    self.__initialized = False

  def initialize_translator(self, vocabulary: Vocabulary):
    self.__initialized = True
    self.__vocabulary = vocabulary

  def build(self):
    if not self.__initialized:
      raise Exception("TranslatorWidget should be initialized before calling build!")

    self.__lang_picker.pack()
    self.__entry.pack(pady=(25, 5))
    self.__translations_container.pack()
    self.__entry.bind("<KeyRelease>", self.__handle_entry_change)

  def clear(self):
    self.__entry.delete(0, tk.END)
    self.__entry_text = ""
    self.__update_translations([])

  def __handle_entry_change(self, e: tk.Event):
    text = self.__entry.get().strip(" \n")
    if text != self.__entry_text:
      self.__entry_text = text
      self.__update_translations([])
      self.__translate()

  @debounce(.5)
  def __translate(self):
    if not self.__entry_text:
      return
    lang_from, lang_to = self.__lang_picker.get_lang_pair()
    word = Word(self.__entry_text.lower().strip(), lang_from)
    translations = []

    try:
      for t in self.__vocabulary.get_word(word).translations[lang_to]:
        translations.append(t.translation)
    except KeyError:
      pass

    translator_translations = Translator.translate(self.__entry_text.lower().strip(), lang_from.short, lang_to.short)
    for t in translator_translations[:10]:
      t_word = Word(t, lang_to)
      try:
        t_word = self.__vocabulary.get_word(Word(t, lang_to))
      except KeyError:
        pass

      if t_word not in translations:
        translations.append(t_word)

    self.__update_translations(translations)
    self.event_generate("<<TranslateComplete>>")

  def __update_translations(self, translations: Iterable[Word]):
    for child in list(self.__translations_container.children.values()):
      child.destroy()

    for translation in translations:

      checkbox = ctk.CTkCheckBox(self.__translations_container,
                                 text=translation.word,
                                 font=FONT(36),
                                 text_color=COLOR_GRAY,
                                 text_color_disabled=COLOR_GRAY,
                                 variable=tk.IntVar(value=0),
                                 onvalue=1,
                                 offvalue=0,
                                 checkbox_width=36,
                                 checkbox_height=36,
                                 corner_radius=4,
                                 fg_color=COLOR_PINK,
                                 border_color=COLOR_PINK,
                                 hover_color=COLOR_PINK_LIGHT,
                                 #  command=partial(self.__add_to_vocabulary, translation.word),
                                 )
      checkbox.bind("<1>", partial(self.__add_or_del_in_vocabulary, checkbox))

      if translation in self.__vocabulary:
        checkbox.select()

      checkbox.pack(pady=4, anchor="nw")

  def __add_or_del_in_vocabulary(self, checkbox: ctk.CTkCheckBox, e: tk.Event):
    lang_from, lang_to = self.__lang_picker.get_lang_pair()
    word = Word(self.__entry_text.lower().split(), lang_from)
    translation = Word(checkbox._text, lang_to)

    if checkbox.get() == 0:
      try:
        translation = self.__vocabulary.get_word(translation)
        self.__vocabulary.delete_word(translation)
      except KeyError:
        pass

    else:
      try:
        word = self.__vocabulary.get_word(word)
      except KeyError:
        pass

      try:
        translation = self.__vocabulary.get_word(translation)
      except KeyError:
        pass

      self.__vocabulary.add_word(word)
      word = self.__vocabulary.get_word(word)
      self.__vocabulary.add_word(translation)
      translation = self.__vocabulary.get_word(translation)
      self.__vocabulary.add_translation(word, translation)


class ReaderConfigurationWidget(BaseWidget):
  def init(self):
    self.configure(width=200, height=220, background=COLOR_YELLOW, highlightthickness=0)
    self.event_add("<<ConfigurationChange>>", "None")
    self.event_add("<<BookDeleted>>", "None")
    self.gallery = Gallery("assets/reader")
    self.__initialized = False
    self.conf_lang_to = Language.ENGLISH
    self.conf_font_size = 18

    self.__delete_book_label = ctk.CTkLabel(self,
                                            text="Delete book:",
                                            font=FONT(20),
                                            text_color=COLOR_GRAY,
                                            )
    self.__delete_book_button = ctk.CTkButton(self,
                                              width=180,
                                              height=30,
                                              corner_radius=10,
                                              text="DELETE",
                                              text_color=COLOR_PINK,
                                              fg_color=COLOR_YELLOW,
                                              bg_color=COLOR_YELLOW,
                                              hover_color=COLOR_BROWN,
                                              border_color=COLOR_PINK,
                                              border_width=3,
                                              command=lambda: self.event_generate("<<BookDeleted>>"),
                                              )
    self.__font_size_picker_label = ctk.CTkLabel(self,
                                                 text="Choose font size:",
                                                 font=FONT(20),
                                                 text_color=COLOR_GRAY,
                                                 )
    self.__font_size_picker_var = tk.StringVar(self, str(self.conf_font_size))
    self.__font_size_picker_var.trace_add("write", self.__on_fontsize_update)
    self.__font_size_picker = ctk.CTkEntry(self,
                                           width=180,
                                           height=40,
                                           font=FONT(24),
                                           corner_radius=4,
                                           text_color=COLOR_BLACK,
                                           fg_color=COLOR_YELLOW,
                                           border_color=COLOR_PINK,
                                           textvariable=self.__font_size_picker_var,
                                           )

    self.__lang_picker_label = ctk.CTkLabel(self,
                                            text="Translate to:",
                                            font=FONT(20),
                                            text_color=COLOR_GRAY,
                                            )

    self.__lang_picker = ctk.CTkOptionMenu(self, 180, 50, 6,
                                           font=FONT(20, weight=FONT_WEIGHT_BOLD),
                                           dropdown_font=FONT(20),
                                           values=LANGUAGES_FULL,
                                           fg_color=COLOR_PINK,
                                           text_color=COLOR_YELLOW,
                                           dropdown_text_color=COLOR_PINK,
                                           dropdown_hover_color=COLOR_BROWN,
                                           dropdown_fg_color=COLOR_YELLOW,
                                           button_color=COLOR_PINK_DARK,
                                           button_hover_color=COLOR_PINK_DARK,
                                           )

    CTkScrollableDropdown(self.__lang_picker,
                          id_="to",
                          values=LANGUAGES_FULL,
                          command=lambda s: self.__on_lang_change(),
                          button_color=COLOR_PINK,
                          text_color=COLOR_YELLOW,
                          scrollbar_button_color=COLOR_PINK_DARK,
                          fg_color=COLOR_YELLOW,
                          frame_border_width=0,
                          frame_corner_radius=40,
                          scrollbar_button_hover_color=COLOR_PINK_DARK,
                          hover_color=COLOR_PINK_DARK,
                          )

  def build(self):
    if not self.__initialized:
      raise Exception("ReaderConfigurationWidget should be initialized before calling build")
    self.__delete_book_label.pack(pady=(4, 0))
    self.__delete_book_button.pack()
    self.__font_size_picker_label.pack()
    self.__font_size_picker.pack()
    self.__lang_picker_label.pack()
    self.__lang_picker.pack()

  def initialize_configuration(self, font_size: int, lang_to: Language):
    self.__initialized = True
    self.conf_font_size = font_size
    self.conf_lang_to = lang_to
    self.__font_size_picker_var.set(f"{font_size}")
    self.__lang_picker.set(lang_to.full.capitalize())

  def __on_fontsize_update(self, *args):
    new_val = self.__font_size_picker_var.get()
    try:
      new_val = int(new_val)
    except ValueError:
      return
    self.conf_font_size = new_val

    self.event_generate("<<ConfigurationChange>>")

  def __on_lang_change(self):
    self.conf_lang_to = Language(self.__lang_picker.get().lower().strip())
    self.event_generate("<<ConfigurationChange>>")


class ImportFromFilePopUP(BasePopUp):

  def build(self):
    self.configure(fg_color=COLOR_YELLOW)
    self.title("Import from file")
    self.geometry("550x280")
    self.resizable(False, False)
    label = ctk.CTkLabel(self,
                         text="Notice!\nFile must contain only lines of this format:",
                         text_color=COLOR_GRAY,
                         font=FONT(24, weight=FONT_WEIGHT_BOLD),
                         )
    l_container = tk.Frame(self, background=COLOR_YELLOW)
    label1 = ctk.CTkLabel(l_container,
                          text="word",
                          text_color=COLOR_GRAY,
                          font=FONT(18, weight=FONT_WEIGHT_REGULAR),
                          )
    label2 = ctk.CTkLabel(l_container,
                          text=" | ",
                          text_color="red",
                          font=FONT(18, weight=FONT_WEIGHT_BOLD),
                          )
    label3 = ctk.CTkLabel(l_container,
                          text="translation1, translation2, ...",
                          text_color=COLOR_GRAY,
                          font=FONT(18, weight=FONT_WEIGHT_REGULAR),
                          )
    label4 = ctk.CTkLabel(self,
                          text="Line will be ignored otherwise!",
                          text_color=COLOR_GRAY,
                          font=FONT(24, weight=FONT_WEIGHT_BOLD),
                          )

    button = ctk.CTkButton(self,
                           height=40,
                           width=240,
                           text="Choose file",
                           text_color=COLOR_WHITE,
                           anchor="s",
                           font=FONT(28, weight=FONT_WEIGHT_BOLD),
                           corner_radius=4,
                           bg_color=COLOR_YELLOW,
                           fg_color=COLOR_BLUE,
                           hover_color=COLOR_PINK,
                           command=self.__update_file_path)
    label.pack(side=tk.TOP, pady=15)
    l_container.pack(side=tk.TOP, pady=15)
    label1.pack(side=tk.LEFT)
    label2.pack(side=tk.LEFT)
    label3.pack(side=tk.LEFT)
    label4.pack(side=tk.TOP, pady=15)
    button.pack(side=tk.TOP, pady=15)

    self.file_path: str | PathLike | None = None

  def __update_file_path(self):
    self.file_path = askopenfilename()
    self.destroy()


class AddNewWordPopUp(BasePopUp):

  def build(self):
    self.configure(fg_color=COLOR_YELLOW)
    self.title("Add new word")
    self.geometry("500x500")
    self.resizable(False, False)
    self.bind("<Button-1>", lambda event: event.widget.focus_set())
    label1 = ctk.CTkLabel(self,
                          text="Enter word:",
                          text_color=COLOR_GRAY,
                          font=FONT(24, weight=FONT_WEIGHT_BOLD),
                          )
    label2 = ctk.CTkLabel(self,
                          text="Enter translations:",
                          text_color=COLOR_GRAY,
                          font=FONT(24, weight=FONT_WEIGHT_BOLD),
                          )
    confirm_button = ctk.CTkButton(self,
                                   height=40,
                                   width=200,
                                   text="Confirm",
                                   text_color=COLOR_WHITE,
                                   anchor="s",
                                   font=FONT(28, weight=FONT_WEIGHT_BOLD),
                                   corner_radius=4,
                                   bg_color=COLOR_YELLOW,
                                   fg_color=COLOR_BLUE,
                                   hover_color=COLOR_PINK,
                                   command=self.__update_data)

    self.word_entry = ctk.CTkEntry(self,
                                   placeholder_text="word",
                                   placeholder_text_color=COLOR_PINK_LIGHT,
                                   text_color=COLOR_GRAY,
                                   font=FONT(24, weight=FONT_WEIGHT_REGULAR),
                                   height=30,
                                   width=300,
                                   corner_radius=6,
                                   border_width=0,
                                   bg_color=COLOR_BROWN,
                                   fg_color=COLOR_BROWN,
                                   )

    self.translation_entries: list[ctk.CTkEntry] = []
    self.translation_entries_container = tk.Frame(self, background=COLOR_YELLOW)

    label1.pack(side=tk.TOP, pady=15)
    self.word_entry.pack(side=tk.TOP, pady=15)
    label2.pack(side=tk.TOP, pady=15)
    self.translation_entries_container.pack()
    self.__add_translation_entry()
    confirm_button.pack(side=tk.BOTTOM, pady=20)

    self.word: str | None = None
    self.translations: list[str] | None

  def __update_data(self):
    if self.word_entry.get():
      self.word = self.word_entry.get().strip().lower()

    translations = list(filter(bool, [t_e.get().strip().lower() for t_e in self.translation_entries]))
    if len(translations):
      self.translations = translations

    self.destroy()

  def __modify_translation_entries(self, e: tk.Event):
    empty_entries = list(filter(lambda x: not bool(x.get()), self.translation_entries))

    if len(empty_entries) > 1:
      self.__del_translation_entry(self.translation_entries.index(empty_entries[-1]))

    for entry in self.translation_entries:
      if not entry.get():
        return
    if len(self.translation_entries) < 6:
      self.__add_translation_entry()

  def __add_translation_entry(self):
    new_entry = ctk.CTkEntry(self.translation_entries_container,
                             placeholder_text=f"one of the translations",
                             placeholder_text_color=COLOR_PINK_LIGHT,
                             text_color=COLOR_GRAY,
                             font=FONT(24, weight=FONT_WEIGHT_REGULAR),
                             height=30,
                             width=300,
                             corner_radius=6,
                             border_width=0,
                             bg_color=COLOR_BROWN,
                             fg_color=COLOR_BROWN,
                             )
    new_entry.pack(side=tk.TOP, pady=5)
    new_entry.bind("<FocusOut>", self.__modify_translation_entries)
    self.translation_entries.append(new_entry)

  def __del_translation_entry(self, i: int):
    entry = self.translation_entries.pop(i)
    entry.pack_forget()
