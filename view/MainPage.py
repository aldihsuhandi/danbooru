import tkinter as tk

from module.Danbooru import Danbooru
from view.Color import Color


def _change_on_hover(button, bg_hover, fg_hover, bg_leave, fg_leave):
    button.bind("<Enter>", func=lambda e: button.config(background=bg_hover, foreground=fg_hover))
    button.bind("<Leave>", func=lambda e: button.config(background=bg_leave, foreground=fg_leave))


class MainPage:
    def __init__(self):
        self.danbooru = None
        self.filter = "All"

        self.root = tk.Tk()
        self.root.title = "Danbooru"

        self.pre()
        self.component()

        self.root.mainloop()

    def component(self):
        # Title
        title = tk.Label(self.root, text="Danbooru", font="Helvetica 18 bold underline", bg=Color.WHITE)
        title.pack(side="top", anchor="center", pady=25)

        # tags label
        tags = tk.Label(self.root, text="Tags", font="Helvetica 14", bg=Color.WHITE)
        tags.pack(side="top", anchor="w", padx=25)

        # tags container
        tags_container = tk.Frame(self.root, bg=Color.WHITE)

        # tags input
        tags_input = tk.Entry(tags_container, font="Helvetica 12", width=36)
        tags_input.configure(borderwidth=5, relief=tk.FLAT)
        tags_input.grid(column=0, row=0, padx=(0, 10))

        tags_button = tk.Button(tags_container, text="Search")
        tags_button.configure(bg=Color.GRAY, fg=Color.WHITE, )
        _change_on_hover(tags_button, Color.BLACK, Color.WHITE, Color.GRAY, Color.WHITE)
        tags_button.grid(column=1, row=0, padx=(10, 0))

        tags_container.pack(side="top", anchor="w", padx=25)

        # Filter
        options = [
            "All",
            "SFW Only",
            "NSFW Only"
        ]

        default = tk.StringVar()
        default.set(options[0])

        tags_filter = tk.OptionMenu(self.root, default, *options, command=self._set_filter)
        tags_filter.configure(borderwidth=5, relief=tk.FLAT)
        tags_filter.configure(background=Color.WHITE, width=32, font="Helvetica 12")
        tags_filter.pack(side="top", anchor="w", padx=25, pady=(4, 0))

        # command
        tags_button.configure(command=lambda: self._init_danbooru(tags_input))

    def _init_danbooru(self, tags_input):
        tags = tags_input.get()

        print("tags=%s\nfilter=%s\n" % (tags, self.filter))

        self.danbooru = Danbooru(tags=tags, filter=self.filter)

    def _set_filter(self, filter):
        self.filter = filter

    def pre(self):
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        self.root.configure(background=Color.WHITE)
