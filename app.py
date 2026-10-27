"""Desktop entry point for the Python-only Text Adventure Mystery Solver."""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import ttk
from typing import Any

from cases.night_clock import CASE as DEFAULT_CASE
from engine import Analysis, MysteryEngine
from i18n import text as ui_text


class MysteryApp:
    """Tkinter interface for one data-driven mystery case."""

    INK = "#10182b"
    PANEL = "#1e2b47"
    PANEL_HIGH = "#263654"
    LINE = "#40506e"
    PAPER = "#f4f0e7"
    MUTED = "#aebbd0"
    TEAL = "#77d7d1"
    GOLD = "#e8b85a"
    GREEN = "#91d4a0"
    ROSE = "#ed8d91"
    FONT = "Microsoft YaHei UI"
    SERIF = "Microsoft YaHei"
    DIALOGUE_PORTRAIT_SCALE = 6
    NOTEBOOK_PORTRAIT_SCALE = 14

    def __init__(
        self,
        root: tk.Tk,
        case: dict[str, Any] | None = None,
        on_return: Any | None = None,
        language: str = "zh",
    ) -> None:
        self.root = root
        self.case = case or DEFAULT_CASE
        self.on_return = on_return
        self.language = language
        self.engine = MysteryEngine(self.case)
        self.statement_ids: dict[str, str] = {}
        self.evidence_ids: dict[str, str] = {}
        self.suspect_ids: dict[str, str] = {}
        # Newly archived information stays marked until the player has seen the
        # corresponding notebook entry.  These are UI-only states: the engine
        # remains responsible for the actual case progress.
        self.unread_evidence_ids: set[str] = set()
        self.unread_testimony_ids: set[str] = set()
        self.unread_timeline_location_ids: set[str] = set()
        self.image_cache: dict[str, tk.PhotoImage] = {}
        self.project_root = Path(__file__).resolve().parent

        self.root.title(f"{self.case['title']} · {self._t('case_archive')}")
        self.root.configure(bg=self.INK)
        # The three fixed game columns need this much room; the interface never
        # switches to a responsive/mobile layout.
        self.root.minsize(1180, 700)
        self._configure_styles()
        self._build_layout()
        self.render()

    def _t(self, key: str, **values: object) -> str:
        return ui_text(self.language, key, **values)

    def _configure_styles(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure(
            "Mystery.TCombobox",
            fieldbackground="#17233b",
            background="#17233b",
            foreground=self.PAPER,
            arrowcolor=self.TEAL,
            bordercolor=self.LINE,
            lightcolor=self.LINE,
            darkcolor=self.LINE,
            padding=7,
        )
        style.map("Mystery.TCombobox", fieldbackground=[("disabled", "#18233a")])

    def _panel(self, parent: tk.Widget, title: str, meta: str = "") -> tuple[tk.Frame, tk.Frame]:
        outer = tk.Frame(parent, bg=self.PANEL, highlightbackground=self.LINE, highlightthickness=1)
        header = tk.Frame(outer, bg=self.PANEL)
        header.pack(fill="x", padx=16, pady=(13, 9))
        tk.Label(header, text=title, bg=self.PANEL, fg=self.PAPER, font=(self.SERIF, 11, "bold")).pack(side="left")
        meta_label = tk.Label(header, text=meta, bg=self.PANEL, fg=self.MUTED, font=("Consolas", 8))
        meta_label.pack(side="right")
        outer.meta_label = meta_label  # type: ignore[attr-defined]
        tk.Frame(outer, height=1, bg=self.LINE).pack(fill="x")
        body = tk.Frame(outer, bg=self.PANEL)
        body.pack(fill="both", expand=True)
        return outer, body

    def _journal_page(self, parent: tk.Widget, tab_id: str, label: str) -> tk.Frame:
        """Create one page of the in-game detective notebook."""
        button = self._button(parent, label, lambda page_id=tab_id: self.show_journal_page(page_id), kind="normal")
        button.config(font=(self.FONT, 8, "bold"), padx=7, pady=7)
        button.pack(side="left", fill="x", expand=True, padx=(0, 4))
        page = tk.Frame(self.journal_pages_host, bg=self.PANEL)
        self.journal_buttons[tab_id] = button
        self.journal_pages[tab_id] = page
        return page

    def show_journal_page(self, tab_id: str) -> None:
        """Switch the visible notebook page without changing investigation state."""
        self.active_journal_page = tab_id
        for page_id, page in self.journal_pages.items():
            page.pack_forget()
            selected = page_id == tab_id
            button = self.journal_buttons[page_id]
            button.config(
                bg="#224453" if selected else self.PANEL_HIGH,
                fg=self.PAPER if selected else self.MUTED,
                activebackground="#224453" if selected else self.PANEL_HIGH,
                activeforeground=self.PAPER if selected else self.MUTED,
                highlightbackground=self.TEAL if selected else self.LINE,
            )
        self.journal_pages[tab_id].pack(fill="both", expand=True)

    def _button(self, parent: tk.Widget, text: str, command: Any, *, kind: str = "normal") -> tk.Button:
        colors = {
            "normal": (self.PANEL_HIGH, self.PAPER, self.LINE),
            "action": (self.GOLD, self.INK, self.GOLD),
            "selected": ("#224453", self.PAPER, self.TEAL),
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
            disabledforeground="#76829a",
            relief="flat",
            bd=0,
            highlightbackground=border,
            highlightthickness=1,
            cursor="hand2",
            font=(self.FONT, 9, "bold"),
            padx=11,
            pady=8,
        )

    def _build_legacy_dashboard_layout(self) -> None:
        app = tk.Frame(self.root, bg=self.INK)
        app.pack(fill="both", expand=True, padx=20, pady=16)

        header = tk.Frame(app, bg=self.INK)
        header.pack(fill="x", pady=(0, 17))
        title_box = tk.Frame(header, bg=self.INK)
        title_box.pack(side="left")
        tk.Label(title_box, text="文字推理冒险  /  进行中的案件", bg=self.INK, fg=self.TEAL, font=(self.FONT, 9, "bold")).pack(anchor="w")
        self.title_label = tk.Label(title_box, bg=self.INK, fg=self.PAPER, font=(self.SERIF, 26, "bold"))
        self.title_label.pack(anchor="w", pady=(2, 0))
        self.subtitle_label = tk.Label(title_box, bg=self.INK, fg=self.MUTED, font=(self.FONT, 10))
        self.subtitle_label.pack(anchor="w", pady=(3, 0))

        progress_box = tk.Frame(header, bg=self.INK)
        progress_box.pack(side="right")

        if self.on_return is not None:
            self._button(header, "← 返回案件档案", self.on_return, kind="quiet").pack(side="right", padx=(0, 10))
        self.progress_value = tk.Label(progress_box, width=5, bg=self.INK, fg=self.GOLD, font=("Consolas", 15, "bold"))
        self.progress_value.pack(side="left", padx=(0, 9))
        self.progress_text = tk.Label(progress_box, justify="left", bg=self.INK, fg=self.MUTED, font=(self.FONT, 9))
        self.progress_text.pack(side="left")

        objective = tk.Frame(app, bg="#172b42", highlightbackground=self.TEAL, highlightthickness=1)
        objective.pack(fill="x", pady=(0, 14))
        objective_marker = tk.Label(objective, text="下一线索", bg=self.TEAL, fg=self.INK, font=(self.FONT, 9, "bold"), padx=11, pady=10)
        objective_marker.pack(side="left", fill="y")
        objective_words = tk.Frame(objective, bg="#172b42")
        objective_words.pack(side="left", fill="x", expand=True, padx=13, pady=7)
        self.objective_label = tk.Label(objective_words, bg="#172b42", fg=self.PAPER, anchor="w", font=(self.FONT, 10, "bold"))
        self.objective_label.pack(fill="x")
        self.objective_detail = tk.Label(objective_words, bg="#172b42", fg=self.MUTED, anchor="w", font=(self.FONT, 8))
        self.objective_detail.pack(fill="x", pady=(2, 0))

        scroll_area = tk.Frame(app, bg=self.INK)
        scroll_area.pack(fill="both", expand=True)
        self.scroll_canvas = tk.Canvas(scroll_area, bg=self.INK, highlightthickness=0, bd=0)
        self.scrollbar = ttk.Scrollbar(scroll_area, orient="vertical", command=self.scroll_canvas.yview)
        self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scroll_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y", padx=(8, 0))

        self.workspace = tk.Frame(self.scroll_canvas, bg=self.INK)
        self.workspace_window = self.scroll_canvas.create_window((0, 0), window=self.workspace, anchor="nw")
        self.workspace.columnconfigure(0, weight=2, minsize=230)
        self.workspace.columnconfigure(1, weight=4, minsize=450)
        self.workspace.columnconfigure(2, weight=3, minsize=315)
        self.workspace.rowconfigure(0, weight=1)
        self.workspace.bind("<Configure>", self._refresh_scroll_region)
        self.scroll_canvas.bind("<Configure>", self._fit_workspace_to_canvas)
        self.root.bind_all("<MouseWheel>", self._on_mousewheel)
        self.root.bind_all("<Button-4>", self._on_mousewheel)
        self.root.bind_all("<Button-5>", self._on_mousewheel)

        self.left_panel, left_body = self._panel(self.workspace, "现场地图", "地点")
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        self.location_list = tk.Frame(left_body, bg=self.PANEL)
        self.location_list.pack(fill="x", padx=9, pady=9)
        rule = tk.Label(
            left_body,
            text="DETECTIVE'S RULE\nA witness account is a lead, not a fact. Cross-check every claim with independently verifiable evidence.",
            bg="#243d4a",
            fg="#dbe5e5",
            justify="left",
            anchor="w",
            font=(self.FONT, 9),
            wraplength=220,
            padx=12,
            pady=12,
        )
        rule.pack(fill="x", padx=17, pady=(8, 18))
        rule.config(text="侦探守则\n证词只是线索，并非事实。请用能独立验证的物证交叉核对每一项说法。")

        self.center_column = tk.Frame(self.workspace, bg=self.INK)
        self.center_column.rowconfigure(0, weight=1)
        self.center_column.grid(row=0, column=1, sticky="nsew", padx=8)
        scene_panel, scene_body = self._panel(self.center_column, "当前场景", "探索 • 收集 • 询问")
        scene_panel.pack(fill="both", expand=True)
        scene_body.configure(padx=24, pady=22)
        stage = tk.Frame(scene_body, bg="#101b30", highlightbackground=self.GOLD, highlightthickness=1)
        stage.pack(fill="x", pady=(0, 16))
        self.scene_image = tk.Label(
            stage,
            text="正在加载场景图",
            bg="#17233b",
            fg=self.MUTED,
            font=(self.FONT, 10),
            width=50,
            height=9,
        )
        self.scene_image.pack(fill="x")
        self.scene_code = tk.Label(scene_body, bg=self.PANEL, fg=self.TEAL, font=("Consolas", 9, "bold"))
        self.scene_code.pack(anchor="w")
        self.scene_title = tk.Label(scene_body, bg=self.PANEL, fg=self.PAPER, font=(self.SERIF, 20, "bold"))
        self.scene_title.pack(anchor="w", pady=(8, 8))
        self.scene_description = tk.Label(scene_body, bg=self.PANEL, fg="#c8d2df", justify="left", anchor="w", wraplength=520, font=(self.FONT, 10), padx=0)
        self.scene_description.pack(fill="x", anchor="w")
        self.scene_status = tk.Label(scene_body, bg=self.PANEL, fg=self.MUTED, anchor="w", font=(self.FONT, 9))
        self.scene_status.pack(fill="x", pady=(19, 8))
        self.investigate_button = self._button(scene_body, "搜查此场景", self.investigate, kind="action")
        self.investigate_button.pack(anchor="e")
        self.reward_label = tk.Label(scene_body, bg=self.PANEL, fg=self.GREEN, anchor="w", justify="left", wraplength=520, font=(self.FONT, 9))
        self.reward_label.pack(fill="x", pady=(13, 0))
        self.dialogue_frame = tk.Frame(scene_body, bg="#24314c", highlightbackground=self.TEAL, highlightthickness=1)
        self.dialogue_portrait = tk.Label(self.dialogue_frame, text="◇", bg="#24314c", fg=self.TEAL, font=(self.FONT, 15), width=9, height=5)
        self.dialogue_portrait.pack(side="left", padx=10, pady=10)
        dialogue_words = tk.Frame(self.dialogue_frame, bg="#24314c")
        dialogue_words.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=10)
        self.dialogue_name = tk.Label(dialogue_words, bg="#24314c", fg=self.TEAL, anchor="w", font=(self.FONT, 9, "bold"))
        self.dialogue_name.pack(fill="x")
        self.dialogue_text = tk.Label(dialogue_words, bg="#24314c", fg=self.PAPER, anchor="w", justify="left", wraplength=385, font=(self.FONT, 9))
        self.dialogue_text.pack(fill="x", pady=(4, 0))

        reasoning_panel, reasoning_body = self._panel(self.center_column, "推理台", "用事实检验证词")
        reasoning_panel.pack(fill="x", pady=(12, 0))
        reasoning_body.configure(padx=20, pady=17)
        selectors = tk.Frame(reasoning_body, bg=self.PANEL)
        selectors.pack(fill="x")
        selectors.columnconfigure(0, weight=1)
        selectors.columnconfigure(1, weight=1)
        tk.Label(selectors, text="选择一条证词", bg=self.PANEL, fg=self.MUTED, font=(self.FONT, 8)).grid(row=0, column=0, sticky="w")
        tk.Label(selectors, text="选择一项已发现物证", bg=self.PANEL, fg=self.MUTED, font=(self.FONT, 8)).grid(row=0, column=1, sticky="w", padx=(12, 0))
        self.statement_var = tk.StringVar()
        self.evidence_var = tk.StringVar()
        self.statement_box = ttk.Combobox(selectors, textvariable=self.statement_var, style="Mystery.TCombobox", state="disabled")
        self.evidence_box = ttk.Combobox(selectors, textvariable=self.evidence_var, style="Mystery.TCombobox", state="disabled")
        self.statement_box.grid(row=1, column=0, sticky="ew", pady=(5, 0))
        self.evidence_box.grid(row=1, column=1, sticky="ew", padx=(12, 0), pady=(5, 0))
        self.reason_note = tk.Text(reasoning_body, height=3, bg="#17233b", fg=self.PAPER, insertbackground=self.PAPER, relief="flat", highlightbackground=self.LINE, highlightthickness=1, font=(self.FONT, 9), wrap="word", padx=9, pady=7)
        self.reason_note.pack(fill="x", pady=(11, 9))
        self.reason_note.insert("1.0", "写下你的推理，例如：门禁记录推翻了安德鲁的时间线。")
        controls = tk.Frame(reasoning_body, bg=self.PANEL)
        controls.pack(fill="x")
        self.reason_hint = tk.Label(controls, text="将一条证词与一项物证配对，判断两者能否同时成立。", bg=self.PANEL, fg=self.MUTED, justify="left", font=(self.FONT, 8))
        self.reason_hint.pack(side="left")
        self.analyze_button = self._button(controls, "开始推理", self.analyze, kind="action")
        self.analyze_button.pack(side="right")
        self.analysis_label = tk.Label(reasoning_body, bg="#17343e", fg="#d7efed", justify="left", anchor="w", wraplength=530, font=(self.FONT, 9), padx=11, pady=10)
        self.analysis_label.pack(fill="x", pady=(12, 0))

        self.right_column = tk.Frame(self.workspace, bg=self.INK)
        self.right_column.grid(row=0, column=2, sticky="nsew", padx=(8, 0))
        journal_panel, journal_body = self._panel(self.right_column, "侦探笔记", "打开笔记")
        journal_panel.pack(fill="both", expand=True)
        journal_body.configure(padx=12, pady=12)
        journal_tabs = tk.Frame(journal_body, bg=self.PANEL)
        journal_tabs.pack(fill="x", pady=(0, 10))
        self.journal_pages_host = tk.Frame(journal_body, bg=self.PANEL)
        self.journal_pages_host.pack(fill="both", expand=True)
        self.journal_buttons: dict[str, tk.Button] = {}
        self.journal_pages: dict[str, tk.Frame] = {}
        self.active_journal_page = "evidence"
        evidence_page = self._journal_page(journal_tabs, "evidence", "物证")
        testimony_page = self._journal_page(journal_tabs, "testimonies", "证词")
        timeline_page = self._journal_page(journal_tabs, "timeline", "时间线")
        final_page = self._journal_page(journal_tabs, "accuse", "指控")

        self.evidence_panel, self.evidence_list = self._panel(evidence_page, "物证档案", "00 / 00")
        self.evidence_panel.pack(fill="both", expand=True)
        self.testimony_panel, self.testimony_list = self._panel(testimony_page, "人物证词", "00 / 00")
        self.testimony_panel.pack(fill="both", expand=True)
        self.timeline_panel, self.timeline_list = self._panel(timeline_page, "已知时间线", "已锁定事实")
        self.timeline_panel.pack(fill="both", expand=True)
        final_panel, final_body = self._panel(final_page, "最终指控", "结案")
        final_panel.pack(fill="both", expand=True)
        final_body.configure(padx=15, pady=14)
        self.final_hint = tk.Label(final_body, bg=self.PANEL, fg=self.MUTED, justify="left", anchor="w", wraplength=300, font=(self.FONT, 9))
        self.final_hint.pack(fill="x", pady=(0, 8))
        final_controls = tk.Frame(final_body, bg=self.PANEL)
        final_controls.pack(fill="x")
        self.suspect_var = tk.StringVar()
        self.suspect_box = ttk.Combobox(final_controls, textvariable=self.suspect_var, style="Mystery.TCombobox", state="disabled")
        self.suspect_box.pack(side="left", fill="x", expand=True)
        self.accuse_button = self._button(final_controls, "提交指控", self.accuse, kind="action")
        self.accuse_button.pack(side="left", padx=(8, 0))
        self.case_result = tk.Label(final_body, bg="#1b3a31", fg="#d9f4df", justify="left", anchor="w", wraplength=300, font=(self.FONT, 9), padx=10, pady=9)
        self.case_result.pack(fill="x", pady=(10, 0))
        self.reset_button = self._button(final_body, "重新开始案件", self.reset_game, kind="quiet")
        self.reset_button.pack(anchor="e", pady=(10, 0))

        self.show_journal_page("evidence")

        self.toast = tk.Label(app, bg="#173b42", fg="#eef7f5", font=(self.FONT, 9), padx=12, pady=7)
        self.toast.pack(anchor="e", pady=(10, 0))

    def _build_layout(self) -> None:
        """Build the current scene-first investigation interface."""
        self._build_adventure_layout()

    def _build_adventure_layout(self) -> None:
        """Build a scene-first layout rather than a desktop-style dashboard."""
        app = tk.Frame(self.root, bg=self.INK)
        app.pack(fill="both", expand=True, padx=18, pady=14)

        header = tk.Frame(app, bg=self.INK)
        header.pack(fill="x", pady=(0, 12))
        title_box = tk.Frame(header, bg=self.INK)
        title_box.pack(side="left")
        tk.Label(title_box, text=self._t("running_case"), bg=self.INK, fg=self.TEAL, font=(self.FONT, 9, "bold")).pack(anchor="w")
        self.title_label = tk.Label(title_box, bg=self.INK, fg=self.PAPER, font=(self.SERIF, 25, "bold"))
        self.title_label.pack(anchor="w", pady=(2, 0))
        self.subtitle_label = tk.Label(title_box, bg=self.INK, fg=self.MUTED, font=(self.FONT, 9))
        self.subtitle_label.pack(anchor="w", pady=(2, 0))

        hud = tk.Frame(header, bg="#172b42", highlightbackground=self.LINE, highlightthickness=1, padx=12, pady=8)
        hud.pack(side="right")
        if self.on_return is not None:
            self._button(hud, self._t("back_archive"), self.on_return, kind="quiet").pack(side="right", padx=(10, 0))
        self.progress_value = tk.Label(hud, width=5, bg="#172b42", fg=self.GOLD, font=("Consolas", 15, "bold"))
        self.progress_value.pack(side="left", padx=(0, 8))
        self.progress_text = tk.Label(hud, justify="left", bg="#172b42", fg=self.MUTED, font=(self.FONT, 8))
        self.progress_text.pack(side="left")

        objective = tk.Frame(app, bg="#173b42", highlightbackground=self.TEAL, highlightthickness=1)
        objective.pack(fill="x", pady=(0, 12))
        tk.Label(objective, text=self._t("objective"), bg=self.TEAL, fg=self.INK, font=(self.FONT, 9, "bold"), padx=14, pady=10).pack(side="left", fill="y")
        objective_words = tk.Frame(objective, bg="#173b42")
        objective_words.pack(side="left", fill="x", expand=True, padx=14, pady=7)
        self.objective_label = tk.Label(objective_words, bg="#173b42", fg=self.PAPER, anchor="w", font=(self.FONT, 10, "bold"))
        self.objective_label.pack(fill="x")
        self.objective_detail = tk.Label(objective_words, bg="#173b42", fg=self.MUTED, anchor="w", font=(self.FONT, 8))
        self.objective_detail.pack(fill="x", pady=(2, 0))

        scroll_area = tk.Frame(app, bg=self.INK)
        scroll_area.pack(fill="both", expand=True)
        self.scroll_canvas = tk.Canvas(scroll_area, bg=self.INK, highlightthickness=0, bd=0)
        self.scrollbar = ttk.Scrollbar(scroll_area, orient="vertical", command=self.scroll_canvas.yview)
        self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scroll_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y", padx=(8, 0))

        self.workspace = tk.Frame(self.scroll_canvas, bg=self.INK)
        self.workspace_window = self.scroll_canvas.create_window((0, 0), window=self.workspace, anchor="nw")
        self.workspace.columnconfigure(0, weight=0, minsize=245)
        self.workspace.columnconfigure(1, weight=1, minsize=820)
        self.workspace.rowconfigure(0, weight=0)
        self.workspace.rowconfigure(1, weight=1)
        self.workspace.bind("<Configure>", self._refresh_scroll_region)
        self.scroll_canvas.bind("<Configure>", self._fit_workspace_to_canvas)
        self.root.bind_all("<MouseWheel>", self._on_mousewheel)
        self.root.bind_all("<Button-4>", self._on_mousewheel)
        self.root.bind_all("<Button-5>", self._on_mousewheel)

        scene_panel, scene_body = self._panel(self.workspace, self._t("current_scene"), self._t("immersive_scene"))
        scene_panel.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        scene_body.configure(padx=20, pady=18)
        stage = tk.Frame(scene_body, bg="#0d1728", highlightbackground=self.GOLD, highlightthickness=1)
        stage.pack(fill="x")
        self.scene_image = tk.Label(stage, text=self._t("loading_scene"), bg="#17233b", fg=self.MUTED, font=(self.FONT, 10), width=90, height=15)
        self.scene_image.pack(anchor="center")

        scene_details = tk.Frame(scene_body, bg=self.PANEL)
        scene_details.pack(fill="x", pady=(16, 0))
        self.scene_code = tk.Label(scene_details, bg=self.PANEL, fg=self.TEAL, font=(self.FONT, 9, "bold"))
        self.scene_code.pack(anchor="w")
        self.scene_title = tk.Label(scene_details, bg=self.PANEL, fg=self.PAPER, font=(self.SERIF, 22, "bold"))
        self.scene_title.pack(anchor="w", pady=(5, 6))
        self.scene_description = tk.Label(scene_details, bg=self.PANEL, fg="#c8d2df", justify="left", anchor="w", wraplength=960, font=(self.FONT, 10))
        self.scene_description.pack(fill="x")
        scene_actions = tk.Frame(scene_details, bg=self.PANEL)
        scene_actions.pack(fill="x", pady=(14, 4))
        self.scene_status = tk.Label(scene_actions, bg=self.PANEL, fg=self.MUTED, anchor="w", font=(self.FONT, 9))
        self.scene_status.pack(side="left", fill="x", expand=True)
        self.investigate_button = self._button(scene_actions, self._t("investigate"), self.investigate, kind="action")
        self.investigate_button.pack(side="right")
        self.reward_label = tk.Label(scene_details, bg="#20394a", fg="#d8f4ef", anchor="w", justify="left", wraplength=940, font=(self.FONT, 9), padx=12, pady=9)
        self.reward_label.pack(fill="x", pady=(10, 0))

        self.dialogue_frame = tk.Frame(scene_body, bg="#243d4a", highlightbackground=self.TEAL, highlightthickness=1)
        portrait_stage = tk.Frame(self.dialogue_frame, bg="#101b30", highlightbackground=self.GOLD, highlightthickness=1)
        portrait_stage.pack(side="left", padx=14, pady=14)
        self.dialogue_portrait = tk.Label(portrait_stage, text="◇", bg="#101b30", fg=self.TEAL, font=(self.FONT, 15), width=12, height=8)
        self.dialogue_portrait.pack(padx=4, pady=(4, 0))
        dialogue_words = tk.Frame(self.dialogue_frame, bg="#243d4a")
        dialogue_words.pack(side="left", fill="both", expand=True, padx=(4, 20), pady=20)
        self.dialogue_name = tk.Label(dialogue_words, bg="#243d4a", fg=self.TEAL, anchor="w", font=(self.FONT, 12, "bold"))
        self.dialogue_name.pack(fill="x")
        self.dialogue_text = tk.Label(dialogue_words, bg="#243d4a", fg=self.PAPER, anchor="w", justify="left", wraplength=700, font=(self.FONT, 11))
        self.dialogue_text.pack(fill="x", pady=(10, 0))

        self.left_panel, left_body = self._panel(self.workspace, self._t("map"), self._t("next_location"))
        self.left_panel.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        self.location_list = tk.Frame(left_body, bg=self.PANEL)
        self.location_list.pack(fill="x", padx=10, pady=10)
        rule = tk.Label(
            left_body,
            text=self._t("detective_rule"),
            bg="#243d4a",
            fg="#dbe5e5",
            justify="left",
            anchor="w",
            font=(self.FONT, 9),
            wraplength=215,
            padx=12,
            pady=12,
        )
        rule.pack(fill="x", padx=16, pady=(8, 16))

        self.right_column = tk.Frame(self.workspace, bg=self.INK)
        self.right_column.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        journal_panel, journal_body = self._panel(self.right_column, self._t("journal"), self._t("journal_meta"))
        journal_panel.pack(fill="both", expand=True)
        journal_body.configure(padx=14, pady=14)
        journal_tabs = tk.Frame(journal_body, bg=self.PANEL)
        journal_tabs.pack(fill="x", pady=(0, 12))
        self.journal_pages_host = tk.Frame(journal_body, bg=self.PANEL)
        self.journal_pages_host.pack(fill="both", expand=True)
        self.journal_buttons = {}
        self.journal_pages = {}
        self.active_journal_page = "evidence"
        evidence_page = self._journal_page(journal_tabs, "evidence", self._t("evidence"))
        testimony_page = self._journal_page(journal_tabs, "testimonies", self._t("testimonies"))
        timeline_page = self._journal_page(journal_tabs, "timeline", self._t("timeline"))
        reasoning_page = self._journal_page(journal_tabs, "reasoning", self._t("reasoning"))
        final_page = self._journal_page(journal_tabs, "accuse", self._t("accuse"))

        self.evidence_panel, self.evidence_list = self._panel(evidence_page, self._t("evidence_archive"), "00 / 00")
        self.evidence_panel.pack(fill="both", expand=True)
        self.testimony_panel, self.testimony_list = self._panel(testimony_page, self._t("testimony_archive"), "00 / 00")
        self.testimony_panel.pack(fill="both", expand=True)
        self.timeline_panel, self.timeline_list = self._panel(timeline_page, self._t("known_timeline"), self._t("locked_facts"))
        self.timeline_panel.pack(fill="both", expand=True)

        reasoning_panel, reasoning_body = self._panel(reasoning_page, self._t("reasoning_desk"), self._t("reasoning_meta"))
        reasoning_panel.pack(fill="both", expand=True)
        reasoning_body.configure(padx=18, pady=16)
        selectors = tk.Frame(reasoning_body, bg=self.PANEL)
        selectors.pack(fill="x")
        selectors.columnconfigure(0, weight=1)
        selectors.columnconfigure(1, weight=1)
        tk.Label(selectors, text=self._t("statement_select"), bg=self.PANEL, fg=self.MUTED, font=(self.FONT, 9)).grid(row=0, column=0, sticky="w")
        tk.Label(selectors, text=self._t("evidence_select"), bg=self.PANEL, fg=self.MUTED, font=(self.FONT, 9)).grid(row=0, column=1, sticky="w", padx=(14, 0))
        self.statement_var = tk.StringVar()
        self.evidence_var = tk.StringVar()
        self.statement_box = ttk.Combobox(selectors, textvariable=self.statement_var, style="Mystery.TCombobox", state="disabled")
        self.evidence_box = ttk.Combobox(selectors, textvariable=self.evidence_var, style="Mystery.TCombobox", state="disabled")
        self.statement_box.grid(row=1, column=0, sticky="ew", pady=(6, 0))
        self.evidence_box.grid(row=1, column=1, sticky="ew", padx=(14, 0), pady=(6, 0))
        self.reason_note = tk.Text(reasoning_body, height=4, bg="#17233b", fg=self.PAPER, insertbackground=self.PAPER, relief="flat", highlightbackground=self.LINE, highlightthickness=1, font=(self.FONT, 10), wrap="word", padx=10, pady=8)
        self.reason_note.pack(fill="x", pady=(14, 10))
        self.reason_note.insert("1.0", self._t("reason_placeholder"))
        controls = tk.Frame(reasoning_body, bg=self.PANEL)
        controls.pack(fill="x")
        self.reason_hint = tk.Label(controls, text=self._t("reason_hint"), bg=self.PANEL, fg=self.MUTED, justify="left", font=(self.FONT, 9))
        self.reason_hint.pack(side="left")
        self.analyze_button = self._button(controls, self._t("analyze"), self.analyze, kind="action")
        self.analyze_button.pack(side="right")
        self.analysis_label = tk.Label(reasoning_body, bg="#17343e", fg="#d7efed", justify="left", anchor="w", wraplength=700, font=(self.FONT, 10), padx=12, pady=11)
        self.analysis_label.pack(fill="x", pady=(14, 0))

        final_panel, final_body = self._panel(final_page, self._t("final_accusation"), self._t("close_case"))
        final_panel.pack(fill="both", expand=True)
        final_body.configure(padx=18, pady=16)
        self.final_hint = tk.Label(final_body, bg=self.PANEL, fg=self.MUTED, justify="left", anchor="w", wraplength=720, font=(self.FONT, 10))
        self.final_hint.pack(fill="x", pady=(0, 10))
        final_controls = tk.Frame(final_body, bg=self.PANEL)
        final_controls.pack(fill="x")
        self.suspect_var = tk.StringVar()
        self.suspect_box = ttk.Combobox(final_controls, textvariable=self.suspect_var, style="Mystery.TCombobox", state="disabled")
        self.suspect_box.pack(side="left", fill="x", expand=True)
        self.accuse_button = self._button(final_controls, self._t("submit_accusation"), self.accuse, kind="action")
        self.accuse_button.pack(side="left", padx=(10, 0))
        self.case_result = tk.Label(final_body, bg="#1b3a31", fg="#d9f4df", justify="left", anchor="w", wraplength=720, font=(self.FONT, 10), padx=12, pady=11)
        self.case_result.pack(fill="x", pady=(12, 0))
        self.reset_button = self._button(final_body, self._t("reset_case"), self.reset_game, kind="quiet")
        self.reset_button.pack(anchor="e", pady=(12, 0))

        self.show_journal_page("evidence")
        self.toast = tk.Label(app, bg="#173b42", fg="#eef7f5", font=(self.FONT, 9), padx=12, pady=7)
        self.toast.pack(anchor="e", pady=(10, 0))

    @staticmethod
    def _clear(frame: tk.Widget) -> None:
        for child in frame.winfo_children():
            child.destroy()

    def _center_wrap(self) -> int:
        return 520

    def _right_wrap(self) -> int:
        return 650

    def _scene_image_scale(self) -> int:
        return 1

    def _refresh_scroll_region(self, _event: tk.Event[tk.Misc]) -> None:
        self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))

    def _fit_workspace_to_canvas(self, event: tk.Event[tk.Misc]) -> None:
        self.scroll_canvas.itemconfigure(self.workspace_window, width=event.width)
        self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))

    def _on_mousewheel(self, event: tk.Event[tk.Misc]) -> str:
        if getattr(event, "num", None) == 4:
            self.scroll_canvas.yview_scroll(-3, "units")
        elif getattr(event, "num", None) == 5:
            self.scroll_canvas.yview_scroll(3, "units")
        elif getattr(event, "delta", 0):
            self.scroll_canvas.yview_scroll(-3 if event.delta > 0 else 3, "units")
        return "break"

    def render(self) -> None:
        self.title_label.config(text=self.case["title"])
        self.subtitle_label.config(text=self.case["subtitle"])
        self.progress_value.config(text=f"{self.engine.progress_percent}%")
        progress_key = "progress_solved" if self.engine.solved else "progress_contradiction" if self.engine.contradiction_found else "progress_start" if not self.engine.investigated else "progress_accumulating"
        self.progress_text.config(
            text=f"{self._t(progress_key)}\n{self._t('progress_detail', count=len(self.engine.investigated), total=len(self.case['locations']))}"
        )
        self._render_objective()
        self._render_locations()
        self._render_scene()
        self._render_evidence()
        self._render_testimonies()
        self._render_timeline()
        self._render_reasoning_controls()
        self._render_final_controls()

    def _render_objective(self) -> None:
        """Keep one clear player-facing action visible above the investigation board."""
        location = self.engine.current_location
        if self.engine.solved:
            title = self._t("objective_solved")
            detail = self._t("objective_solved_detail")
        elif location["id"] not in self.engine.investigated:
            title = self._t("objective_search", location=location["name"])
            detail = self._t("objective_search_detail", evidence=len(location["evidence"]), testimonies=len(location["testimonies"]))
        elif not self.engine.contradiction_found:
            title = self._t("objective_reason")
            detail = self._t("objective_reason_detail")
        elif not self.engine.has_required_contradictions:
            title = self._t("objective_more_contradictions")
            detail = self._t("objective_more_contradictions_detail")
        elif self.engine.can_accuse:
            title = self._t("objective_accuse")
            detail = self._t("objective_accuse_detail")
        else:
            remaining = len(set(self.case["final_accusation"]["required_evidence"]) - self.engine.discovered_evidence)
            title = self._t("objective_evidence")
            detail = self._t("objective_evidence_detail", remaining=remaining)
        self.objective_label.config(text=title)
        self.objective_detail.config(text=detail)

    def _render_locations(self) -> None:
        self.left_panel.meta_label.config(text=self._t("location_count", count=len(self.case["locations"])))  # type: ignore[attr-defined]
        self._clear(self.location_list)
        for index, location in enumerate(self.case["locations"], start=1):
            done = location["id"] in self.engine.investigated
            current = location["id"] == self.engine.selected_location
            suffix = "  ✓" if done else ""
            button = self._button(
                self.location_list,
                f"{index:02d}  {location['name']}{suffix}\n      {location['meta']}",
                lambda item_id=location["id"]: self.select_location(item_id),
                kind="selected" if current else "normal",
            )
            button.config(anchor="w", justify="left", padx=10, pady=9)
            button.pack(fill="x", pady=3)

    def _render_scene(self) -> None:
        location = self.engine.current_location
        complete = location["id"] in self.engine.investigated
        self._set_image(self.scene_image, location.get("background"), scale=self._scene_image_scale(), fallback=self._t("scene_image_error"))
        self.scene_code.config(text=location["code"])
        self.scene_title.config(text=location["title"])
        self.scene_description.config(text=location["description"])
        if complete:
            self.scene_status.config(text=self._t("completed_scene"))
            self.investigate_button.config(text=self._t("completed_button"), state="disabled")
            evidence_by_id = {item["id"]: item for item in self.case["evidence"]}
            case_facts = [self._name_for(item_id) for item_id in location["evidence"] if evidence_by_id[item_id].get("kind", "case") == "case"]
            observations = [self._name_for(item_id) for item_id in location["evidence"] if evidence_by_id[item_id].get("kind") == "distractor"]
            links = [self._name_for(item_id) for item_id in location["evidence"] if evidence_by_id[item_id].get("kind") == "cross-scene"]
            summary = []
            if case_facts:
                summary.append(self._t("archived_facts") + " · ".join(case_facts))
            if observations:
                summary.append(self._t("other_observations") + " · ".join(observations))
            if links:
                summary.append(self._t("possible_links") + " · ".join(links))
            if location["testimonies"]:
                summary.append(self._t("new_testimonies") + " · ".join(self._name_for(item_id) for item_id in location["testimonies"]))
            self.reward_label.config(text="\n".join(summary))
            self._render_scene_dialogue(location)
        else:
            evidence_count = len(location["evidence"])
            statement_text = self._t("and_testimonies") if location["testimonies"] else ""
            self.scene_status.config(text=self._t("discoverable", count=evidence_count, testimonies=statement_text))
            self.investigate_button.config(text=self._t("investigate"), state="normal")
            self.reward_label.config(text="")
            self.dialogue_frame.pack_forget()

    def _render_scene_dialogue(self, location: dict[str, Any]) -> None:
        if not location["testimonies"]:
            self.dialogue_frame.pack_forget()
            return
        testimony_id = location["testimonies"][0]
        testimony = next(item for item in self.case["testimonies"] if item["id"] == testimony_id)
        # The source portraits are high-resolution.  Keep the scene portrait
        # prominent without allowing it to dominate the dialogue panel.
        self._set_image(
            self.dialogue_portrait,
            testimony.get("portrait"),
            scale=self.DIALOGUE_PORTRAIT_SCALE,
            fallback="◇",
        )
        self.dialogue_name.config(text=f"{testimony['person']} · {testimony['role']}")
        self.dialogue_text.config(text=testimony["text"])
        self.dialogue_frame.pack(fill="x", pady=(12, 0))

    def _render_evidence(self) -> None:
        self.evidence_panel.meta_label.config(text=f"{len(self.engine.discovered_evidence):02d} / {len(self.case['evidence']):02d}")  # type: ignore[attr-defined]
        self._clear(self.evidence_list)
        discovered_items = [item for item in self.case["evidence"] if item["id"] in self.engine.discovered_evidence]
        if not discovered_items:
            tk.Label(
                self.evidence_list,
                text=self._t("empty_evidence"),
                bg="#243d4a",
                fg=self.MUTED,
                justify="left",
                anchor="w",
                font=(self.FONT, 10),
                padx=14,
                pady=15,
            ).pack(fill="x", padx=10, pady=10)
            return
        for item in discovered_items:
            unlocked = True
            kind = item.get("kind", "case")
            background = {
                "case": "#24314c",
                "distractor": "#2c3347",
                "cross-scene": "#1e3b46",
            }.get(kind, "#24314c") if unlocked else self.PANEL
            row = tk.Frame(self.evidence_list, bg=background, padx=10, pady=8)
            row.pack(fill="x", padx=9, pady=3)
            self._read_marker(row, item["id"] in self.unread_evidence_ids)
            tk.Label(row, text=item["icon"] if unlocked else "◇", bg=row["bg"], fg=self.GOLD if unlocked else self.MUTED, font=(self.FONT, 12)).pack(side="left", padx=(0, 8))
            words = tk.Frame(row, bg=row["bg"])
            words.pack(side="left", fill="x", expand=True)
            title_row = tk.Frame(words, bg=row["bg"])
            title_row.pack(fill="x")
            tk.Label(title_row, text=item["name"] if unlocked else self._t("unidentified_evidence"), bg=row["bg"], fg=self.PAPER, anchor="w", font=(self.FONT, 9, "bold")).pack(side="left", fill="x", expand=True)
            if unlocked:
                kind_label = {
                    "case": self._t("case_fact"),
                    "distractor": self._t("observation"),
                    "cross-scene": self._t("cross_scene"),
                }.get(kind, self._t("evidence"))
                tk.Label(title_row, text=kind_label, bg=row["bg"], fg=self.TEAL if kind == "cross-scene" else self.GOLD if kind == "case" else self.MUTED, font=("Consolas", 7, "bold")).pack(side="right")
            detail = self._t("locked_evidence")
            if unlocked:
                if kind == "cross-scene":
                    if self.engine.is_cross_scene_link_resolved(item):
                        detail = item["connection_detail"]
                    else:
                        related_location = next(site["name"] for site in self.case["locations"] if site["id"] == item["related_location"])
                        detail = self._t("unresolved_link", location=related_location, detail=item["partial_detail"])
                else:
                    detail = item["detail"]
            tk.Label(words, text=detail, bg=row["bg"], fg=self.MUTED, anchor="w", justify="left", wraplength=max(155, self._right_wrap() - 52), font=(self.FONT, 8)).pack(fill="x", pady=(2, 0))
            self._dismiss_unread_on_inspect(row, self.unread_evidence_ids, item["id"], self._render_evidence)

    def _render_testimonies(self) -> None:
        self.testimony_panel.meta_label.config(text=f"{len(self.engine.discovered_testimonies):02d} / {len(self.case['testimonies']):02d}")  # type: ignore[attr-defined]
        self._clear(self.testimony_list)
        discovered_items = [item for item in self.case["testimonies"] if item["id"] in self.engine.discovered_testimonies]
        if not discovered_items:
            tk.Label(
                self.testimony_list,
                text=self._t("empty_testimony"),
                bg="#243d4a",
                fg=self.MUTED,
                justify="left",
                anchor="w",
                font=(self.FONT, 10),
                padx=14,
                pady=15,
            ).pack(fill="x", padx=10, pady=10)
            return
        for item in discovered_items:
            unlocked = True
            row = tk.Frame(self.testimony_list, bg="#24314c" if unlocked else self.PANEL, padx=10, pady=9)
            row.pack(fill="x", padx=9, pady=3)
            self._read_marker(row, item["id"] in self.unread_testimony_ids)
            portrait = tk.Label(row, text="◇", bg=row["bg"], fg=self.TEAL if unlocked else self.MUTED, font=(self.FONT, 12), width=5, height=4)
            if unlocked:
                self._set_image(
                    portrait,
                    item.get("portrait"),
                    scale=self.NOTEBOOK_PORTRAIT_SCALE,
                    fallback="◇",
                )
            portrait.pack(side="left", padx=(0, 8))
            top = tk.Frame(row, bg=row["bg"])
            top.pack(fill="x", expand=True)
            tk.Label(top, text=item["person"] if unlocked else self._t("unknown_witness"), bg=row["bg"], fg=self.PAPER, font=(self.FONT, 9, "bold")).pack(side="left")
            tk.Label(top, text=item["role"] if unlocked else self._t("locked"), bg=row["bg"], fg=self.TEAL if unlocked else self.MUTED, font=(self.FONT, 7)).pack(side="right")
            tk.Label(top, text=item["text"] if unlocked else self._t("unlock_testimony"), bg=row["bg"], fg="#cad2df", justify="left", anchor="w", wraplength=max(130, self._right_wrap() - 105), font=(self.FONT, 8)).pack(fill="x", pady=(5, 0))
            self._dismiss_unread_on_inspect(row, self.unread_testimony_ids, item["id"], self._render_testimonies)

    def _render_timeline(self) -> None:
        self._clear(self.timeline_list)
        for location in self.case["locations"]:
            if location["id"] not in self.engine.investigated:
                continue
            time, text = location["timeline"].split(" ", 1)
            row = tk.Frame(self.timeline_list, bg=self.PANEL, padx=12, pady=5)
            row.pack(fill="x")
            self._read_marker(row, location["id"] in self.unread_timeline_location_ids)
            tk.Label(row, text=time, bg=self.PANEL, fg=self.GOLD, font=("Consolas", 8)).pack(side="left")
            tk.Label(row, text=text, bg=self.PANEL, fg="#c8d2df", justify="left", anchor="w", wraplength=max(150, self._right_wrap() - 65), font=(self.FONT, 8)).pack(side="left", fill="x", expand=True, padx=(10, 0))
            self._dismiss_unread_on_inspect(row, self.unread_timeline_location_ids, location["id"], self._render_timeline)

    def _read_marker(self, parent: tk.Widget, is_unread: bool) -> None:
        """Reserve a consistent slot for the red notebook notification dot."""
        tk.Label(
            parent,
            text="●" if is_unread else " ",
            bg=parent["bg"],
            fg="#f1606b",
            font=(self.FONT, 10, "bold"),
            width=2,
        ).pack(side="left", padx=(0, 2))

    def _dismiss_unread_on_inspect(
        self,
        row: tk.Widget,
        unread_ids: set[str],
        item_id: str,
        refresh: Any,
    ) -> None:
        """Mark an entry read when its row (or any child) receives attention."""
        def dismiss(_event: tk.Event[Any] | None = None) -> None:
            if item_id not in unread_ids:
                return
            unread_ids.discard(item_id)
            # Repaint after the current Tk event has finished so a hover never
            # removes a widget while it is still being dispatched.
            self.root.after_idle(refresh)

        def bind_descendants(widget: tk.Widget) -> None:
            widget.bind("<Enter>", dismiss, add="+")
            widget.bind("<Button-1>", dismiss, add="+")
            for child in widget.winfo_children():
                bind_descendants(child)

        bind_descendants(row)

    def _render_reasoning_controls(self) -> None:
        old_statement, old_evidence = self.statement_var.get(), self.evidence_var.get()
        self.statement_ids = {f"{item['person']} · {item['text']}": item["id"] for item in self.engine.available_testimonies()}
        self.evidence_ids = {item["name"]: item["id"] for item in self.engine.available_evidence()}
        self.statement_box["values"] = list(self.statement_ids)
        self.evidence_box["values"] = list(self.evidence_ids)
        ready = bool(self.statement_ids and self.evidence_ids)
        state = "readonly" if ready else "disabled"
        self.statement_box.config(state=state)
        self.evidence_box.config(state=state)
        self.analyze_button.config(state="normal" if ready else "disabled")
        self.statement_var.set(old_statement if old_statement in self.statement_ids else "")
        self.evidence_var.set(old_evidence if old_evidence in self.evidence_ids else "")
        if self.engine.contradiction_found:
            self.reason_hint.config(text=self._t("reason_confirmed"))

    def _render_final_controls(self) -> None:
        self.suspect_ids = {item["name"]: item["id"] for item in self.case["suspects"]}
        self.suspect_box["values"] = list(self.suspect_ids)
        enabled = self.engine.can_accuse
        self.suspect_box.config(state="readonly" if enabled else "disabled")
        self.accuse_button.config(state="normal" if enabled else "disabled")
        if self.engine.solved:
            hint = self._t("final_solved")
        elif enabled:
            hint = self._t("final_ready")
        elif self.engine.contradiction_found and not self.engine.has_required_contradictions:
            hint = self._t("final_need_contradiction")
        elif self.engine.contradiction_found:
            remaining = len(set(self.case["final_accusation"]["required_evidence"]) - self.engine.discovered_evidence)
            hint = self._t("final_remaining", remaining=remaining)
        else:
            hint = self._t("final_find_contradiction")
        self.final_hint.config(text=hint)

    def _name_for(self, item_id: str) -> str:
        for item in [*self.case["evidence"], *self.case["testimonies"]]:
            if item["id"] == item_id:
                return item.get("name", item.get("person", item_id))
        return item_id

    def _set_image(self, label: tk.Label, relative_path: str | None, *, scale: int, fallback: str) -> None:
        """Load a project PNG once and retain it so tkinter does not discard it."""
        if not relative_path:
            label.config(image="", text=fallback)
            return
        cache_key = f"{relative_path}:{scale}"
        try:
            if cache_key not in self.image_cache:
                source = self.project_root / relative_path
                image = tk.PhotoImage(file=source)
                self.image_cache[cache_key] = image.subsample(scale, scale)
            label.config(image=self.image_cache[cache_key], text="", width=0, height=0)
        except tk.TclError:
            label.config(image="", text=fallback)

    def select_location(self, location_id: str) -> None:
        self.engine.select_location(location_id)
        self.render()

    def investigate(self) -> None:
        found = self.engine.investigate_current_location()
        if found:
            evidence_ids = {item["id"] for item in self.case["evidence"]}
            testimony_ids = {item["id"] for item in self.case["testimonies"]}
            self.unread_evidence_ids.update(set(found) & evidence_ids)
            self.unread_testimony_ids.update(set(found) & testimony_ids)
            self.unread_timeline_location_ids.add(self.engine.current_location["id"])
            self.toast.config(text=self._t("investigation_complete", location=self.engine.current_location["name"]))
        self.render()

    def analyze(self) -> None:
        statement_id = self.statement_ids.get(self.statement_var.get(), "")
        evidence_id = self.evidence_ids.get(self.evidence_var.get(), "")
        result = self.engine.analyze(statement_id, evidence_id)
        self._show_analysis(result)
        self.render()

    def _show_analysis(self, result: Analysis) -> None:
        if result.outcome in {"error", "failure"}:
            background, foreground = "#4a252e", "#ffd9da"
        elif result.outcome == "contradiction":
            background, foreground = "#17434a", "#d7efed"
        else:
            background, foreground = "#263044", "#d5dde9"
        self.analysis_label.config(text=result.message, bg=background, fg=foreground)

    def accuse(self) -> None:
        suspect_id = self.suspect_ids.get(self.suspect_var.get(), "")
        result = self.engine.accuse(suspect_id)
        colors = ("#1b3a31", "#d9f4df") if result.outcome == "success" else ("#4a252e", "#ffd9da")
        self.case_result.config(text=result.message, bg=colors[0], fg=colors[1])
        if result.outcome == "success":
            self.toast.config(text=self._t("case_solved_toast"))
        self.render()

    def reset_game(self) -> None:
        self.engine = MysteryEngine(self.case)
        self.unread_evidence_ids.clear()
        self.unread_testimony_ids.clear()
        self.unread_timeline_location_ids.clear()
        self.statement_var.set("")
        self.evidence_var.set("")
        self.suspect_var.set("")
        self.reason_note.delete("1.0", "end")
        self.reason_note.insert("1.0", self._t("reason_placeholder"))
        self.analysis_label.config(text="", bg="#17343e")
        self.case_result.config(text="", bg="#1b3a31")
        self.toast.config(text=self._t("case_reset"))
        self.render()


def main() -> None:
    from launcher import launch

    launch()


if __name__ == "__main__":
    main()
