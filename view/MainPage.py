import tkinter as tk

from controller import Controller, Util
from module.Danbooru import Danbooru
from view.Color import Color


class MainPage:

    def __init__(self):
        self._tags_input = None
        self._min_page_field = None
        self._max_page_field = None
        self._maximal_page_label = None

        self.log_box = None

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
        self._tags_components()
        self._maximal_page()
        self._page_component()
        self._download_button()
        self.log_box_init()

    def _tags_components(self):
        # tags label
        tags = tk.Label(self.root, text="Tags", font="Helvetica 14", bg=Color.WHITE)
        tags.pack(side="top", anchor="w", padx=25)

        # tags container
        tags_container = tk.Frame(self.root, bg=Color.WHITE)

        # tags input
        self._tags_input = tk.Entry(tags_container, font="Helvetica 12", width=36)
        self._tags_input.configure(borderwidth=5, relief=tk.FLAT)
        self._tags_input.grid(column=0, row=0, padx=(0, 10))

        tags_button = tk.Button(tags_container, text="Search")
        tags_button.configure(bg=Color.GRAY, fg=Color.WHITE, )
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
        tags_button.configure(command=lambda: self._init_danbooru(self._tags_input))

    def _maximal_page(self):
        self._maximal_page_label = tk.Label(self.root, text="Maximal page: 0", font="Helvetica 12", bg=Color.WHITE)
        self._maximal_page_label.pack(side="top", anchor="w", padx=25, pady=(10, 0))

    def _update_max_page(self, max_page):
        Controller.insert_log(self.log_box, "Found %d page(s)" % max_page, 'normal')
        s = "Maximal page: %d" % max_page
        self._maximal_page_label.configure(text=s)

    def _page_component(self):
        # page field
        page_container = tk.Frame(self.root, bg=Color.WHITE)

        self._min_page_label = tk.Label(page_container, text="Min Page: ", font="Helvetica 12", bg=Color.WHITE)
        self._min_page_label.grid(row=0, column=0)

        self._min_page_field = tk.Entry(page_container, font="Helvetica 12", width=5)
        self._min_page_field.configure(borderwidth=5, relief=tk.FLAT, bg=Color.WHITE)
        self._min_page_field.grid(row=0, column=1)

        self._max_page_label = tk.Label(page_container, text="Max Page: ", font="Helvetica 12", bg=Color.WHITE)
        self._max_page_label.grid(row=0, column=2, padx=(10, 0))

        self._max_page_field = tk.Entry(page_container, font="Helvetica 12", width=5)
        self._max_page_field.configure(borderwidth=5, relief=tk.FLAT, bg=Color.WHITE)
        self._max_page_field.grid(row=0, column=3)

        page_container.pack(side="top", anchor="w", padx=25, pady=(30, 0))

    def _download_button(self):
        download_btn = tk.Button(self.root, text="Scrap Images", font="Helvetica 14 bold")
        download_btn.configure(bg=Color.GRAY, fg=Color.WHITE)
        download_btn.configure(borderwidth=5, relief=tk.FLAT)
        download_btn.pack(anchor="e", side="bottom", padx=25, pady=25)

        download_btn.configure(
            command=lambda: Controller.scrap_page(self.danbooru, self._min_page_field, self._max_page_field,
                                                  self.log_box))

    def log_box_init(self):
        self.log_box = tk.Text(self.root, pady=5, padx=5)
        self.log_box.config(borderwidth=3, relief=tk.FLAT)
        self.log_box.config(bg=Color.WHITE, font="Helvetica 14")
        self.log_box.config(state="disabled")
        self.log_box.pack(side="bottom", anchor="center", padx=25, pady=(10, 15))

        self.log_box.tag_config('warning', foreground=Color.RED)
        self.log_box.tag_config('normal', foreground=Color.BLACK)

    def _clear_log(self):
        self.log_box.config(state="normal")
        self.log_box.delete('1.0', tk.END)
        self.log_box.config(state="disabled")

    def _init_danbooru(self, _tags_input):
        tags = _tags_input.get()
        self._clear_log()
        if not Util.check_tags(tags):
            Controller.insert_log(self.log_box, "Tags cannot be empty", 'warning')
            return

        self.danbooru = Danbooru(tags=tags, filter=self.filter)
        self._update_max_page(self.danbooru.get_max_page())

    def _set_filter(self, filter):
        self.filter = filter

    def pre(self):
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        self.root.configure(background=Color.WHITE)
