# expense_tracker/gui_app.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from storage import load_expenses, save_expenses
from logic import KATEGORIJAS, sum_total, filter_by_month, sum_by_category, get_available_months
from export import export_to_csv
import os
import re

class ModernGUI:
    # Moderna krāsu palete
    COLORS = {
        'bg': '#0a0e1a',
        'fg': '#ffffff',
        'accent': '#4361ee',
        'accent_light': '#4895ef',
        'accent_dark': '#3f37c9',
        'success': '#4cc9f0',
        'danger': '#f72585',
        'warning': '#f8961e',
        'info': '#7209b7',
        'card_bg': '#1a1f2e',
        'card_border': '#2b3245',
        'hover': '#2d3748',
        'valid': '#38b000',
        'invalid': '#d00000',
        'gradient_start': '#4361ee',
        'gradient_end': '#7209b7'
    }
    
    def __init__(self, root):
        self.root = root
        self.root.title("Izdevumu Izsekotājs Pro")
        self.root.geometry("1400x800")
        self.root.configure(bg=self.COLORS['bg'])
        
        self.setup_icon()
        
        self.expenses = load_expenses()
        self.current_filter = None
        self.current_view = "Visi izdevumi"
        self.editing_index = None
        
        self.setup_styles()
        self.create_custom_titlebar()
        self.create_menu()
        self.create_header()
        self.create_main_content()
        self.create_status_bar()
        self.setup_shortcuts()
        
        self.auto_save()
        self.refresh_table()
        self.update_stats()
    
    def setup_icon(self):
        try:
            icon_paths = [
                'icon.ico',
                os.path.join(os.path.dirname(__file__), '..', 'icon.ico'),
                os.path.join(os.path.dirname(__file__), 'icon.ico')
            ]
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    self.root.iconbitmap(icon_path)
                    break
        except:
            pass
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Treeview',
                       background=self.COLORS['card_bg'],
                       foreground=self.COLORS['fg'],
                       fieldbackground=self.COLORS['card_bg'],
                       rowheight=40,
                       font=('Segoe UI', 10))
        
        style.configure('Treeview.Heading',
                       background=self.COLORS['gradient_start'],
                       foreground=self.COLORS['fg'],
                       relief='flat',
                       font=('Segoe UI', 11, 'bold'))
        
        style.map('Treeview',
                 background=[('selected', self.COLORS['info'])])
        
        style.configure('TProgressbar',
                       background=self.COLORS['success'],
                       troughcolor=self.COLORS['card_bg'])
    
    def interpolate_color(self, color1, color2, ratio):
        c1 = [int(color1[i:i+2], 16) for i in range(1, 7, 2)]
        c2 = [int(color2[i:i+2], 16) for i in range(1, 7, 2)]
        
        r = int(c1[0] + (c2[0] - c1[0]) * ratio)
        g = int(c1[1] + (c2[1] - c1[1]) * ratio)
        b = int(c1[2] + (c2[2] - c1[2]) * ratio)
        
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def create_stat_card(self, parent, title, color):
        card = tk.Frame(parent, bg=self.COLORS['card_bg'], bd=1, relief=tk.FLAT)
        
        line = tk.Frame(card, bg=color, height=4)
        line.pack(fill=tk.X)
        
        tk.Label(card,
                text=title,
                font=('Segoe UI', 10),
                bg=self.COLORS['card_bg'],
                fg=self.COLORS['fg']).pack(padx=15, pady=(10, 0))
        
        return card
    
    def create_custom_titlebar(self):
        titlebar = tk.Frame(self.root, bg=self.COLORS['gradient_end'], height=35)
        titlebar.pack(fill=tk.X)
        titlebar.pack_propagate(False)
        
        canvas = tk.Canvas(titlebar, height=35, highlightthickness=0)
        canvas.pack(fill=tk.X)
        canvas.create_rectangle(0, 0, 1400, 35, 
                               fill=self.COLORS['gradient_start'],
                               outline="")
        
        title = tk.Label(canvas,
                        text="  💰 Izdevumu Izsekotājs Pro",
                        bg=self.COLORS['gradient_start'],
                        fg=self.COLORS['fg'],
                        font=('Segoe UI', 11, 'bold'))
        canvas.create_window(100, 17, window=title)
        
        def minimize():
            self.root.iconify()
        
        def maximize():
            if self.root.state() == 'normal':
                self.root.state('zoomed')
            else:
                self.root.state('normal')
        
        def close():
            self.root.quit()
        
        close_btn = tk.Button(canvas, text="✕", command=close,
                            bg=self.COLORS['gradient_start'], fg=self.COLORS['fg'],
                            font=('Segoe UI', 10), bd=0, padx=15,
                            activebackground=self.COLORS['danger'])
        canvas.create_window(1350, 17, window=close_btn)
        
        max_btn = tk.Button(canvas, text="□", command=maximize,
                          bg=self.COLORS['gradient_start'], fg=self.COLORS['fg'],
                          font=('Segoe UI', 10), bd=0, padx=15,
                          activebackground=self.COLORS['hover'])
        canvas.create_window(1300, 17, window=max_btn)
        
        min_btn = tk.Button(canvas, text="─", command=minimize,
                          bg=self.COLORS['gradient_start'], fg=self.COLORS['fg'],
                          font=('Segoe UI', 10), bd=0, padx=15,
                          activebackground=self.COLORS['hover'])
        canvas.create_window(1250, 17, window=min_btn)
    
    def create_menu(self):
        menubar = tk.Menu(self.root, bg=self.COLORS['card_bg'], fg=self.COLORS['fg'],
                         activebackground=self.COLORS['accent'],
                         activeforeground=self.COLORS['fg'],
                         tearoff=0)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0, bg=self.COLORS['card_bg'], fg=self.COLORS['fg'])
        menubar.add_cascade(label="📁 Fails", menu=file_menu)
        file_menu.add_command(label="💾 Eksportēt CSV (Ctrl+S)", command=self.export_csv)
        file_menu.add_separator()
        file_menu.add_command(label="💿 Dublēt datus", command=self.backup_data)
        file_menu.add_command(label="📀 Atjaunot datus", command=self.restore_data)
        file_menu.add_separator()
        file_menu.add_command(label="🚪 Iziet (Alt+F4)", command=self.root.quit)
        
        edit_menu = tk.Menu(menubar, tearoff=0, bg=self.COLORS['card_bg'], fg=self.COLORS['fg'])
        menubar.add_cascade(label="✏️ Rediģēt", menu=edit_menu)
        edit_menu.add_command(label="➕ Pievienot (Ctrl+N)", command=self.add_expense_dialog)
        edit_menu.add_command(label="✏️ Rediģēt (Ctrl+E)", command=self.edit_expense)
        edit_menu.add_command(label="🗑️ Dzēst (Del)", command=self.delete_expense)
        edit_menu.add_separator()
        edit_menu.add_command(label="🔍 Meklēt (Ctrl+F)", command=lambda: self.search_entry.focus())
        
        view_menu = tk.Menu(menubar, tearoff=0, bg=self.COLORS['card_bg'], fg=self.COLORS['fg'])
        menubar.add_cascade(label="👁️ Skats", menu=view_menu)
        view_menu.add_command(label="📋 Visi izdevumi", command=self.show_all)
        view_menu.add_command(label="📊 Statistika", command=self.show_statistics_window)
        view_menu.add_command(label="📈 Grafiki", command=self.show_charts)
        
        help_menu = tk.Menu(menubar, tearoff=0, bg=self.COLORS['card_bg'], fg=self.COLORS['fg'])
        menubar.add_cascade(label="❓ Palīdzība", menu=help_menu)
        help_menu.add_command(label="📖 Lietošanas instrukcija (F1)", command=self.show_help)
        help_menu.add_command(label="ℹ️ Par programmu", command=self.show_about)
    
    def create_header(self):
        header = tk.Frame(self.root, height=180)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        canvas = tk.Canvas(header, height=180, highlightthickness=0)
        canvas.pack(fill=tk.X)
        
        for i in range(180):
            color = self.interpolate_color(self.COLORS['gradient_start'],
                                          self.COLORS['gradient_end'],
                                          i/180)
            canvas.create_line(0, i, 1400, i, fill=color, width=1)
        
        content = tk.Frame(canvas, bg=self.COLORS['gradient_start'])
        canvas.create_window(700, 90, window=content)
        
        left = tk.Frame(content, bg=self.COLORS['gradient_start'])
        left.pack(side=tk.LEFT, padx=30)
        
        logo_label = tk.Label(left,
                             text="💰",
                             font=('Segoe UI', 48),
                             bg=self.COLORS['gradient_start'],
                             fg=self.COLORS['fg'])
        logo_label.pack(side=tk.LEFT, padx=(0, 20))
        
        title_frame = tk.Frame(left, bg=self.COLORS['gradient_start'])
        title_frame.pack(side=tk.LEFT)
        
        title_label = tk.Label(title_frame,
                              text="IZDEVUMU IZSEKOTĀJS PRO",
                              font=('Segoe UI', 24, 'bold'),
                              bg=self.COLORS['gradient_start'],
                              fg=self.COLORS['fg'])
        title_label.pack(anchor=tk.W)
        
        subtitle_label = tk.Label(title_frame,
                                 text="Personīgo finanšu uzskaites rīks | Versija 3.0",
                                 font=('Segoe UI', 11),
                                 bg=self.COLORS['gradient_start'],
                                 fg=self.COLORS['fg'])
        subtitle_label.pack(anchor=tk.W)
        
        right = tk.Frame(content, bg=self.COLORS['gradient_start'])
        right.pack(side=tk.RIGHT, padx=30)
        
        total_card = self.create_stat_card(right, "Kopējie izdevumi", self.COLORS['success'])
        total_card.pack(side=tk.LEFT, padx=5)
        
        self.total_label = tk.Label(total_card,
                                   text="0.00 €",
                                   font=('Segoe UI', 20, 'bold'),
                                   bg=self.COLORS['card_bg'],
                                   fg=self.COLORS['fg'])
        self.total_label.pack(padx=15, pady=(0, 10))
        
        count_card = self.create_stat_card(right, "Ierakstu skaits", self.COLORS['info'])
        count_card.pack(side=tk.LEFT, padx=5)
        
        self.count_label = tk.Label(count_card,
                                   text="0",
                                   font=('Segoe UI', 20, 'bold'),
                                   bg=self.COLORS['card_bg'],
                                   fg=self.COLORS['fg'])
        self.count_label.pack(padx=15, pady=(0, 10))
        
        date_card = self.create_stat_card(right, "Šodienas datums", self.COLORS['accent_light'])
        date_card.pack(side=tk.LEFT, padx=5)
        
        today = datetime.now().strftime("%d.%m.%Y")
        today_label = tk.Label(date_card,
                              text=today,
                              font=('Segoe UI', 18, 'bold'),
                              bg=self.COLORS['card_bg'],
                              fg=self.COLORS['fg'])
        today_label.pack(padx=15, pady=(0, 10))
    
    def create_main_content(self):
        main = tk.Frame(self.root, bg=self.COLORS['bg'])
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        left_panel = tk.Frame(main, bg=self.COLORS['card_bg'], width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        left_panel.pack_propagate(False)
        
        right_panel = tk.Frame(main, bg=self.COLORS['card_bg'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.create_left_panel(left_panel)
        self.create_right_panel(right_panel)
    
    def create_card(self, parent, title):
        frame = tk.Frame(parent, bg=self.COLORS['card_bg'], bd=1, relief=tk.FLAT)
        
        title_frame = tk.Frame(frame, bg=self.COLORS['card_bg'])
        title_frame.pack(fill=tk.X, pady=(10, 5))
        
        tk.Label(title_frame,
                text=title,
                font=('Segoe UI', 11, 'bold'),
                bg=self.COLORS['card_bg'],
                fg=self.COLORS['success']).pack()
        
        canvas = tk.Canvas(title_frame, height=2, bg=self.COLORS['success'],
                          highlightthickness=0)
        canvas.pack(fill=tk.X, padx=15, pady=5)
        
        return frame
    
    def create_modern_button(self, parent, text, command, color):
        btn = tk.Button(parent,
                       text=text,
                       command=lambda: [command(), self.animate_button(btn)],
                       bg=color,
                       fg=self.COLORS['fg'],
                       font=('Segoe UI', 11, 'bold'),
                       bd=0,
                       padx=15,
                       pady=12,
                       cursor='hand2',
                       activebackground=self.COLORS['hover'],
                       activeforeground=self.COLORS['fg'])
        
        btn.bind('<Enter>', lambda e, b=btn: b.configure(bg=self.COLORS['hover']))
        btn.bind('<Leave>', lambda e, b=btn, c=color: b.configure(bg=c))
        
        return btn
    
    def create_left_panel(self, parent):
        parent.configure(bd=1, relief=tk.FLAT)
        
        quick_frame = self.create_card(parent, "ĀTRĀS DARBĪBAS")
        quick_frame.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        buttons = [
            ("➕ PIEVIENOT", self.add_expense_dialog, self.COLORS['success']),
            ("✏️ REDIĢĒT", self.edit_expense, self.COLORS['info']),
            ("🗑️ DZĒST", self.delete_expense, self.COLORS['danger']),
        ]
        
        for text, cmd, color in buttons:
            btn = self.create_modern_button(quick_frame, text, cmd, color)
            btn.pack(fill=tk.X, pady=3)
        
        filter_frame = self.create_card(parent, "FILTRĒŠANA")
        filter_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.filter_var = tk.StringVar()
        self.filter_combo = ttk.Combobox(filter_frame,
                                        textvariable=self.filter_var,
                                        state="readonly",
                                        font=('Segoe UI', 10))
        self.filter_combo.pack(fill=tk.X, pady=5)
        self.filter_combo.bind('<<ComboboxSelected>>', self.apply_filter)
        
        clear_btn = self.create_modern_button(filter_frame, "NOTĪRĪT FILTRU",
                                            self.show_all, self.COLORS['accent_dark'])
        clear_btn.pack(fill=tk.X, pady=5)
        
        analysis_frame = self.create_card(parent, "ANALĪZE")
        analysis_frame.pack(fill=tk.X, padx=15, pady=10)
        
        analysis_buttons = [
            ("📊 STATISTIKA", self.show_statistics_window, self.COLORS['info']),
            ("📈 GRAFIKI", self.show_charts, self.COLORS['warning']),
        ]
        
        for text, cmd, color in analysis_buttons:
            btn = self.create_modern_button(analysis_frame, text, cmd, color)
            btn.pack(fill=tk.X, pady=2)
        
        self.create_budget_card(parent)
    
    def create_budget_card(self, parent):
        budget_frame = self.create_card(parent, "BUDŽETS")
        budget_frame.pack(fill=tk.X, padx=15, pady=10)
        
        content = tk.Frame(budget_frame, bg=self.COLORS['card_bg'])
        content.pack(fill=tk.X, padx=15, pady=10)
        
        self.budget_value = tk.StringVar(value="500.00 €")
        tk.Label(content,
                textvariable=self.budget_value,
                font=('Segoe UI', 20, 'bold'),
                bg=self.COLORS['card_bg'],
                fg=self.COLORS['success']).pack()
        
        progress_frame = tk.Frame(content, bg=self.COLORS['card_bg'])
        progress_frame.pack(fill=tk.X, pady=10)
        
        self.budget_progress = ttk.Progressbar(progress_frame,
                                              length=200,
                                              mode='determinate',
                                              style='TProgressbar')
        self.budget_progress.pack()
        
        self.budget_label = tk.Label(content,
                                     text="0%",
                                     font=('Segoe UI', 10, 'bold'),
                                     bg=self.COLORS['card_bg'],
                                     fg=self.COLORS['fg'])
        self.budget_label.pack()
        
        budget_btn = self.create_modern_button(content, "IESTATĪT BUDŽETU",
                                             self.set_budget, self.COLORS['info'])
        budget_btn.pack(pady=10)
    
    def create_right_panel(self, parent):
        search_frame = tk.Frame(parent, bg=self.COLORS['card_bg'])
        search_frame.pack(fill=tk.X, padx=20, pady=15)
        
        search_icon = tk.Label(search_frame,
                              text="🔍",
                              font=('Segoe UI', 12),
                              bg=self.COLORS['card_bg'],
                              fg=self.COLORS['fg'])
        search_icon.pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.search_expenses)
        self.search_entry = tk.Entry(search_frame,
                                    textvariable=self.search_var,
                                    bg=self.COLORS['bg'],
                                    fg=self.COLORS['fg'],
                                    insertbackground=self.COLORS['fg'],
                                    font=('Segoe UI', 11),
                                    relief=tk.FLAT,
                                    width=30)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        table_frame = tk.Frame(parent, bg=self.COLORS['card_bg'])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        vsb = tk.Scrollbar(table_frame, bg=self.COLORS['card_bg'])
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        hsb = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL, bg=self.COLORS['card_bg'])
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.tree = ttk.Treeview(table_frame,
                                columns=("datums", "summa", "kategorija", "apraksts"),
                                show="tree headings",
                                yscrollcommand=vsb.set,
                                xscrollcommand=hsb.set,
                                selectmode='browse')
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        self.tree.heading("#0", text="Nr.", anchor='center')
        self.tree.heading("datums", text="Datums", anchor='center')
        self.tree.heading("summa", text="Summa (€)", anchor='center')
        self.tree.heading("kategorija", text="Kategorija", anchor='center')
        self.tree.heading("apraksts", text="Apraksts", anchor='w')
        
        self.tree.column("#0", width=60, anchor='center')
        self.tree.column("datums", width=100, anchor='center')
        self.tree.column("summa", width=120, anchor='center')
        self.tree.column("kategorija", width=150, anchor='center')
        self.tree.column("apraksts", width=500, anchor='w')
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        self.create_context_menu()
        self.tree.bind('<Double-1>', lambda e: self.edit_expense())
    
    def create_context_menu(self):
        self.context_menu = tk.Menu(self.root, tearoff=0,
                                   bg=self.COLORS['card_bg'],
                                   fg=self.COLORS['fg'],
                                   activebackground=self.COLORS['accent'])
        self.context_menu.add_command(label="✏️ Rediģēt", command=self.edit_expense)
        self.context_menu.add_command(label="🗑️ Dzēst", command=self.delete_expense)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="📋 Kopēt aprakstu", command=self.copy_description)
        
        self.tree.bind('<Button-3>', self.show_context_menu)
    
    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def create_status_bar(self):
        status = tk.Frame(self.root, bg=self.COLORS['gradient_start'], height=30)
        status.pack(side=tk.BOTTOM, fill=tk.X)
        status.pack_propagate(False)
        
        canvas = tk.Canvas(status, height=30, highlightthickness=0)
        canvas.pack(fill=tk.X)
        canvas.create_rectangle(0, 0, 1400, 30, 
                               fill=self.COLORS['gradient_start'],
                               outline="")
        
        self.status_bar = tk.Label(canvas,
                                   text="✓ Gatavs",
                                   anchor=tk.W,
                                   bg=self.COLORS['gradient_start'],
                                   fg=self.COLORS['fg'],
                                   font=('Segoe UI', 9))
        canvas.create_window(100, 15, window=self.status_bar, anchor=tk.W)
        
        self.view_count = tk.Label(canvas,
                                  text="",
                                  bg=self.COLORS['gradient_start'],
                                  fg=self.COLORS['fg'],
                                  font=('Segoe UI', 9))
        canvas.create_window(1250, 15, window=self.view_count)
        
        self.clock_label = tk.Label(canvas,
                                   text="",
                                   bg=self.COLORS['gradient_start'],
                                   fg=self.COLORS['fg'],
                                   font=('Segoe UI', 9))
        canvas.create_window(1350, 15, window=self.clock_label)
        
        self.update_clock()
    
    def update_clock(self):
        now = datetime.now()
        self.clock_label.config(text=now.strftime("%H:%M  |  %d.%m.%Y"))
        self.root.after(1000, self.update_clock)
    
    def setup_shortcuts(self):
        self.root.bind('<Control-n>', lambda e: self.add_expense_dialog())
        self.root.bind('<Control-e>', lambda e: self.edit_expense())
        self.root.bind('<Delete>', lambda e: self.delete_expense())
        self.root.bind('<Control-f>', lambda e: self.search_entry.focus())
        self.root.bind('<Control-s>', lambda e: self.export_csv())
        self.root.bind('<F1>', lambda e: self.show_help())
        self.root.bind('<Escape>', lambda e: self.root.focus())
    
    def animate_button(self, button):
        original_bg = button.cget('bg')
        button.configure(bg=self.COLORS['hover'])
        self.root.after(200, lambda: button.configure(bg=original_bg))
    
    def auto_save(self):
        save_expenses(self.expenses)
        self.status_bar.config(text="✓ Automātiski saglabāts")
        self.root.after(300000, self.auto_save)
    
    def refresh_table(self, filtered_data=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        display_data = filtered_data if filtered_data is not None else self.expenses
        if not filtered_data and self.search_var.get():
            display_data = self.search_in_expenses(self.expenses, self.search_var.get())
        
        for i, exp in enumerate(display_data, 1):
            tags = ()
            if exp['amount'] > 50:
                tags = ('high',)
            elif exp['amount'] < 5:
                tags = ('low',)
            
            self.tree.insert("", tk.END, text=str(i),
                           values=(exp['date'],
                                  f"{exp['amount']:.2f}",
                                  exp['category'],
                                  exp['description']),
                           tags=tags)
        
        self.tree.tag_configure('high', foreground=self.COLORS['danger'])
        self.tree.tag_configure('low', foreground=self.COLORS['success'])
        
        self.update_stats()
        self.update_view_count(len(display_data))
    
    def update_stats(self):
        total = sum_total(self.expenses)
        self.total_label.config(text=f"{total:.2f} €")
        self.count_label.config(text=str(len(self.expenses)))
        
        months = get_available_months(self.expenses)
        self.filter_combo['values'] = months
    
    def update_view_count(self, count):
        self.view_count.config(text=f"Rāda {count} no {len(self.expenses)} ierakstiem")
    
    def search_in_expenses(self, expenses, term):
        if not term:
            return expenses
        term = term.lower()
        return [e for e in expenses if term in e['description'].lower()]
    
    def search_expenses(self, *args):
        self.refresh_table()
    
    def apply_filter(self, event=None):
        selected = self.filter_var.get()
        if selected:
            year, month = map(int, selected.split('-'))
            self.current_filter = filter_by_month(self.expenses, year, month)
            self.refresh_table(self.current_filter)
            self.status_bar.config(text=f"✓ Filtrēts pēc {selected}")
    
    def show_all(self):
        self.current_filter = None
        self.filter_var.set("")
        self.refresh_table()
        self.status_bar.config(text="✓ Rāda visus izdevumus")
    
    def create_input_field(self, parent, label, row):
        tk.Label(parent,
                text=label,
                font=('Segoe UI', 10, 'bold'),
                bg=self.COLORS['card_bg'],
                fg=self.COLORS['fg']).grid(row=row, column=0, sticky='w', pady=(0, 5))
    
    def create_validated_entry(self, parent, row):
        entry = tk.Entry(parent, bg=self.COLORS['bg'], fg=self.COLORS['fg'],
                        insertbackground=self.COLORS['fg'],
                        font=('Segoe UI', 11), relief=tk.FLAT)
        entry.grid(row=row, column=0, columnspan=2, sticky='ew', pady=(0, 15))
        return entry
    
    def add_expense_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Pievienot izdevumu")
        dialog.geometry("500x600")
        dialog.configure(bg=self.COLORS['bg'])
        
        try:
            icon_paths = ['icon.ico', '../icon.ico']
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    dialog.iconbitmap(icon_path)
                    break
        except:
            pass
        
        dialog.transient(self.root)
        dialog.grab_set()
        
        main = tk.Frame(dialog, bg=self.COLORS['card_bg'], bd=1, relief=tk.FLAT)
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title_frame = tk.Frame(main, bg=self.COLORS['card_bg'])
        title_frame.pack(fill=tk.X, pady=(15, 20))
        
        tk.Label(title_frame,
                text="PIEVIENOT IZDEVUMU",
                font=('Segoe UI', 16, 'bold'),
                bg=self.COLORS['card_bg'],
                fg=self.COLORS['success']).pack()
        
        canvas = tk.Canvas(title_frame, height=2, bg=self.COLORS['success'],
                          highlightthickness=0)
        canvas.pack(fill=tk.X, padx=50, pady=5)
        
        content = tk.Frame(main, bg=self.COLORS['card_bg'])
        content.pack(fill=tk.BOTH, expand=True, padx=30)
        
        self.create_input_field(content, "Datums (YYYY-MM-DD):", 0)
        date_entry = self.create_validated_entry(content, 1)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        self.create_input_field(content, "Kategorija:", 2)
        category_var = tk.StringVar()
        category_combo = ttk.Combobox(content, textvariable=category_var,
                                     values=KATEGORIJAS, state="readonly",
                                     font=('Segoe UI', 11))
        category_combo.grid(row=3, column=0, columnspan=2, sticky='ew', pady=(0, 15))
        
        self.create_input_field(content, "Summa (EUR):", 4)
        amount_entry = self.create_validated_entry(content, 5)
        
        self.create_input_field(content, "Apraksts:", 6)
        desc_entry = self.create_validated_entry(content, 7)
        
        error_label = tk.Label(content, text="", bg=self.COLORS['card_bg'],
                              fg=self.COLORS['danger'], font=('Segoe UI', 9))
        error_label.grid(row=8, column=0, columnspan=2, pady=5)
        
        button_frame = tk.Frame(content, bg=self.COLORS['card_bg'])
        button_frame.grid(row=9, column=0, columnspan=2, pady=20)
        
        def validate_date():
            date_text = date_entry.get()
            pattern = r'^\d{4}-\d{2}-\d{2}$'
            if re.match(pattern, date_text):
                try:
                    datetime.strptime(date_text, "%Y-%m-%d")
                    date_entry.configure(bg=self.COLORS['valid'])
                    return True
                except:
                    date_entry.configure(bg=self.COLORS['invalid'])
                    return False
            else:
                date_entry.configure(bg=self.COLORS['invalid'])
                return False
        
        def validate_amount():
            try:
                amount = float(amount_entry.get())
                if amount > 0:
                    amount_entry.configure(bg=self.COLORS['valid'])
                    return True
                else:
                    amount_entry.configure(bg=self.COLORS['invalid'])
                    return False
            except:
                amount_entry.configure(bg=self.COLORS['invalid'])
                return False
        
        def validate_desc():
            if len(desc_entry.get().strip()) > 0:
                desc_entry.configure(bg=self.COLORS['valid'])
                return True
            else:
                desc_entry.configure(bg=self.COLORS['invalid'])
                return False
        
        date_entry.bind('<KeyRelease>', lambda e: validate_date())
        amount_entry.bind('<KeyRelease>', lambda e: validate_amount())
        desc_entry.bind('<KeyRelease>', lambda e: validate_desc())
        
        def save():
            if (validate_date() and validate_amount() and 
                validate_desc() and category_var.get()):
                
                new_expense = {
                    "date": date_entry.get(),
                    "amount": float(amount_entry.get()),
                    "category": category_var.get(),
                    "description": desc_entry.get().strip()
                }
                
                self.expenses.append(new_expense)
                save_expenses(self.expenses)
                self.refresh_table()
                dialog.destroy()
                self.status_bar.config(text=f"✓ Pievienots: {new_expense['description']}")
            else:
                error_label.config(text="Lūdzu, aizpildi visus laukus pareizi!")
        
        tk.Button(button_frame, text="SAGLABĀT", command=save,
                 bg=self.COLORS['success'], fg=self.COLORS['fg'],
                 font=('Segoe UI', 11, 'bold'),
                 bd=0, padx=25, pady=8,
                 cursor='hand2').pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="ATCELT", command=dialog.destroy,
                 bg=self.COLORS['danger'], fg=self.COLORS['fg'],
                 font=('Segoe UI', 11),
                 bd=0, padx=25, pady=8,
                 cursor='hand2').pack(side=tk.LEFT, padx=5)
        
        dialog.bind('<Return>', lambda e: save())
        dialog.bind('<Escape>', lambda e: dialog.destroy())
    
    def edit_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Brīdinājums", "Izvēlies ierakstu, ko rediģēt!")
            return
        
        index = int(self.tree.item(selected[0])['text']) - 1
        expense = self.expenses[index]
        self.editing_index = index
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Rediģēt izdevumu")
        dialog.geometry("500x600")
        dialog.configure(bg=self.COLORS['bg'])
        
        try:
            icon_paths = ['icon.ico', '../icon.ico']
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    dialog.iconbitmap(icon_path)
                    break
        except:
            pass
        
        dialog.transient(self.root)
        dialog.grab_set()
        
        main = tk.Frame(dialog, bg=self.COLORS['card_bg'], bd=1, relief=tk.FLAT)
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title_frame = tk.Frame(main, bg=self.COLORS['card_bg'])
        title_frame.pack(fill=tk.X, pady=(15, 20))
        
        tk.Label(title_frame,
                text="REDIĢĒT IZDEVUMU",
                font=('Segoe UI', 16, 'bold'),
                bg=self.COLORS['card_bg'],
                fg=self.COLORS['warning']).pack()
        
        canvas = tk.Canvas(title_frame, height=2, bg=self.COLORS['warning'],
                          highlightthickness=0)
        canvas.pack(fill=tk.X, padx=50, pady=5)
        
        content = tk.Frame(main, bg=self.COLORS['card_bg'])
        content.pack(fill=tk.BOTH, expand=True, padx=30)
        
        self.create_input_field(content, "Datums (YYYY-MM-DD):", 0)
        date_entry = self.create_validated_entry(content, 1)
        date_entry.insert(0, expense['date'])
        
        self.create_input_field(content, "Kategorija:", 2)
        category_var = tk.StringVar(value=expense['category'])
        category_combo = ttk.Combobox(content, textvariable=category_var,
                                     values=KATEGORIJAS, state="readonly",
                                     font=('Segoe UI', 11))
        category_combo.grid(row=3, column=0, columnspan=2, sticky='ew', pady=(0, 15))
        
        self.create_input_field(content, "Summa (EUR):", 4)
        amount_entry = self.create_validated_entry(content, 5)
        amount_entry.insert(0, str(expense['amount']))
        
        self.create_input_field(content, "Apraksts:", 6)
        desc_entry = self.create_validated_entry(content, 7)
        desc_entry.insert(0, expense['description'])
        
        error_label = tk.Label(content, text="", bg=self.COLORS['card_bg'],
                              fg=self.COLORS['danger'], font=('Segoe UI', 9))
        error_label.grid(row=8, column=0, columnspan=2, pady=5)
        
        button_frame = tk.Frame(content, bg=self.COLORS['card_bg'])
        button_frame.grid(row=9, column=0, columnspan=2, pady=20)
        
        def validate_date():
            date_text = date_entry.get()
            pattern = r'^\d{4}-\d{2}-\d{2}$'
            if re.match(pattern, date_text):
                try:
                    datetime.strptime(date_text, "%Y-%m-%d")
                    date_entry.configure(bg=self.COLORS['valid'])
                    return True
                except:
                    date_entry.configure(bg=self.COLORS['invalid'])
                    return False
            else:
                date_entry.configure(bg=self.COLORS['invalid'])
                return False
        
        def validate_amount():
            try:
                amount = float(amount_entry.get())
                if amount > 0:
                    amount_entry.configure(bg=self.COLORS['valid'])
                    return True
                else:
                    amount_entry.configure(bg=self.COLORS['invalid'])
                    return False
            except:
                amount_entry.configure(bg=self.COLORS['invalid'])
                return False
        
        def validate_desc():
            if len(desc_entry.get().strip()) > 0:
                desc_entry.configure(bg=self.COLORS['valid'])
                return True
            else:
                desc_entry.configure(bg=self.COLORS['invalid'])
                return False
        
        date_entry.bind('<KeyRelease>', lambda e: validate_date())
        amount_entry.bind('<KeyRelease>', lambda e: validate_amount())
        desc_entry.bind('<KeyRelease>', lambda e: validate_desc())
        
        def save_edit():
            if (validate_date() and validate_amount() and 
                validate_desc() and category_var.get()):
                
                self.expenses[self.editing_index] = {
                    "date": date_entry.get(),
                    "amount": float(amount_entry.get()),
                    "category": category_var.get(),
                    "description": desc_entry.get().strip()
                }
                
                save_expenses(self.expenses)
                self.refresh_table()
                dialog.destroy()
                self.status_bar.config(text=f"✓ Rediģēts: {desc_entry.get()}")
            else:
                error_label.config(text="Lūdzu, aizpildi visus laukus pareizi!")
        
        tk.Button(button_frame, text="SAGLABĀT", command=save_edit,
                 bg=self.COLORS['success'], fg=self.COLORS['fg'],
                 font=('Segoe UI', 11, 'bold'),
                 bd=0, padx=25, pady=8,
                 cursor='hand2').pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="ATCELT", command=dialog.destroy,
                 bg=self.COLORS['danger'], fg=self.COLORS['fg'],
                 font=('Segoe UI', 11),
                 bd=0, padx=25, pady=8,
                 cursor='hand2').pack(side=tk.LEFT, padx=5)
        
        dialog.bind('<Return>', lambda e: save_edit())
        dialog.bind('<Escape>', lambda e: dialog.destroy())
    
    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Brīdinājums", "Izvēlies ierakstu, ko dzēst!")
            return
        
        if messagebox.askyesno("Apstiprinājums", "Vai tiešām vēlies dzēst šo ierakstu?"):
            index = int(self.tree.item(selected[0])['text']) - 1
            deleted = self.expenses.pop(index)
            save_expenses(self.expenses)
            self.refresh_table()
            self.status_bar.config(text=f"✓ Dzēsts: {deleted['description']}")
    
    def copy_description(self):
        selected = self.tree.selection()
        if selected:
            index = int(self.tree.item(selected[0])['text']) - 1
            desc = self.expenses[index]['description']
            self.root.clipboard_clear()
            self.root.clipboard_append(desc)
            self.status_bar.config(text="✓ Apraksts kopēts!")
    
    def export_csv(self):
        filename = f"izdevumi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        if export_to_csv(self.expenses, filename):
            messagebox.showinfo("Veiksmīgi", f"Dati eksportēti uz {filename}")
            self.status_bar.config(text=f"✓ Eksportēts: {filename}")
    
    def backup_data(self):
        import shutil
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = f"expenses_backup_{timestamp}.json"
        
        try:
            shutil.copy2('expenses.json', backup)
            messagebox.showinfo("Veiksmīgi", f"Dublējums izveidots: {backup}")
            self.status_bar.config(text="✓ Dublējums izveidots")
        except:
            messagebox.showerror("Kļūda", "Neizdevās izveidot dublējumu!")
    
    def restore_data(self):
        backups = [f for f in os.listdir('.') if f.startswith('expenses_backup_')]
        if not backups:
            messagebox.showinfo("Informācija", "Nav atrasts neviens dublējums!")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Atjaunot datus")
        dialog.geometry("400x350")
        dialog.configure(bg=self.COLORS['bg'])
        
        try:
            icon_paths = ['icon.ico', '../icon.ico']
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    dialog.iconbitmap(icon_path)
                    break
        except:
            pass
        
        tk.Label(dialog,
                text="IZVĒLIES DUBLĒJUMU",
                font=('Segoe UI', 12, 'bold'),
                bg=self.COLORS['bg'],
                fg=self.COLORS['fg']).pack(pady=15)
        
        listbox = tk.Listbox(dialog, bg=self.COLORS['card_bg'], fg=self.COLORS['fg'],
                            font=('Segoe UI', 10), selectbackground=self.COLORS['accent'])
        listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        for backup in backups:
            listbox.insert(tk.END, backup)
        
        def restore():
            selected = listbox.curselection()
            if selected:
                backup = backups[selected[0]]
                import shutil
                try:
                    shutil.copy2(backup, 'expenses.json')
                    self.expenses = load_expenses()
                    self.refresh_table()
                    dialog.destroy()
                    messagebox.showinfo("Veiksmīgi", "Dati atjaunoti!")
                    self.status_bar.config(text="✓ Dati atjaunoti")
                except:
                    messagebox.showerror("Kļūda", "Neizdevās atjaunot datus!")
        
        tk.Button(dialog, text="ATJAUNOT", command=restore,
                 bg=self.COLORS['success'], fg=self.COLORS['fg'],
                 font=('Segoe UI', 11, 'bold'),
                 bd=0, padx=20, pady=8,
                 cursor='hand2').pack(pady=15)
    
    def set_budget(self):
        from tkinter import simpledialog
        budget = simpledialog.askfloat("Budžets", "Ievadi mēneša budžetu (EUR):",
                                      minvalue=0, maxvalue=100000)
        if budget:
            self.budget_value.set(f"{budget:.2f} €")
            self.update_budget_indicator()
            self.status_bar.config(text=f"✓ Budžets iestatīts: {budget:.2f} €")
    
    def update_budget_indicator(self):
        total = sum_total(self.expenses)
        try:
            budget = float(self.budget_value.get().split()[0])
            
            if budget > 0:
                percent = (total / budget) * 100
                self.budget_progress['value'] = min(percent, 100)
                self.budget_label.config(text=f"{percent:.1f}%")
                
                if percent >= 100:
                    self.budget_label.config(fg=self.COLORS['danger'])
                elif percent >= 80:
                    self.budget_label.config(fg=self.COLORS['warning'])
                else:
                    self.budget_label.config(fg=self.COLORS['success'])
        except:
            pass
    
    def show_statistics_window(self):
        stats = tk.Toplevel(self.root)
        stats.title("Statistika")
        stats.geometry("700x600")
        stats.configure(bg=self.COLORS['bg'])
        
        try:
            icon_paths = ['icon.ico', '../icon.ico']
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    stats.iconbitmap(icon_path)
                    break
        except:
            pass
        
        if not self.expenses:
            tk.Label(stats,
                    text="Nav datu statistikai",
                    font=('Segoe UI', 14),
                    bg=self.COLORS['bg'],
                    fg=self.COLORS['fg']).pack(expand=True)
            return
        
        notebook = ttk.Notebook(stats)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        summary = tk.Frame(notebook, bg=self.COLORS['card_bg'])
        notebook.add(summary, text="📊 Kopsavilkums")
        
        charts = tk.Frame(notebook, bg=self.COLORS['card_bg'])
        notebook.add(charts, text="📈 Grafiki")
        
        details = tk.Frame(notebook, bg=self.COLORS['card_bg'])
        notebook.add(details, text="📋 Detalizēti")
        
        self.add_summary_content(summary)
        self.add_charts_content(charts)
        self.add_details_content(details)
    
    def add_summary_content(self, parent):
        total = sum_total(self.expenses)
        cats = sum_by_category(self.expenses)
        
        text = tk.Text(parent, bg=self.COLORS['bg'], fg=self.COLORS['fg'],
                      font=('Consolas', 11), wrap=tk.WORD, relief=tk.FLAT)
        text.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        text.insert(tk.END, "="*60 + "\n")
        text.insert(tk.END, "📊 STATISTIKAS KOPSAVILKUMS\n")
        text.insert(tk.END, "="*60 + "\n\n")
        
        text.insert(tk.END, f"💰 Kopējie izdevumi: {total:.2f} €\n")
        text.insert(tk.END, f"📝 Ierakstu skaits: {len(self.expenses)}\n")
        text.insert(tk.END, f"📅 Dienu skaits: {len(set(e['date'] for e in self.expenses))}\n\n")
        
        text.insert(tk.END, "📌 Kategoriju sadalījums:\n")
        text.insert(tk.END, "-"*40 + "\n")
        
        for cat, amount in cats.items():
            percent = (amount / total) * 100 if total > 0 else 0
            bars = "█" * int(percent // 2)
            text.insert(tk.END, f"{cat:<20} {amount:>8.2f} € ({percent:>5.1f}%) {bars}\n")
        
        text.config(state=tk.DISABLED)
    
    def add_charts_content(self, parent):
        try:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
            fig.patch.set_facecolor(self.COLORS['card_bg'])
            
            cats = sum_by_category(self.expenses)
            colors = ['#4361ee', '#4cc9f0', '#f8961e', '#f72585', '#7209b7', '#38b000', '#ffd166']
            ax1.pie(cats.values(), labels=cats.keys(), autopct='%1.1f%%', colors=colors)
            ax1.set_title("Kategoriju sadalījums", color=self.COLORS['fg'])
            
            dates = {}
            for e in self.expenses:
                dates[e['date']] = dates.get(e['date'], 0) + e['amount']
            
            x = sorted(dates.keys())
            y = [dates[d] for d in x]
            
            ax2.plot(x, y, marker='o', color=self.COLORS['accent'], linewidth=2, markersize=8)
            ax2.fill_between(x, y, alpha=0.3, color=self.COLORS['accent'])
            ax2.set_title("Izdevumi pa dienām", color=self.COLORS['fg'])
            ax2.tick_params(axis='x', rotation=45, colors=self.COLORS['fg'])
            ax2.tick_params(axis='y', colors=self.COLORS['fg'])
            ax2.set_facecolor(self.COLORS['bg'])
            ax2.grid(True, alpha=0.3, color=self.COLORS['fg'])
            
            plt.tight_layout()
            
            canvas = FigureCanvasTkAgg(fig, parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
        except Exception as e:
            tk.Label(parent,
                    text=f"Kļūda veidojot grafikus: {e}",
                    bg=self.COLORS['card_bg'],
                    fg=self.COLORS['danger']).pack(expand=True)
    
    def add_details_content(self, parent):
        columns = ('Kategorija', 'Ieraksti', 'Kopā (€)', 'Vidēji (€)', 'Min (€)', 'Max (€)')
        
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor='center')
        
        category_stats = {}
        for exp in self.expenses:
            cat = exp['category']
            if cat not in category_stats:
                category_stats[cat] = []
            category_stats[cat].append(exp['amount'])
        
        for cat, amounts in category_stats.items():
            total = sum(amounts)
            avg = total / len(amounts)
            minimum = min(amounts)
            maximum = max(amounts)
            
            tree.insert('', tk.END, values=(
                cat, len(amounts), f"{total:.2f}", f"{avg:.2f}", 
                f"{minimum:.2f}", f"{maximum:.2f}"
            ))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
    
    def show_charts(self):
        self.show_statistics_window()
    
    def show_help(self):
        help_text = """
        📖 LIETOŠANAS INSTRUKCIJA
        
        Īsinājumtaustiņi:
        • Ctrl+N - jauns ieraksts
        • Ctrl+E - rediģēt ierakstu
        • Delete - dzēst ierakstu
        • Ctrl+F - meklēt
        • Ctrl+S - eksportēt CSV
        • F1 - palīdzība
        
        Galvenās funkcijas:
        
        1️⃣ PIEVIENOT IZDEVUMU
        • Ievadi datumu (YYYY-MM-DD)
        • Izvēlies kategoriju
        • Ievadi summu (EUR)
        • Ievadi aprakstu
        
        2️⃣ REDIĢĒT IZDEVUMU
        • Izvēlies ierakstu tabulā
        • Spied Ctrl+E vai dubultklikšķi
        • Labo nepieciešamos laukus
        • Saglabā izmaiņas
        
        3️⃣ DZĒST IZDEVUMU
        • Izvēlies ierakstu
        • Spied Delete vai labo klikšķi
        • Apstiprini dzēšanu
        
        4️⃣ FILTRĒŠANA
        • Izvēlies mēnesi no saraksta
        • Redzēsi tikai tā mēneša izdevumus
        • Spied "Notīrīt filtru", lai redzētu visus
        
        5️⃣ MEKLĒŠANA
        • Ieraksti meklējamo vārdu
        • Meklē pēc apraksta satura
        
        6️⃣ BUDŽETS
        • Iestati mēneša budžetu
        • Seko līdzi izlietojumam
        • Saņem brīdinājumus
        
        7️⃣ EKSPORTS
        • Eksportē datus uz CSV failu
        • Izveido datu dublējumu
        • Atjauno datus no dublējuma
        
        8️⃣ STATISTIKA
        • Apskati kopsavilkumu
        • Skaties grafikus
        • Analizē detalizētu info
        """
        
        messagebox.showinfo("Palīdzība", help_text)
    
    def show_about(self):
        about_text = """
        💰 IZDEVUMU IZSEKOTĀJS PRO
        ===========================
        
        Versija: 3.0
        Izstrādāts: 2026
        
        📝 APRAKSTS
        Profesionāls personīgo finanšu 
        uzskaites rīks ar modernu interfeisu.
        
        ⭐ FUNKCIJAS
        • ✅ Izdevumu pievienošana
        • ✅ Rediģēšana un dzēšana
        • ✅ Filtrēšana pēc mēneša
        • ✅ Meklēšana pēc apraksta
        • ✅ Kategoriju analīze
        • ✅ Grafiki un diagrammas
        • ✅ CSV eksports
        • ✅ Datu dublēšana
        • ✅ Budžeta plānošana
        • ✅ Automātiskā saglabāšana
        • ✅ Īsinājumtaustiņi
        • ✅ Moderns interfeiss
        
        🔧 TEHNISKĀ INFORMĀCIJA
        • Python 3.10+
        • Tkinter GUI
        • Matplotlib vizualizācijas
        • JSON datu glabāšana
        
        👨‍💻 AUTORS
        Izstrādāts mācību projekta ietvaros
        
        © 2026
        """
        
        messagebox.showinfo("Par programmu", about_text)

def main():
    root = tk.Tk()
    app = ModernGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()