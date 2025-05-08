
import asyncio
from fasttk import *

class Login(Component):

    display: Label

    def change(self, x: str):
        self.display.text = x

    def struct(self):
        return Frame(tags="container lol").add(
            Label(tags="next", text="Hello World", ref="display"),
            Combobox(
                values=["Genshin", "impact", "mc", "xt"], tags="cb rb",
                readonly=True, on_select=self.change
            )
        )

    def styles(self) -> list[Style]:
        return [
            {
                "selector": ".container",
                "expand": True,
                "display": "pack",
                "pack_direction": "column",
                "background": "#39c5bb",
                "left": 0.05,
                "top": 0.05,
                "width": 0.9,
                "height": 0.9
            }
        ]


class ExampleWindow(Component):

    sub: Frame
    create_but: Button
    del_but: Button
    pre: Component
    
    async def test(self) -> None:
        await asyncio.sleep(10)
        print("time's up")
    
    def ch(self, _) -> None:
        self.create_but.disabled = not self.create_but.disabled

    def create_window(self):
        self.pre = ftk.create_window(
            Login, background="alice blue"
        )

    def del_cp(self):
        self.pre.destroy()
        self.create_but.disabled = False
        self.del_but.disabled = True

    def on_mount(self):
        self.key_listen = self.window.bind(
            EventSpec(event="KeyPress", modifier1="Control", key="w"),
            lambda _: self.change_component()
        )

    def change_component(self):
        self.window.unbind(
            EventSpec(event="KeyPress", modifier1="Control", key="w"),
            self.key_listen
        )
        self.destroy()
        ftk.mount_component(self.window, Login)

    def struct(self) -> Node:
        return Frame(tags="container lol").add(
            Label(tags="next", text="Hello World"),
            Frame(tags="sub", ref="sub").add(
                Button(
                    tags="rb default", text="Mount",
                    on_pressed=self.create_window,
                    ref="create_but"
                ),
                Button(
                    tags="rb default", text="Del", on_pressed=self.del_cp,
                    ref="del_but", disabled=True
                ),
            ),
        )

    def styles(self) -> list[Style]:
        return [
            {
                "selector": ".container",

                "relief": "ridge",
                "height": 0.9,
                "width": 0.9,
                "left": 0.05,
                "top": 0.05,
                "background": "#39c5bb",
                "border_width": 15,
                "display": "grid",
                "row_weight": "0 1",
                "column_weight": "0 0, 1 1",
                "column_minsize": "0 20"
            },
            {
                "selector": ".next",
                "cursor": "hand2",
                "foreground": "green",
                "background": "#39c5bb",
                "font": "Consolas",
                "font_unit": "pound",
                "font_size": 20,
                "font_variant": ("overstrike", "italic"),
                "grid": "0, 0",
                "stick": "horizontal",
                "compound_position": "left",
                "padding_right": 10
            },
            {
                "selector": ".sub",
                "background": "cyan",
                "grid": "0, 1",
                "stick": "all",
                "padding": 50,
                "display": "pack",
                "pack_direction": "column",
                "align_items": "stretch"
            },
            {
                "selector": ".rb",
                "font": "Consolas",
                "font_unit": "pound",
                "font_size": 20,
                "font_weight": "normal",
                "font_variant": ("overstrike", "italic")
            },
            {
                "selector": "button.default",
                "default_button": True
            },
            {
                "selector": "checkbutton",
                "background": "red",
                "foreground": "green",
                "font": "Consolas",
                "font_unit": "pound",
                "font_size": 20,
                "font_variant": ("overstrike", "italic")
            },
            {
                "selector": ".input",
                "cursor": "xterm",
                "background": "red",
                "foreground": "yellow green",
                "text_align": "left",
                "padding": (20, 20)
            },
            {
                "selector": ".sb",
                "background": "red",
                "foreground": "sea green"
            },
            {
                "selector": ".cb",
                "foreground": "red",
                "combo_background": "yellow",
                "margin": 10
            },
            {
                "selector": ".sc",
                "foreground": "purple",
                "background": "green yellow",
                "orientation": "horizontal",
                "scale_length": 200
            },
            {
                "selector": "text",
                "background": "red",
                "foreground": "yellow"
            }
        ]

if __name__ == '__main__':
    
    ftk.main_window(
        ExampleWindow, size=(600, 450)
    )
    ftk.mainloop()
