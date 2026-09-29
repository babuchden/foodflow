import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

from database import Database


BG = "#F4F6F8"
PANEL = "#FFFFFF"
TEXT = "#171A1F"
MUTED = "#697386"
DARK = "#121A22"
DARK_ACTIVE = "#222D36"
ACCENT = "#168A4A"
ACCENT_HOVER = "#11743E"
ACCENT_SOFT = "#E8F5ED"
BORDER = "#DDE2E7"
SOFT = "#F8FAFB"
BLUE = "#2878D0"
ORANGE = "#D88912"
GREEN = "#168A4A"
RED = "#D43C3C"


class FoodDeliveryAIS:
    def __init__(self, root):
        self.root = root
        self.db = Database()
        self.root.title("FoodFlow — АІС управління доставкою готової їжі")
        self.root.geometry("1280x780")
        self.root.minsize(1080, 680)
        self.root.configure(bg=BG)
        self.section = "Огляд"
        self.nav_buttons = {}
        self.configure_styles()
        self.build_layout()
        self.show_dashboard()

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background=PANEL,
            fieldbackground=PANEL,
            foreground=TEXT,
            rowheight=38,
            borderwidth=0,
            relief="flat",
            font=("Segoe UI", 9),
        )
        style.configure(
            "Treeview.Heading",
            background="#F1F4F6",
            foreground="#374151",
            borderwidth=0,
            relief="flat",
            padding=(8, 11),
            font=("Segoe UI", 9, "bold"),
        )
        style.map(
            "Treeview",
            background=[("selected", "#E8F5ED")],
            foreground=[("selected", TEXT)],
        )
        style.configure(
            "TCombobox",
            fieldbackground=PANEL,
            background=PANEL,
            foreground=TEXT,
            bordercolor=BORDER,
            lightcolor=BORDER,
            darkcolor=BORDER,
            arrowcolor="#4B5563",
            padding=8,
        )
        style.map("TCombobox", fieldbackground=[("readonly", PANEL)])
        style.configure(
            "Vertical.TScrollbar",
            background="#E5E9ED",
            troughcolor=PANEL,
            bordercolor=PANEL,
            arrowcolor="#64748B",
        )

    def build_layout(self):
        self.sidebar = tk.Frame(self.root, bg=DARK, width=218)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        brand = tk.Frame(self.sidebar, bg=DARK)
        brand.pack(fill="x", padx=24, pady=(27, 31))
        brand_line = tk.Frame(brand, bg=DARK)
        brand_line.pack(fill="x")
        logo = tk.Label(
            brand_line,
            text="▣",
            bg=DARK,
            fg=ACCENT,
            font=("Segoe UI Symbol", 20, "bold"),
        )
        logo.pack(side="left", padx=(0, 9))
        tk.Label(
            brand_line,
            text="Food",
            bg=DARK,
            fg="white",
            font=("Segoe UI", 19, "bold"),
        ).pack(side="left")
        tk.Label(
            brand_line,
            text="Flow",
            bg=DARK,
            fg="#36B96F",
            font=("Segoe UI", 19, "bold"),
        ).pack(side="left")
        tk.Label(
            brand,
            text="Доставка під контролем",
            bg=DARK,
            fg="#9AA5B1",
            font=("Segoe UI", 8),
        ).pack(anchor="w", padx=35, pady=(2, 0))

        items = [
            ("Огляд", "⌂", self.show_dashboard),
            ("Замовлення", "▤", self.show_orders),
            ("Клієнти", "♙", self.show_customers),
            ("Кур’єри", "▣", self.show_couriers),
            ("Меню", "≡", self.show_menu),
        ]

        for label, icon, command in items:
            row = tk.Frame(self.sidebar, bg=DARK)
            row.pack(fill="x", pady=2)
            indicator = tk.Frame(row, bg=DARK, width=4)
            indicator.pack(side="left", fill="y")
            button = tk.Button(
                row,
                text=f"{icon}    {label}",
                command=command,
                anchor="w",
                padx=19,
                pady=12,
                bd=0,
                relief="flat",
                bg=DARK,
                fg="#D3D9DF",
                activebackground=DARK_ACTIVE,
                activeforeground="white",
                font=("Segoe UI", 10),
                cursor="hand2",
            )
            button.pack(side="left", fill="x", expand=True)
            self.nav_buttons[label] = (row, indicator, button)

        footer = tk.Frame(self.sidebar, bg=DARK)
        footer.pack(side="bottom", fill="x", padx=0, pady=(0, 18))
        settings = tk.Button(
            footer,
            text="⚙    Налаштування",
            command=self.show_settings,
            anchor="w",
            padx=23,
            pady=10,
            bd=0,
            bg=DARK,
            fg="#AEB7C0",
            activebackground=DARK_ACTIVE,
            activeforeground="white",
            font=("Segoe UI", 9),
            cursor="hand2",
        )
        settings.pack(fill="x")
        exit_btn = tk.Button(
            footer,
            text="↪    Вихід",
            command=self.root.destroy,
            anchor="w",
            padx=23,
            pady=10,
            bd=0,
            bg=DARK,
            fg="#D3D9DF",
            activebackground=DARK_ACTIVE,
            activeforeground="white",
            font=("Segoe UI", 9),
            cursor="hand2",
        )
        exit_btn.pack(fill="x")

        status = tk.Frame(self.sidebar, bg=DARK)
        status.pack(side="bottom", fill="x", padx=23, pady=(0, 12))
        tk.Label(status, text="●", bg=DARK, fg="#36B96F", font=("Segoe UI", 8)).pack(side="left", anchor="n")
        status_text = tk.Frame(status, bg=DARK)
        status_text.pack(side="left", padx=(7, 0))
        tk.Label(
            status_text,
            text="База даних: підключено",
            bg=DARK,
            fg="#D3D9DF",
            font=("Segoe UI", 8),
        ).pack(anchor="w")
        tk.Label(
            status_text,
            text=datetime.now().strftime("%d.%m.%Y  %H:%M"),
            bg=DARK,
            fg="#7F8A95",
            font=("Segoe UI", 8),
        ).pack(anchor="w", pady=(2, 0))

        self.main = tk.Frame(self.root, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)

        self.body = tk.Frame(self.main, bg=BG)
        self.body.pack(fill="both", expand=True, padx=28, pady=24)

    def set_section(self, name):
        self.section = name
        for label, parts in self.nav_buttons.items():
            row, indicator, button = parts
            if label == name:
                row.config(bg=DARK_ACTIVE)
                indicator.config(bg=ACCENT)
                button.config(bg=DARK_ACTIVE, fg="white")
            else:
                row.config(bg=DARK)
                indicator.config(bg=DARK)
                button.config(bg=DARK, fg="#D3D9DF")
        for child in self.body.winfo_children():
            child.destroy()

    def page_header(self, title, subtitle, action_text=None, action_command=None):
        top = tk.Frame(self.body, bg=BG)
        top.pack(fill="x", pady=(0, 18))
        text = tk.Frame(top, bg=BG)
        text.pack(side="left")
        tk.Label(
            text,
            text=title,
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 24, "bold"),
        ).pack(anchor="w")
        tk.Label(
            text,
            text=subtitle,
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 9),
        ).pack(anchor="w", pady=(3, 0))
        right = tk.Frame(top, bg=BG)
        right.pack(side="right", anchor="n")
        if action_text and action_command:
            self.primary_button(right, action_text, action_command).pack(side="right")
        date_box = tk.Frame(right, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
        date_box.pack(side="right", padx=(0, 12))
        tk.Label(
            date_box,
            text=f"▣  {datetime.now().strftime('%d.%m.%Y')}",
            bg=PANEL,
            fg="#374151",
            font=("Segoe UI", 9, "bold"),
            padx=13,
            pady=9,
        ).pack()
        return top

    def primary_button(self, parent, text, command):
        return tk.Button(
            parent,
            text=f"＋  {text}" if not text.startswith(("Зберегти", "Створити", "Додати")) else text,
            command=command,
            bd=0,
            relief="flat",
            bg=ACCENT,
            fg="white",
            activebackground=ACCENT_HOVER,
            activeforeground="white",
            padx=17,
            pady=9,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
        )

    def ghost_button(self, parent, text, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bd=0,
            relief="flat",
            bg="#F0F3F5",
            fg="#334155",
            activebackground="#E5E9ED",
            activeforeground=TEXT,
            padx=13,
            pady=8,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
        )

    def danger_button(self, parent, text, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bd=0,
            relief="flat",
            bg="#FDECEC",
            fg=RED,
            activebackground="#F9DADA",
            activeforeground=RED,
            padx=13,
            pady=8,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
        )

    def stat_card(self, parent, title, value, accent, subtitle=""):
        frame = tk.Frame(parent, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
        top = tk.Frame(frame, bg=PANEL)
        top.pack(fill="x", padx=14, pady=(13, 0))
        icon = tk.Label(
            top,
            text="●",
            bg=PANEL,
            fg=accent,
            font=("Segoe UI", 13, "bold"),
        )
        icon.pack(side="left")
        tk.Label(
            top,
            text=title,
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 8, "bold"),
        ).pack(side="left", padx=(8, 0))
        tk.Label(
            frame,
            text=str(value),
            bg=PANEL,
            fg=TEXT,
            font=("Segoe UI", 21, "bold"),
        ).pack(anchor="w", padx=14, pady=(5, 0))
        if subtitle:
            tk.Label(
                frame,
                text=subtitle,
                bg=PANEL,
                fg=MUTED,
                font=("Segoe UI", 8),
            ).pack(anchor="w", padx=14, pady=(2, 12))
        else:
            tk.Frame(frame, bg=PANEL, height=12).pack()
        return frame

    def make_tree(self, parent, columns, widths, height=None):
        holder = tk.Frame(parent, bg=PANEL)
        holder.pack(fill="both", expand=True)
        kwargs = {"columns": columns, "show": "headings"}
        if height:
            kwargs["height"] = height
        tree = ttk.Treeview(holder, **kwargs)
        for col, width in zip(columns, widths):
            tree.heading(col, text=col)
            tree.column(col, width=width, minwidth=50, anchor="w")
        scroll = ttk.Scrollbar(holder, orient="vertical", command=tree.yview, style="Vertical.TScrollbar")
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        return tree

    def search_box(self, parent, variable, width=34):
        frame = tk.Frame(parent, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
        tk.Label(frame, text="⌕", bg=PANEL, fg="#64748B", font=("Segoe UI Symbol", 13)).pack(side="left", padx=(10, 2))
        entry = tk.Entry(
            frame,
            textvariable=variable,
            bd=0,
            relief="flat",
            bg=PANEL,
            fg=TEXT,
            insertbackground=TEXT,
            font=("Segoe UI", 9),
            width=width,
        )
        entry.pack(side="left", fill="x", expand=True, padx=(2, 10), ipady=8)
        return frame, entry

    def show_dashboard(self):
        self.set_section("Огляд")
        self.page_header("Огляд", "Короткий стан служби доставки", "Нове замовлення", self.new_order_dialog)
        stats = self.db.dashboard()

        cards = tk.Frame(self.body, bg=BG)
        cards.pack(fill="x", pady=(0, 18))
        data = [
            ("Замовлень сьогодні", stats["orders_today"], BLUE, "За поточну дату"),
            ("Активні доставки", stats["active"], ORANGE, "Нові, готуються, в дорозі"),
            ("Виручка сьогодні", f'{stats["revenue"]:.0f} ₴', GREEN, "Без скасованих"),
            ("Вільні кур’єри", stats["free_couriers"], ACCENT, f'Середній чек {stats["avg"]:.0f} ₴'),
        ]
        for i, item in enumerate(data):
            cards.columnconfigure(i, weight=1)
            card = self.stat_card(cards, *item)
            card.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 6, 0 if i == 3 else 6))

        panel = tk.Frame(self.body, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
        panel.pack(fill="both", expand=True)
        panel_top = tk.Frame(panel, bg=PANEL)
        panel_top.pack(fill="x", padx=16, pady=(14, 10))
        tk.Label(panel_top, text="Останні замовлення", bg=PANEL, fg=TEXT, font=("Segoe UI", 13, "bold")).pack(side="left")
        self.ghost_button(panel_top, "Перейти до журналу", self.show_orders).pack(side="right")
        table_area = tk.Frame(panel, bg=PANEL)
        table_area.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        tree = self.make_tree(table_area, ["№", "Клієнт", "Статус", "Кур’єр", "Сума", "Створено"], [60, 210, 130, 180, 100, 150])
        for row in self.db.recent_orders():
            tree.insert(
                "",
                "end",
                values=(
                    f"#{row['id']}",
                    row["customer"],
                    row["status"],
                    row["courier"],
                    f"{row['total']:.0f} ₴",
                    row["created_at"][5:16],
                ),
            )

    def show_orders(self):
        self.set_section("Замовлення")
        self.page_header("Замовлення", "Керування замовленнями та статусами доставки", "Нове замовлення", self.new_order_dialog)

        all_orders = self.db.orders("", "Усі")
        counts = {
            "Усі": len(all_orders),
            "Нове": 0,
            "Готується": 0,
            "В дорозі": 0,
            "Доставлено": 0,
            "Скасовано": 0,
        }
        for row in all_orders:
            counts[row["status"]] = counts.get(row["status"], 0) + 1

        stats = tk.Frame(self.body, bg=BG)
        stats.pack(fill="x", pady=(0, 14))
        stat_data = [
            ("Усі замовлення", counts["Усі"], "#56616C"),
            ("Готується", counts["Готується"], BLUE),
            ("В дорозі", counts["В дорозі"], ORANGE),
            ("Доставлено", counts["Доставлено"], GREEN),
            ("Скасовано", counts["Скасовано"], RED),
        ]
        for i, item in enumerate(stat_data):
            stats.columnconfigure(i, weight=1)
            card = self.stat_card(stats, item[0], item[1], item[2])
            card.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 5, 0 if i == 4 else 5))

        filter_panel = tk.Frame(self.body, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
        filter_panel.pack(fill="x", pady=(0, 14))
        filters = tk.Frame(filter_panel, bg=PANEL)
        filters.pack(fill="x", padx=12, pady=12)

        search_var = tk.StringVar()
        status_var = tk.StringVar(value="Усі")
        courier_var = tk.StringVar(value="Усі")

        search_frame, search_entry = self.search_box(filters, search_var, 29)
        search_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))

        status_box = tk.Frame(filters, bg=PANEL)
        status_box.pack(side="left", padx=(0, 10))
        tk.Label(status_box, text="Статус", bg=PANEL, fg="#374151", font=("Segoe UI", 8, "bold")).pack(anchor="w")
        status_combo = ttk.Combobox(
            status_box,
            textvariable=status_var,
            values=["Усі", "Нове", "Готується", "В дорозі", "Доставлено", "Скасовано"],
            state="readonly",
            width=16,
        )
        status_combo.pack(pady=(3, 0))

        courier_names = ["Усі"] + [row["name"] for row in self.db.couriers()]
        courier_box = tk.Frame(filters, bg=PANEL)
        courier_box.pack(side="left")
        tk.Label(courier_box, text="Кур’єр", bg=PANEL, fg="#374151", font=("Segoe UI", 8, "bold")).pack(anchor="w")
        courier_combo = ttk.Combobox(courier_box, textvariable=courier_var, values=courier_names, state="readonly", width=20)
        courier_combo.pack(pady=(3, 0))

        panel = tk.Frame(self.body, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
        panel.pack(fill="both", expand=True)
        top = tk.Frame(panel, bg=PANEL)
        top.pack(fill="x", padx=14, pady=(12, 10))
        tk.Label(top, text="Журнал замовлень", bg=PANEL, fg=TEXT, font=("Segoe UI", 12, "bold")).pack(side="left")
        actions = tk.Frame(top, bg=PANEL)
        actions.pack(side="right")

        table_area = tk.Frame(panel, bg=PANEL)
        table_area.pack(fill="both", expand=True, padx=12)
        tree = self.make_tree(
            table_area,
            ["№", "Клієнт", "Телефон", "Адреса", "Статус", "Кур’єр", "Сума", "Створено"],
            [58, 150, 130, 200, 110, 150, 80, 115],
        )

        footer = tk.Frame(panel, bg=PANEL)
        footer.pack(fill="x", padx=14, pady=10)
        count_label = tk.Label(footer, text="", bg=PANEL, fg=MUTED, font=("Segoe UI", 8))
        count_label.pack(side="left")
        page_box = tk.Frame(footer, bg=PANEL)
        page_box.pack(side="right")
        self.ghost_button(page_box, "‹", lambda: None).pack(side="left", padx=2)
        current = tk.Label(page_box, text="1", bg=ACCENT, fg="white", font=("Segoe UI", 9, "bold"), padx=12, pady=7)
        current.pack(side="left", padx=2)
        self.ghost_button(page_box, "›", lambda: None).pack(side="left", padx=2)

        def refresh(*_):
            for item in tree.get_children():
                tree.delete(item)
            rows = list(self.db.orders(search_var.get().strip(), status_var.get()))
            if courier_var.get() != "Усі":
                rows = [row for row in rows if row["courier"] == courier_var.get()]
            for row in rows:
                tree.insert(
                    "",
                    "end",
                    iid=str(row["id"]),
                    values=(
                        f"#{row['id']}",
                        row["customer"],
                        row["phone"],
                        row["address"],
                        row["status"],
                        row["courier"],
                        f"{row['total']:.0f} ₴",
                        row["created_at"][5:16],
                    ),
                )
            count_label.config(text=f"Показано {len(rows)} замовлень")

        def selected_id():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Замовлення", "Оберіть замовлення у таблиці")
                return None
            return int(sel[0])

        def status_dialog():
            order_id = selected_id()
            if not order_id:
                return
            win = self.modal("Змінити статус", 410, 245)
            self.modal_title(win, f"Замовлення #{order_id}", "Оберіть новий статус")
            value = tk.StringVar(value="Готується")
            combo = ttk.Combobox(
                win,
                textvariable=value,
                values=["Нове", "Готується", "В дорозі", "Доставлено", "Скасовано"],
                state="readonly",
                width=28,
            )
            combo.pack(pady=(5, 15))

            def save():
                self.db.update_order_status(order_id, value.get())
                win.destroy()
                self.show_orders()

            self.primary_button(win, "Зберегти", save).pack()

        def courier_dialog():
            order_id = selected_id()
            if not order_id:
                return
            couriers = self.db.couriers()
            win = self.modal("Призначити кур’єра", 470, 255)
            self.modal_title(win, f"Замовлення #{order_id}", "Призначення виконавця доставки")
            mapping = {f"{r['name']} · {r['transport']} · {r['status']}": r["id"] for r in couriers}
            value = tk.StringVar(value=next(iter(mapping), ""))
            combo = ttk.Combobox(win, textvariable=value, values=list(mapping), state="readonly", width=42)
            combo.pack(pady=(5, 15))

            def save():
                if value.get():
                    self.db.assign_courier(order_id, mapping[value.get()])
                    win.destroy()
                    self.show_orders()

            self.primary_button(win, "Призначити", save).pack()

        def details():
            order_id = selected_id()
            if not order_id:
                return
            rows = self.db.order_items(order_id)
            win = self.modal(f"Склад замовлення #{order_id}", 560, 390)
            self.modal_title(win, "Склад замовлення", f"Замовлення #{order_id}")
            area = tk.Frame(win, bg=PANEL)
            area.pack(fill="both", expand=True, padx=22, pady=(0, 22))
            tree2 = self.make_tree(area, ["Страва", "К-сть", "Ціна", "Сума"], [240, 70, 90, 90], height=7)
            for row in rows:
                tree2.insert("", "end", values=(row["name"], row["quantity"], f"{row['price']:.0f} ₴", f"{row['subtotal']:.0f} ₴"))

        self.ghost_button(actions, "Склад", details).pack(side="left", padx=3)
        self.ghost_button(actions, "Кур’єр", courier_dialog).pack(side="left", padx=3)
        self.ghost_button(actions, "Статус", status_dialog).pack(side="left", padx=3)
        search_entry.bind("<KeyRelease>", refresh)
        status_combo.bind("<<ComboboxSelected>>", refresh)
        courier_combo.bind("<<ComboboxSelected>>", refresh)
        tree.bind("<Double-1>", lambda _: details())
        refresh()

    def show_customers(self):
        self.set_section("Клієнти")
        self.page_header("Клієнти", "Контактна база та історія замовлень")

        customers = list(self.db.customers())
        total_spent = sum(float(row["spent"]) for row in customers)
        cards = tk.Frame(self.body, bg=BG)
        cards.pack(fill="x", pady=(0, 14))
        data = [
            ("Клієнтів у базі", len(customers), BLUE, "Збережені контакти"),
            ("Усього замовлень", sum(int(row["orders_count"]) for row in customers), ORANGE, "Без скасованих"),
            ("Загальна сума", f"{total_spent:.0f} ₴", GREEN, "За всі замовлення"),
        ]
        for i, item in enumerate(data):
            cards.columnconfigure(i, weight=1)
            self.stat_card(cards, *item).grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 6, 0 if i == 2 else 6))

        panel = tk.Frame(self.body, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
        panel.pack(fill="both", expand=True)
        top = tk.Frame(panel, bg=PANEL)
        top.pack(fill="x", padx=14, pady=12)
        tk.Label(top, text="База клієнтів", bg=PANEL, fg=TEXT, font=("Segoe UI", 12, "bold")).pack(side="left")
        search_var = tk.StringVar()
        search_frame, entry = self.search_box(top, search_var, 27)
        search_frame.pack(side="right")
        area = tk.Frame(panel, bg=PANEL)
        area.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        tree = self.make_tree(area, ["ID", "Ім’я", "Телефон", "Адреса", "Замовлень", "Витрачено"], [60, 180, 150, 300, 100, 110])

        def refresh(*_):
            for item in tree.get_children():
                tree.delete(item)
            for row in self.db.customers(search_var.get().strip()):
                tree.insert("", "end", values=(row["id"], row["name"], row["phone"], row["address"], row["orders_count"], f"{row['spent']:.0f} ₴"))

        entry.bind("<KeyRelease>", refresh)
        refresh()

    def show_couriers(self):
        self.set_section("Кур’єри")
        self.page_header("Кур’єри", "Команда доставки та поточна зайнятість", "Додати кур’єра", self.new_courier_dialog)

        rows = list(self.db.couriers())
        free = sum(1 for row in rows if row["status"] == "Вільний")
        busy = len(rows) - free
        cards = tk.Frame(self.body, bg=BG)
        cards.pack(fill="x", pady=(0, 14))
        for i, item in enumerate([
            ("Усього кур’єрів", len(rows), BLUE, "У команді"),
            ("Вільні", free, GREEN, "Готові до доставки"),
            ("На доставці", busy, ORANGE, "Зайняті зараз"),
        ]):
            cards.columnconfigure(i, weight=1)
            self.stat_card(cards, *item).grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 6, 0 if i == 2 else 6))

        panel = tk.Frame(self.body, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
        panel.pack(fill="both", expand=True)
        top = tk.Frame(panel, bg=PANEL)
        top.pack(fill="x", padx=14, pady=12)
        tk.Label(top, text="Команда доставки", bg=PANEL, fg=TEXT, font=("Segoe UI", 12, "bold")).pack(side="left")
        area = tk.Frame(panel, bg=PANEL)
        area.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        tree = self.make_tree(area, ["ID", "Кур’єр", "Телефон", "Транспорт", "Статус"], [70, 240, 190, 160, 140])

        def refresh():
            for item in tree.get_children():
                tree.delete(item)
            for row in self.db.couriers():
                tree.insert("", "end", iid=str(row["id"]), values=(row["id"], row["name"], row["phone"], row["transport"], row["status"]))

        def change_status():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Кур’єри", "Оберіть кур’єра")
                return
            cid = int(sel[0])
            current = tree.item(sel[0])["values"][4]
            new = "Вільний" if current != "Вільний" else "На доставці"
            self.db.update_courier_status(cid, new)
            self.show_couriers()

        self.ghost_button(top, "Змінити статус", change_status).pack(side="right")
        refresh()

    def show_menu(self):
        self.set_section("Меню")
        self.page_header("Меню", "Страви, категорії та доступність", "Додати позицію", self.new_menu_item_dialog)

        rows = list(self.db.menu())
        active = sum(1 for row in rows if row["active"])
        categories = len({row["category"] for row in rows})
        cards = tk.Frame(self.body, bg=BG)
        cards.pack(fill="x", pady=(0, 14))
        for i, item in enumerate([
            ("Позицій", len(rows), BLUE, "У меню"),
            ("Активних", active, GREEN, "Доступні для замовлення"),
            ("Категорій", categories, ORANGE, "Групи страв"),
        ]):
            cards.columnconfigure(i, weight=1)
            self.stat_card(cards, *item).grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 6, 0 if i == 2 else 6))

        panel = tk.Frame(self.body, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
        panel.pack(fill="both", expand=True)
        top = tk.Frame(panel, bg=PANEL)
        top.pack(fill="x", padx=14, pady=12)
        tk.Label(top, text="Меню закладу", bg=PANEL, fg=TEXT, font=("Segoe UI", 12, "bold")).pack(side="left")
        area = tk.Frame(panel, bg=PANEL)
        area.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        tree = self.make_tree(area, ["ID", "Назва", "Категорія", "Ціна", "Доступність"], [70, 280, 220, 120, 140])

        def refresh():
            for item in tree.get_children():
                tree.delete(item)
            for row in self.db.menu():
                tree.insert("", "end", iid=str(row["id"]), values=(row["id"], row["name"], row["category"], f"{row['price']:.0f} ₴", "Активна" if row["active"] else "Прихована"))

        def toggle():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Меню", "Оберіть позицію")
                return
            self.db.toggle_menu_item(int(sel[0]))
            self.show_menu()

        self.ghost_button(top, "Увімкнути / вимкнути", toggle).pack(side="right")
        refresh()

    def show_settings(self):
        win = self.modal("Налаштування", 460, 290)
        self.modal_title(win, "Налаштування", "Параметри локальної системи")
        box = tk.Frame(win, bg=SOFT, highlightbackground=BORDER, highlightthickness=1)
        box.pack(fill="x", padx=22, pady=(4, 16))
        tk.Label(box, text="База даних", bg=SOFT, fg=MUTED, font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=14, pady=(12, 2))
        tk.Label(box, text="SQLite · food_delivery.db", bg=SOFT, fg=TEXT, font=("Segoe UI", 10)).pack(anchor="w", padx=14)
        tk.Label(box, text="Статус", bg=SOFT, fg=MUTED, font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=14, pady=(10, 2))
        tk.Label(box, text="Підключено", bg=SOFT, fg=GREEN, font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=14, pady=(0, 12))
        self.ghost_button(win, "Закрити", win.destroy).pack()

    def modal(self, title, width, height):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry(f"{width}x{height}")
        win.configure(bg=PANEL)
        win.transient(self.root)
        win.grab_set()
        win.resizable(False, False)
        win.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - width) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - height) // 2
        win.geometry(f"{width}x{height}+{x}+{y}")
        return win

    def modal_title(self, win, title, subtitle=""):
        tk.Frame(win, bg=ACCENT, height=4).pack(fill="x")
        tk.Label(win, text=title, bg=PANEL, fg=TEXT, font=("Segoe UI", 16, "bold")).pack(anchor="w", padx=22, pady=(18, 2))
        if subtitle:
            tk.Label(win, text=subtitle, bg=PANEL, fg=MUTED, font=("Segoe UI", 8)).pack(anchor="w", padx=22, pady=(0, 14))

    def labeled_entry(self, parent, label, row, variable, width=34):
        tk.Label(parent, text=label, bg=PANEL, fg="#374151", font=("Segoe UI", 8, "bold")).grid(row=row, column=0, sticky="w", pady=7, padx=(0, 12))
        entry = tk.Entry(
            parent,
            textvariable=variable,
            bd=0,
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=ACCENT,
            font=("Segoe UI", 9),
            bg=PANEL,
            fg=TEXT,
            width=width,
        )
        entry.grid(row=row, column=1, sticky="ew", pady=7, ipady=8)
        return entry

    def new_order_dialog(self):
        win = self.modal("Нове замовлення", 720, 680)
        self.modal_title(win, "Створення замовлення", "Дані клієнта, склад замовлення та доставка")

        form = tk.Frame(win, bg=PANEL)
        form.pack(fill="x", padx=24)
        name = tk.StringVar()
        phone = tk.StringVar()
        address = tk.StringVar()
        self.labeled_entry(form, "Клієнт", 0, name)
        self.labeled_entry(form, "Телефон", 1, phone)
        self.labeled_entry(form, "Адреса", 2, address)
        form.columnconfigure(1, weight=1)

        tk.Frame(win, bg=BORDER, height=1).pack(fill="x", padx=24, pady=14)

        tk.Label(win, text="Позиції замовлення", bg=PANEL, fg=TEXT, font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=24, pady=(0, 8))
        menu = self.db.menu(active_only=True)
        menu_map = {f"{row['name']} · {row['price']:.0f} ₴": row for row in menu}
        choose = tk.Frame(win, bg=PANEL)
        choose.pack(fill="x", padx=24)
        item_var = tk.StringVar(value=next(iter(menu_map), ""))
        qty_var = tk.StringVar(value="1")
        ttk.Combobox(choose, textvariable=item_var, values=list(menu_map), state="readonly", width=39).pack(side="left", padx=(0, 8))
        tk.Entry(
            choose,
            textvariable=qty_var,
            width=5,
            bd=0,
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=ACCENT,
            font=("Segoe UI", 9),
        ).pack(side="left", ipady=8, padx=(0, 8))
        cart = []

        cart_frame = tk.Frame(win, bg=PANEL)
        cart_frame.pack(fill="both", expand=True, padx=24, pady=12)
        cart_tree = self.make_tree(cart_frame, ["Страва", "К-сть", "Ціна", "Сума"], [300, 70, 100, 110], height=6)

        total_label = tk.Label(win, text="Разом з доставкою: 60 ₴", bg=PANEL, fg=TEXT, font=("Segoe UI", 12, "bold"))
        total_label.pack(anchor="e", padx=24)

        def refresh_cart():
            for child in cart_tree.get_children():
                cart_tree.delete(child)
            subtotal = 0
            for idx, item in enumerate(cart):
                amount = item["price"] * item["quantity"]
                subtotal += amount
                cart_tree.insert("", "end", iid=str(idx), values=(item["name"], item["quantity"], f"{item['price']:.0f} ₴", f"{amount:.0f} ₴"))
            total_label.config(text=f"Разом з доставкою: {subtotal + 60:.0f} ₴")

        def add_item():
            try:
                qty = int(qty_var.get())
                if qty <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Замовлення", "Кількість має бути додатним цілим числом")
                return
            if item_var.get() not in menu_map:
                return
            row = menu_map[item_var.get()]
            for item in cart:
                if item["id"] == row["id"]:
                    item["quantity"] += qty
                    refresh_cart()
                    return
            cart.append({"id": row["id"], "name": row["name"], "price": row["price"], "quantity": qty})
            refresh_cart()

        self.ghost_button(choose, "Додати", add_item).pack(side="left")

        courier_rows = self.db.couriers()
        courier_map = {"Не призначати": None}
        for row in courier_rows:
            courier_map[f"{row['name']} · {row['status']}"] = row["id"]
        courier_var = tk.StringVar(value="Не призначати")
        courier_frame = tk.Frame(win, bg=PANEL)
        courier_frame.pack(fill="x", padx=24, pady=(10, 12))
        tk.Label(courier_frame, text="Кур’єр", bg=PANEL, fg="#374151", font=("Segoe UI", 8, "bold")).pack(side="left")
        ttk.Combobox(courier_frame, textvariable=courier_var, values=list(courier_map), state="readonly", width=37).pack(side="right")

        actions = tk.Frame(win, bg=PANEL)
        actions.pack(fill="x", padx=24, pady=(0, 20))

        def save():
            if not name.get().strip() or not phone.get().strip() or not address.get().strip():
                messagebox.showerror("Замовлення", "Заповніть дані клієнта")
                return
            if not cart:
                messagebox.showerror("Замовлення", "Додайте хоча б одну позицію")
                return
            try:
                customer_id = self.db.find_or_create_customer(name.get().strip(), phone.get().strip(), address.get().strip())
                order_id, total = self.db.create_order(customer_id, courier_map[courier_var.get()], cart)
            except Exception as exc:
                messagebox.showerror("Замовлення", str(exc))
                return
            messagebox.showinfo("Готово", f"Замовлення #{order_id} створено\nСума: {total:.0f} ₴")
            win.destroy()
            if self.section == "Замовлення":
                self.show_orders()
            else:
                self.show_dashboard()

        self.ghost_button(actions, "Скасувати", win.destroy).pack(side="right", padx=(8, 0))
        self.primary_button(actions, "Створити замовлення", save).pack(side="right")

    def new_courier_dialog(self):
        win = self.modal("Новий кур’єр", 500, 365)
        self.modal_title(win, "Додати кур’єра", "Контактні дані та транспорт")
        form = tk.Frame(win, bg=PANEL)
        form.pack(fill="x", padx=24)
        name = tk.StringVar()
        phone = tk.StringVar()
        transport = tk.StringVar(value="Авто")
        self.labeled_entry(form, "Ім’я", 0, name)
        self.labeled_entry(form, "Телефон", 1, phone)
        tk.Label(form, text="Транспорт", bg=PANEL, fg="#374151", font=("Segoe UI", 8, "bold")).grid(row=2, column=0, sticky="w", pady=7, padx=(0, 12))
        ttk.Combobox(form, textvariable=transport, values=["Авто", "Скутер", "Велосипед", "Пішки"], state="readonly", width=31).grid(row=2, column=1, sticky="ew", pady=7)
        form.columnconfigure(1, weight=1)

        def save():
            if not name.get().strip() or not phone.get().strip():
                messagebox.showerror("Кур’єр", "Заповніть ім’я та телефон")
                return
            try:
                self.db.add_courier(name.get().strip(), phone.get().strip(), transport.get())
            except Exception as exc:
                messagebox.showerror("Кур’єр", str(exc))
                return
            win.destroy()
            self.show_couriers()

        self.primary_button(win, "Додати", save).pack(pady=22)

    def new_menu_item_dialog(self):
        win = self.modal("Нова позиція меню", 500, 390)
        self.modal_title(win, "Додати позицію меню", "Назва, категорія та ціна")
        form = tk.Frame(win, bg=PANEL)
        form.pack(fill="x", padx=24)
        name = tk.StringVar()
        category = tk.StringVar(value="Основні страви")
        price = tk.StringVar()
        self.labeled_entry(form, "Назва", 0, name)
        tk.Label(form, text="Категорія", bg=PANEL, fg="#374151", font=("Segoe UI", 8, "bold")).grid(row=1, column=0, sticky="w", pady=7, padx=(0, 12))
        ttk.Combobox(
            form,
            textvariable=category,
            values=["Піца", "Бургери", "Салати", "Основні страви", "Азійська кухня", "Закуски", "Напої", "Десерти"],
            state="readonly",
            width=31,
        ).grid(row=1, column=1, sticky="ew", pady=7)
        self.labeled_entry(form, "Ціна, ₴", 2, price)
        form.columnconfigure(1, weight=1)

        def save():
            try:
                value = float(price.get().replace(",", "."))
                if value < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Меню", "Введіть коректну ціну")
                return
            if not name.get().strip():
                messagebox.showerror("Меню", "Введіть назву")
                return
            self.db.add_menu_item(name.get().strip(), category.get(), value)
            win.destroy()
            self.show_menu()

        self.primary_button(win, "Додати", save).pack(pady=22)


if __name__ == "__main__":
    root = tk.Tk()
    FoodDeliveryAIS(root)
    root.mainloop()
