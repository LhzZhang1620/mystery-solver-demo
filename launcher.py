"""Start screen, case selection, settings, and navigation for the game."""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import ttk
from typing import Any, Callable

from app import MysteryApp
from cases.night_clock import case_for_language
from i18n import text as ui_text


class CaseLauncher:
    INK = "#10182b"
    PANEL = "#1e2b47"
    PANEL_HIGH = "#263654"
    LINE = "#40506e"
    PAPER = "#f4f0e7"
    MUTED = "#aebbd0"
    TEAL = "#77d7d1"
    GOLD = "#e8b85a"
    FONT = "Microsoft YaHei UI"
    SERIF = "Microsoft YaHei"
    START_HERO_HEIGHT = 300
    START_HERO_SCALE = 1
    HERO_EDGE_FADE_WIDTH = 470
    CASE_COVER_SIZE = (760, 360)

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.project_root = Path(__file__).resolve().parent
        self.images: dict[str, tk.PhotoImage] = {}
        self.language = "zh"
        self.root.title(self._t("launcher_title"))
        self.root.configure(bg=self.INK)
        self.root.geometry("1200x780")
        self.root.minsize(900, 620)
        self._configure_styles()
        self.show_start()

    def _t(self, key: str, **values: object) -> str:
        return ui_text(self.language, key, **values)

    def _configure_styles(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("Archive.Horizontal.TSeparator", background=self.LINE)

    def _clear_page(self) -> None:
        for sequence in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            self.root.unbind_all(sequence)
        for child in self.root.winfo_children():
            child.destroy()

    def _button(self, parent: tk.Widget, text: str, command: Callable[[], None], kind: str = "normal") -> tk.Button:
        colors = {
            "normal": (self.PANEL_HIGH, self.PAPER, self.LINE),
            "action": (self.GOLD, self.INK, self.GOLD),
            "quiet": (self.INK, self.MUTED, self.LINE),
        }
        bg, fg, border = colors[kind]
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=bg,
            activeforeground=fg,
            relief="flat",
            bd=0,
            highlightbackground=border,
            highlightthickness=1,
            cursor="hand2",
            font=(self.FONT, 10, "bold"),
            padx=15,
            pady=10,
        )

    def _image(self, relative_path: str, scale: int) -> tk.PhotoImage | None:
        cache_key = f"{relative_path}:{scale}"
        try:
            if cache_key not in self.images:
                original = tk.PhotoImage(file=self.project_root / relative_path)
                self.images[cache_key] = original.subsample(scale, scale)
            return self.images[cache_key]
        except tk.TclError:
            return None

    def _cover_image(self, relative_path: str, size: tuple[int, int]) -> tk.PhotoImage | None:
        """Scale an image down, then let its fixed canvas crop it to the display frame."""
        width, height = size
        cache_key = f"{relative_path}:cover:{width}x{height}"
        try:
            if cache_key not in self.images:
                original = tk.PhotoImage(file=self.project_root / relative_path)
                scale = max(1, min(original.width() // width, original.height() // height))
                self.images[cache_key] = original.subsample(scale, scale)
            return self.images[cache_key]
        except tk.TclError:
            return None

    def _add_edge_fade(
        self,
        canvas: tk.Canvas,
        *,
        width: int | None,
        height: int,
        fade_width: int,
        left: bool = False,
        right: bool = False,
    ) -> None:
        """Overlay a dark stippled fade at one or both edges of an image canvas."""
        bands = (
            (0.00, 0.50, None),
            (0.47, 0.66, "gray75"),
            (0.63, 0.80, "gray50"),
            (0.77, 0.93, "gray25"),
            (0.90, 1.00, "gray12"),
        )

        def draw_band(start: int, end: int, stipple: str | None) -> None:
            options: dict[str, str] = {"fill": self.INK, "outline": "", "tags": "edge-fade"}
            if stipple is not None:
                options["stipple"] = stipple
            canvas.create_rectangle(start, 0, end, height, **options)

        if left:
            for start, end, stipple in bands:
                draw_band(round(start * fade_width), round(end * fade_width), stipple)
        if right and width is not None:
            for start, end, stipple in bands:
                draw_band(round(width - end * fade_width), round(width - start * fade_width), stipple)

    def show_start(self) -> None:
        self._clear_page()
        self.root.title(self._t("launcher_title"))

        viewport = tk.Frame(self.root, bg=self.INK)
        viewport.pack(fill="both", expand=True)
        start_canvas = tk.Canvas(viewport, bg=self.INK, highlightthickness=0, bd=0)
        start_scrollbar = ttk.Scrollbar(viewport, orient="vertical", command=start_canvas.yview)
        start_canvas.configure(yscrollcommand=start_scrollbar.set)
        start_canvas.pack(side="left", fill="both", expand=True)
        start_scrollbar.pack(side="right", fill="y")

        page = tk.Frame(start_canvas, bg=self.INK)
        page_window = start_canvas.create_window((0, 0), window=page, anchor="nw")

        def update_scroll_region(_: tk.Event[tk.Misc]) -> None:
            start_canvas.configure(scrollregion=start_canvas.bbox("all"))

        def resize_page(event: tk.Event[tk.Misc]) -> None:
            start_canvas.itemconfigure(page_window, width=event.width)

        def is_over_start_page(event: tk.Event[tk.Misc]) -> bool:
            widget = self.root.winfo_containing(event.x_root, event.y_root)
            while widget is not None:
                if widget is start_canvas:
                    return True
                widget = widget.master
            return False

        def scroll_with_wheel(event: tk.Event[tk.Misc]) -> str | None:
            if not is_over_start_page(event):
                return None
            start_canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")
            return "break"

        def scroll_with_button(direction: int) -> Callable[[tk.Event[tk.Misc]], str | None]:
            def handler(event: tk.Event[tk.Misc]) -> str | None:
                if not is_over_start_page(event):
                    return None
                start_canvas.yview_scroll(direction, "units")
                return "break"

            return handler

        page.bind("<Configure>", update_scroll_region)
        start_canvas.bind("<Configure>", resize_page)
        self.root.bind_all("<MouseWheel>", scroll_with_wheel)
        self.root.bind_all("<Button-4>", scroll_with_button(-1))
        self.root.bind_all("<Button-5>", scroll_with_button(1))

        content = tk.Frame(page, bg=self.INK)
        content.pack(fill="both", expand=True, padx=34, pady=27)

        toolbar = tk.Frame(content, bg=self.INK)
        toolbar.pack(fill="x")
        tk.Label(toolbar, text=self._t("launcher_name"), bg=self.INK, fg=self.PAPER, font=(self.SERIF, 16, "bold")).pack(side="left")
        tk.Label(toolbar, text=f"  /  {self._t('case_archive')}", bg=self.INK, fg=self.TEAL, font=(self.FONT, 9, "bold")).pack(side="left", pady=(3, 0))
        self._button(toolbar, self._t("settings"), self.open_settings, kind="quiet").pack(side="right")

        art = self._image("assets/ui/start-screen.png", self.START_HERO_SCALE)
        hero_height = self.START_HERO_HEIGHT
        hero = tk.Frame(
            content,
            bg=self.PANEL,
            highlightbackground=self.LINE,
            highlightthickness=1,
        )
        hero.pack(fill="x", pady=(17, 20))
        hero_stage = tk.Canvas(hero, height=hero_height, bg="#17233b", highlightthickness=0, bd=0)
        hero_stage.pack(fill="x")
        if art is not None:
            image_id = hero_stage.create_image(0, hero_height // 2, image=art, anchor="center")
            hero_stage.image = art
            hero_stage.bind("<Configure>", lambda event: hero_stage.coords(image_id, event.width // 2, hero_height // 2))
        self._add_edge_fade(
            hero_stage,
            width=None,
            height=hero_height,
            fade_width=self.HERO_EDGE_FADE_WIDTH,
            left=True,
        )
        hero_text_offset = max(0, (hero_height - 300) // 2)
        hero_stage.create_text(42, 58 + hero_text_offset, text="", anchor="w", fill=self.TEAL, font=(self.FONT, 10, "bold"))
        hero_stage.create_text(42, 104 + hero_text_offset, text=self._t("hero_title"), anchor="w", fill=self.PAPER, font=(self.SERIF, 29, "bold"), justify="left")
        hero_stage.create_text(42, 205 + hero_text_offset, text=self._t("hero_body"), anchor="w", fill="#d5dce7", font=(self.FONT, 11), justify="left")
        hero_stage.create_text(42, 265 + hero_text_offset, text=self._t("hero_cta"), anchor="w", fill=self.GOLD, font=(self.FONT, 9, "bold"))

        cards = tk.Frame(content, bg=self.INK)
        cards.pack(fill="both", expand=True)
        cards.columnconfigure(0, weight=1)
        self._case_card(cards, case_for_language(self.language), self._t("case_available"), self._t("start_case"), self.open_case_one)

    def _case_card(self, parent: tk.Widget, case: dict[str, Any], status: str, button_label: str, command: Callable[[], None]) -> None:
        card = tk.Frame(parent, bg=self.PANEL, highlightbackground=self.LINE, highlightthickness=1)
        card.grid(row=0, column=0, sticky="nsew", pady=4)
        card.columnconfigure(0, weight=1)
        content = tk.Frame(card, bg=self.PANEL)
        content.pack(fill="both", expand=True, padx=23, pady=22)
        image_path = case.get("cover") or (case["locations"][0]["background"] if case.get("locations") else None)
        cover_width, cover_height = self.CASE_COVER_SIZE
        cover = tk.Canvas(content, width=cover_width, height=cover_height, bg="#17233b", highlightthickness=0, bd=0)
        cover.pack(anchor="center", pady=(0, 15))
        art = self._cover_image(image_path, self.CASE_COVER_SIZE) if image_path else None
        if art is not None:
            cover.create_image(cover_width // 2, cover_height // 2, image=art, anchor="center")
            cover.image = art
        else:
            cover.create_text(cover_width // 2, cover_height // 2, text=self._t("image_missing"), fill=self.MUTED, font=(self.FONT, 11, "bold"))
        tk.Label(content, text=case["number"], bg=self.PANEL, fg=self.GOLD, font=("Consolas", 10, "bold")).pack(anchor="w")
        tk.Label(content, text=case["title"], bg=self.PANEL, fg=self.PAPER, font=(self.SERIF, 20, "bold")).pack(anchor="w", pady=(9, 5))
        tk.Label(content, text=status, bg=self.PANEL, fg=self.TEAL if status == self._t("case_available") else self.MUTED, font=(self.FONT, 9, "bold")).pack(anchor="w")
        tk.Label(content, text=case["subtitle"], bg=self.PANEL, fg=self.MUTED, justify="left", anchor="w", wraplength=420, font=(self.FONT, 10)).pack(fill="x", pady=(14, 24))
        self._button(content, button_label, command, kind="action" if status == self._t("case_available") else "normal").pack(anchor="w")

    def open_case_one(self) -> None:
        self._clear_page()
        MysteryApp(self.root, case=case_for_language(self.language), on_return=self.show_start, language=self.language)

    def open_settings(self) -> None:
        dialog = tk.Toplevel(self.root)
        dialog.title(self._t("settings"))
        dialog.configure(bg=self.PANEL)
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        body = tk.Frame(dialog, bg=self.PANEL, padx=24, pady=22)
        body.pack(fill="both", expand=True)
        tk.Label(body, text=self._t("settings_title"), bg=self.PANEL, fg=self.PAPER, font=(self.SERIF, 18, "bold")).pack(anchor="w")
        tk.Label(body, text=self._t("window_size"), bg=self.PANEL, fg=self.MUTED, font=(self.FONT, 10)).pack(anchor="w", pady=(18, 5))
        size = tk.StringVar(value=self._t("standard_size"))
        for label, geometry in ((self._t("standard_size"), "1200x760"), (self._t("large_size"), "1400x860")):
            tk.Radiobutton(body, text=label, variable=size, value=label, command=lambda value=geometry: self.root.geometry(value), bg=self.PANEL, fg=self.PAPER, selectcolor=self.PANEL_HIGH, activebackground=self.PANEL, activeforeground=self.PAPER, font=(self.FONT, 10)).pack(anchor="w", pady=3)
        tk.Label(body, text=self._t("language"), bg=self.PANEL, fg=self.MUTED, font=(self.FONT, 10)).pack(anchor="w", pady=(16, 3))
        language = tk.StringVar(value=self.language)

        def change_language(value: str) -> None:
            self.language = value
            dialog.destroy()
            self.show_start()

        tk.Radiobutton(body, text=self._t("chinese"), variable=language, value="zh", command=lambda: change_language("zh"), bg=self.PANEL, fg=self.PAPER, selectcolor=self.PANEL_HIGH, activebackground=self.PANEL, activeforeground=self.PAPER, font=(self.FONT, 10)).pack(anchor="w", pady=3)
        tk.Radiobutton(body, text=self._t("english"), variable=language, value="en", command=lambda: change_language("en"), bg=self.PANEL, fg=self.PAPER, selectcolor=self.PANEL_HIGH, activebackground=self.PANEL, activeforeground=self.PAPER, font=(self.FONT, 10)).pack(anchor="w", pady=3)
        self._button(body, self._t("close"), dialog.destroy, kind="action").pack(anchor="e", pady=(22, 0))


def launch() -> None:
    root = tk.Tk()
    CaseLauncher(root)
    root.mainloop()
