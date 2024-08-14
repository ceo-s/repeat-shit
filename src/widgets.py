from tkinter import ttk
from tkinter.filedialog import askopenfilename
from typing import Callable, ParamSpec, Literal, Any
from abc import abstractmethod, ABC
from os import PathLike

import tkinter as tk
import customtkinter as ctk

from src.consts import *
from src.gallery import Gallery
from src.vocabulary import Vocabulary, Word, Translation, Language
from src.scrollable_dropdown import CTkScrollableDropdown


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
  LANG_LIST = ["Russian", "English", "Italian", "French"]

  def init(self):
    self.pack_propagate(True)
    self.configure(height=50, width=400, background=COLOR_YELLOW, highlightthickness=0, relief='ridge')
    self.__choose_lang_from = ctk.CTkOptionMenu(self, 180, 50, 6,
                                                font=FONT(20, weight=FONT_WEIGHT_BOLD),
                                                dropdown_font=FONT(20),
                                                values=self.LANG_LIST,
                                                fg_color=COLOR_PINK1,
                                                text_color=COLOR_YELLOW,
                                                dropdown_text_color=COLOR_PINK1,
                                                dropdown_hover_color=COLOR_BROWN,
                                                dropdown_fg_color=COLOR_YELLOW,
                                                button_color=COLOR_PINK2,
                                                button_hover_color=COLOR_PINK2,
                                                )
    CTkScrollableDropdown(self.__choose_lang_from,
                          id_="from",
                          values=self.LANG_LIST,
                          command=self.__on_lang_change,
                          button_color=COLOR_PINK1,
                          text_color=COLOR_YELLOW,
                          scrollbar_button_color=COLOR_PINK2,
                          fg_color=COLOR_YELLOW,
                          frame_border_width=0,
                          frame_corner_radius=40,
                          scrollbar_button_hover_color=COLOR_PINK2,
                          hover_color=COLOR_PINK2,
                          )

    self.__choose_lang_to = ctk.CTkOptionMenu(self, 180, 50, 6,
                                              font=FONT(20, FONT_WEIGHT_REGULAR),
                                              dropdown_font=FONT(20, FONT_WEIGHT_REGULAR),
                                              values=self.LANG_LIST,
                                              fg_color=COLOR_PINK1,
                                              text_color=COLOR_YELLOW,
                                              dropdown_text_color=COLOR_PINK1,
                                              dropdown_hover_color=COLOR_BROWN,
                                              dropdown_fg_color=COLOR_YELLOW,
                                              button_color=COLOR_PINK2,
                                              button_hover_color=COLOR_PINK2,
                                              )

    CTkScrollableDropdown(self.__choose_lang_to,
                          id_="to",
                          values=self.LANG_LIST,
                          command=self.__on_lang_change,
                          button_color=COLOR_PINK1,
                          text_color=COLOR_YELLOW,
                          scrollbar_button_color=COLOR_PINK2,
                          fg_color=COLOR_YELLOW,
                          frame_border_width=0,
                          frame_corner_radius=40,
                          scrollbar_button_hover_color=COLOR_PINK2,
                          hover_color=COLOR_PINK2,
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

    self.__callbacks: dict[str, list[Callable[[str], None]]] = {"<<LangSwap>>": [], "<<LangChange>>": []}
    self.add_callback("<<LangChange>>", self.__swap_if_both_same)
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

  def __on_lang_change(self, val: str):
    for callback in self.__callbacks["<<LangChange>>"]:
      callback(val)

  def __on_lang_swap(self):
    for callback in self.__callbacks["<<LangSwap>>"]:
      callback("")

  def add_callback(self, event: Literal["<<LangSwap>>", "<<LangChange>>"], callback: Callable[[str], None]):
    self.__callbacks[event].append(callback)

  def __swap_if_both_same(self, val: str):
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
    self.configure(width=500, height=100, bg=COLOR_YELLOW, highlightthickness=0, relief='ridge')

    self.__slider = ctk.CTkSlider(self, from_=0, to=1,
                                  command=self.__update_label_value,
                                  fg_color=COLOR_PINK3,
                                  height=30,
                                  width=360,
                                  progress_color=COLOR_BLUE,
                                  button_color=COLOR_PINK1,
                                  button_hover_color=COLOR_PINK2,
                                  )

  def build(self):
    self.__text_id = self.create_text(250.0, 35.0, fill=COLOR_GRAY, anchor="center", text=f"{int(self.get())}/{self.__max_value}",
                                      font=FONT(40, weight=FONT_WEIGHT_BOLD))
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

    self.itemconfig(self.__text_id, text=f"{int(self.get())}/{num}")
    self.__slider.set(self.get())
    self.__max_value = num

  def __update_label_value(self, value: float):
    self.itemconfig(self.__text_id, text=f"{int(value)}/{self.__max_value}")


# class VocabularyTable(BaseWidget):

#   def init(self):
#     self.configure(height=460, width=900, bg=COLOR_BROWN, highlightthickness=0)
#     self.head = tk.Canvas(self, height=60, width=900,
#                           bg=COLOR_BROWN, highlightthickness=0)
#     self.body = tk.Canvas(self, height=400, width=900,
#                           bg=COLOR_BROWN, highlightthickness=0)
#     self.body_scrollbar = tk.Scrollbar(self, orient='vertical')
#     self.body_scrollbar.configure(command=self.body.yview)
#     self.body.configure(yscrollcommand=self.body_scrollbar.set)
#     self.body.bind("<MouseWheel>", self.__on_mouse_scroll)
#     self.body.bind("<Button-4>", self.__on_mouse_scroll)
#     self.body.bind("<Button-5>", self.__on_mouse_scroll)
#     self.content: list[Word] = []

#   def build(self):
#     self.__del_rows()
#     self.head.pack()
#     self.body_scrollbar.pack(side=tk.RIGHT, fill='y')
#     self.body.pack()

#     self.head.create_text(
#         30.0,
#         25.0,
#         anchor="nw",
#         text="Word:",
#         fill="#000000",
#         font=FONT(24)
#     )

#     self.head.create_text(
#         350.0,
#         25.0,
#         anchor="nw",
#         text="Translation:",
#         fill="#000000",
#         font=FONT(24)
#     )

#     self.head.create_text(
#         770.0,
#         25.0,
#         anchor="nw",
#         text="Accuracy:",
#         fill="#000000",
#         font=FONT(24)
#     )

#     self.head.create_rectangle(
#         30.0,
#         57.0,
#         870.0,
#         58.0,
#         fill="#000000",
#         outline="")

#     self.__add_rows()

#   def update_content(self, new_content: list[Word]):
#     self.content.clear()
#     self.content.extend(new_content)

#   def __add_rows(self):

#     # Bullshit lines because otherways canvas somehow
#     # places everything relative to first placed element now
#     self.body.create_rectangle(0, 10, 0, 10,
#                                fill=COLOR_BROWN,
#                                outline=COLOR_BROWN)
#     # Endbullshit lines

#     for i, row in enumerate(self.content, start=1):
#       self.body.create_text(35, 30 * i, anchor="w", text=row.word,
#                             fill=COLOR_BLACK, font=FONT(20, FONT_WEIGHT_REGULAR))
#       self.body.create_text(355, 30 * i, anchor="w", text=row.word,
#                             fill=COLOR_BLACK, font=FONT(20, FONT_WEIGHT_REGULAR))
#       self.body.create_text(803, 30 * i, anchor="w", text=f"{row.language.value}%",
#                             fill=COLOR_BLACK, font=FONT(20, FONT_WEIGHT_REGULAR))

#     self.body.configure(scrollregion=self.body.bbox("all"))

#   def __del_rows(self):
#     self.body.delete("all")
#     self.body_scrollbar.pack_forget()
#     self.body.configure(scrollregion=(0, 0, 0, 0))

#   def __on_mouse_scroll(self, e: tk.Event):
#     print(f"Scrolling with wheel {e}")
#     if e.num == 4:
#       self.body.yview_scroll(-1, 'units')
#     if e.num == 5:
#       self.body.yview_scroll(1, 'units')


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

    # button = ctk.CTkButton(self, text="Choose file", command=self.__update_file_path)
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
                           hover_color=COLOR_PINK1,
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
                                   hover_color=COLOR_PINK1,
                                   command=self.__update_data)

    self.word_entry = ctk.CTkEntry(self,
                                   placeholder_text="word",
                                   placeholder_text_color=COLOR_PINK3,
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
                             placeholder_text_color=COLOR_PINK3,
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
