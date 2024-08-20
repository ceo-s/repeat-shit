import tkinter as tk


def add_scroll_linux(widget: tk.Widget):
  widget.bind_all("<Button-4>", lambda e: widget._parent_canvas.yview("scroll", -1, "units"))
  widget.bind_all("<Button-5>", lambda e: widget._parent_canvas.yview("scroll", 1, "units"))
