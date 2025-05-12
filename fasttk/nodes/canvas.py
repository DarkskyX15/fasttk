
import tkinter as tk
from tkinter import ttk
from fasttk.base import Node, StylesManager
from fasttk.style import Style
from typing import Callable, Any

class Canvas(Node):

    _widget_instance: tk.Canvas

    def __init__(
        self,
        *,
        tags: str = "",
        ref: str | None = None,
        style: Style | None = None
    ):
        super().__init__(tags=tags, type="canvas", ref=ref, style=style)

    def __build__(self, master: tk.Misc, component, window) -> None:
        args = self._normal_repr.props_map({
            "cursor": "cursor",
            "take_focus": "takefocus",
            "scale_length": "length"
        })
        style_args = self.__style_map__({
            "border_width": "borderwidth",
            "background": "background"
        })
        args["style"] = StylesManager().use_style("TCanvas", style_args)
        self._widget_instance = ttk.Scale(master, **args)

    @property
    def widget(self) -> tk.Canvas:
        return self._widget_instance
