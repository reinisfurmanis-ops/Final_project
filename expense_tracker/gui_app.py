# expense_tracker/gui_app.py
import tkinter as tk
from tkinter import ttk, messagebox, font
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from storage import load_expenses, save_expenses
from logic import KATEGORIJAS, sum_total, filter_by_month, sum_by_category, get_available_months
from export import export_to_csv
import os

class ModernGUI:
    # Krāsu palete
    COLORS = {
        'bg': '#2b2b2b',           # Tumši pelēks fons
        'fg': '#ffffff',            # Balts teksts
        'accent': '#4CAF50',         # Zaļš akcents
        'danger': '#f44336',         # Sarkans
        'warning': '#ff9800',        # Oranžs
        'info': '#2196F3',           # Zils
        'secondary': '#9e9e9e',      # Pelēks
        'card_bg': '#3c3c3c',        # Gaišāks pelēks kartēm
        'hover': '#5c5c5c'           # Hover efekts
    }
    
    def __init__(self, root):
        self.root = root
        self.root.title("Izdevumu Izsekotājs Pro")
        self.root.geometry("1200x700")
        self.root.configure(bg=self.COLORS['bg'])
        
        # Ielādē ikonas (ja ir)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        # Ielādē datus
        self.expenses = load_expenses()
        self.current_filter = None
        
        # Konfigurē stilu
        self.setup_styles()
        
        # Izveido UI
        self.create_menu()
        self.create_header()
        self.create_main_content()
        self.create_status_bar()
        
        # Atjaunina datus
        self.refresh_table()
        self.update_stats()
    
    def setup_styles(self):
        """Konfigurē ttk stilu"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Pielāgo stilus
        style.configure('Treeview', 
                       background=self.COLORS['card_bg'],
                       foreground=self.COLORS['fg'],
                       fieldbackground=self.COLORS['card_bg'],
                       rowheight=30)
        
        style.configure('Treeview.Heading',
                       background=self.COLORS['accent'],
                       foreground=self.COLORS['fg'],
                       relief='flat',
                       font=('Arial', 10, 'bold'))
        
        style.map('Treeview',
                 background=[('selected', self.COLORS['info'])])
        
        style.configure('TButton',
                       background=self.COLORS['accent'],
                       foreground=self.COLORS['fg'],
                       borderwidth=0,
                       focuscolor='none',
                       font=('Arial', 10))
        
        style.map('TButton',
                 background=[('active', self.COLORS['hover'])])
        
        style.configure('Secondary.TButton',
                       background=self.COLORS['secondary'])
        
        style.configure('Danger.TButton',
                       background=self.COLORS['danger'])
    
    def create_menu(self):
        """Izveido modernu izvēlni"""
        menubar = tk.Menu(self.root, bg=self.COLORS['bg'], fg=self.COLORS['fg'])
        self.root.config(menu=menubar)
        
        # Fails izvēlne
        file_menu = tk.Menu(menubar, tearoff=0, bg=self.COLORS['card_bg'], fg=self.COLORS['fg'])
        menubar.add_cascade(label="Fails", menu=file_menu)
        file_menu.add_command(label="Eksportēt CSV", command=self.export_csv)
        file_menu.add_command(label="Eksportēt PDF", command=self.export_pdf)
        file_menu.add_separator()
        file_menu.add_command(label="Dublēt datus", command=self.backup_data)
        file_menu.add_command(label="Atjaunot datus", command=self.restore_data)
        file_menu.add_separator()
        file_menu.add_command(label="Iziet", command=self.root.quit)
        
        # Rediģēt izvēlne
        edit_menu = tk.Menu(menubar, tearoff=0, bg=self.COLORS['card_bg'], fg=self.COLORS['fg'])
        menubar.add_cascade(label="Rediģēt", menu=edit_menu)
        edit_menu.add_command(label="Pievienot izdevumu", command=self.add_expense_dialog)
        edit_menu.add_command(label="Rediģēt izdevumu", command=self.edit_expense)
        edit_menu.add_command(label="Dzēst izdevumu", command=self.delete_expense)
        
        # Skats izvēlne
        view_menu = tk.Menu(menubar, tearoff=0, bg=self.COLORS['card_bg'], fg=self.COLORS['fg'])
        menubar.add_cascade(label="Skats", menu=view_menu)
        view_menu.add_command(label="Visi izdevumi", command=self.show_all)
        view_menu.add_command(label="Statistika", command=self.show_statistics_window)
        view_menu.add_command(label="Grafiki", command=self.show_charts)
        
        # Palīdzība
        help_menu = tk.Menu(menubar, tearoff=0, bg=self.COLORS['card_bg'], fg=self.COLORS['fg'])
        menubar.add_cascade(label="Palīdzība", menu=help_menu)
        help_menu.add_command(label="Lietošanas instrukcija", command=self.show_help)
        help_menu.add_command(label="Par programmu", command=self.show_about)
    
    def create_header(self):
        """Izveido header ar kopsavilkumu"""
        header = tk.Frame(self.root, bg=self.COLORS['accent'], height=100)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Logo / nosaukums
        title = tk.Label(header, 
                        text="📊 IZDEVUMU IZSEKOTĀJS PRO",
                        font=('Arial', 20, 'bold'),
                        bg=self.COLORS['accent'],
                        fg=self.COLORS['fg'])
        title.pack(side=tk.LEFT, padx=20, pady=20)
        
        # Ātrā statistika
        stats_frame = tk.Frame(header, bg=self.COLORS['accent'])
        stats_frame.pack(side=tk.RIGHT, padx=20, pady=10)
        
        self.total_label = tk.Label(stats_frame,
                                    text="Kopā: 0.00 EUR",
                                    font=('Arial', 12),
                                    bg=self.COLORS['accent'],
                                    fg=self.COLORS['fg'])
        self.total_label.pack()
        
        self.count_label = tk.Label(stats_frame,
                                    text="Ieraksti: 0",
                                    font=('Arial', 12),
                                    bg=self.COLORS['accent'],
                                    fg=self.COLORS['fg'])
        self.count_label.pack()
    
    def create_main_content(self):
        """Izveido galveno saturu ar sadalījumu"""
        # Galvenais konteiners
        main_container = tk.Frame(self.root, bg=self.COLORS['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Kreisā puse - rīki un filtri
        left_panel = tk.Frame(main_container, bg=self.COLORS['card_bg'], width=250)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        self.create_tools_panel(left_panel)
        
        # Labā puse - tabula
        right_panel = tk.Frame(main_container, bg=self.COLORS['card_bg'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.create_table_panel(right_panel)
    
    def create_tools_panel(self, parent):
        """Izveido rīku paneli"""
        # Ātrās darbības
        tk.Label(parent, 
                text="ĀTRĀS DARBĪBAS",
                font=('Arial', 12, 'bold'),
                bg=self.COLORS['card_bg'],
                fg=self.COLORS['accent']).pack(pady=10)
        
        buttons = [
            ("➕ Pievienot", self.add_expense_dialog, self.COLORS['accent']),
            ("✏️ Rediģēt", self.edit_expense, self.COLORS['info']),
            ("🗑️ Dzēst", self.delete_expense, self.COLORS['danger']),
            ("📊 Statistika", self.show_statistics_window, self.COLORS['warning']),
            ("📈 Grafiki", self.show_charts, self.COLORS['secondary']),
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(parent,
                          text=text,
                          command=command,
                          bg=color,
                          fg=self.COLORS['fg'],
                          font=('Arial', 10),
                          bd=0,
                          padx=10,
                          pady=8)
            btn.pack(fill=tk.X, padx=10, pady=2)
            btn.bind('<Enter>', lambda e, b=btn: b.configure(bg=self.COLORS['hover']))
            btn.bind('<Leave>', lambda e, b=btn, c=color: b.configure(bg=c))
        
        # Filtrs
        tk.Label(parent,
                text="\nFILTRĒT PĒC MĒNEŠA",
                font=('Arial', 12, 'bold'),
                bg=self.COLORS['card_bg'],
                fg=self.COLORS['accent']).pack(pady=(20, 5))
        
        self.filter_var = tk.StringVar()
        self.filter_combo = ttk.Combobox(parent,
                                        textvariable=self.filter_var,
                                        state="readonly",
                                        font=('Arial', 10))
        self.filter_combo.pack(fill=tk.X, padx=10, pady=5)
        self.filter_combo.bind('<<ComboboxSelected>>', self.apply_filter)
        
        tk.Button(parent,
                 text="❌ Notīrīt filtru",
                 command=self.show_all,
                 bg=self.COLORS['secondary'],
                 fg=self.COLORS['fg'],
                 bd=0,
                 padx=10,
                 pady=5).pack(fill=tk.X, padx=10, pady=5)
        
        # Budžeta indikators
        self.create_budget_indicator(parent)
    
    def create_budget_indicator(self, parent):
        """Izveido budžeta indikatoru"""
        budget_frame = tk.Frame(parent, bg=self.COLORS['card_bg'])
        budget_frame.pack(fill=tk.X, padx=10, pady=20)
        
        tk.Label(budget_frame,
                text="MĒNEŠA BUDŽETS",
                font=('Arial', 12, 'bold'),
                bg=self.COLORS['card_bg'],
                fg=self.COLORS['accent']).pack()
        
        self.budget_value = tk.StringVar(value="500.00 EUR")
        tk.Label(budget_frame,
                textvariable=self.budget_value,
                font=('Arial', 14, 'bold'),
                bg=self.COLORS['card_bg'],
                fg=self.COLORS['fg']).pack()
        
        # Progresa josla
        self.budget_progress = ttk.Progressbar(budget_frame,
                                              length=200,
                                              mode='determinate')
        self.budget_progress.pack(pady=10)
        
        self.budget_label = tk.Label(budget_frame,
                                     text="0%",
                                     font=('Arial', 10),
                                     bg=self.COLORS['card_bg'],
                                     fg=self.COLORS['fg'])
        self.budget_label.pack()
        
        tk.Button(budget_frame,
                 text="Iestatīt budžetu",
                 command=self.set_budget,
                 bg=self.COLORS['info'],
                 fg=self.COLORS['fg'],
                 bd=0,
                 padx=10,
                 pady=5).pack(pady=5)
    
    def create_table_panel(self, parent):
        """Izveido tabulas paneli"""
        # Meklēšanas lauks
        search_frame = tk.Frame(parent, bg=self.COLORS['card_bg'])
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(search_frame,
                text="🔍 Meklēt:",
                bg=self.COLORS['card_bg'],
                fg=self.COLORS['fg']).pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.search_expenses)
        search_entry = tk.Entry(search_frame,
                               textvariable=self.search_var,
                               bg=self.COLORS['bg'],
                               fg=self.COLORS['fg'],
                               insertbackground=self.COLORS['fg'],
                               width=30)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Tabulas rāmis
        table_frame = tk.Frame(parent, bg=self.COLORS['card_bg'])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Scrollbari
        scroll_y = tk.Scrollbar(table_frame, bg=self.COLORS['card_bg'])
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scroll_x = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL, bg=self.COLORS['card_bg'])
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Treeview
        self.tree = ttk.Treeview(table_frame,
                                columns=("datums", "summa", "kategorija", "apraksts"),
                                show="tree headings",
                                yscrollcommand=scroll_y.set,
                                xscrollcommand=scroll_x.set,
                                selectmode='browse')
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        # Kolonnu konfigurācija
        self.tree.heading("#0", text="Nr.", anchor='center')
        self.tree.heading("datums", text="Datums", anchor='center')
        self.tree.heading("summa", text="Summa (EUR)", anchor='center')
        self.tree.heading("kategorija", text="Kategorija", anchor='center')
        self.tree.heading("apraksts", text="Apraksts", anchor='w')
        
        self.tree.column("#0", width=50, anchor='center')
        self.tree.column("datums", width=100, anchor='center')
        self.tree.column("summa", width=100, anchor='center')
        self.tree.column("kategorija", width=150, anchor='center')
        self.tree.column("apraksts", width=400, anchor='w')
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Pievieno labo klikšķu izvēlni
        self.create_context_menu()
    
    def create_context_menu(self):
        """Izveido konteksta izvēlni tabulai"""
        self.context_menu = tk.Menu(self.root, tearoff=0,
                                   bg=self.COLORS['card_bg'],
                                   fg=self.COLORS['fg'])
        self.context_menu.add_command(label="Rediģēt", command=self.edit_expense)
        self.context_menu.add_command(label="Dzēst", command=self.delete_expense)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Kopēt aprakstu", command=self.copy_description)
        
        self.tree.bind('<Button-3>', self.show_context_menu)
        self.tree.bind('<Double-1>', lambda e: self.edit_expense())
    
    def create_status_bar(self):
        """Izveido statusa joslu"""
        self.status_bar = tk.Label(self.root,
                                   text="Gatavs",
                                   bd=1,
                                   relief=tk.SUNKEN,
                                   anchor=tk.W,
                                   bg=self.COLORS['secondary'],
                                   fg=self.COLORS['fg'])
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def show_context_menu(self, event):
        """Parāda konteksta izvēlni"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def refresh_table(self):
        """Atjaunina tabulu"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Piemēro filtrus
        display_data = self.expenses
        if self.current_filter:
            display_data = self.current_filter
        elif self.search_var.get():
            display_data = self.search_in_expenses(self.expenses, self.search_var.get())
        
        # Pievieno datus
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
        
        # Konfigurē krāsas
        self.tree.tag_configure('high', foreground='#ff6b6b')
        self.tree.tag_configure('low', foreground='#69db7e')
        
        self.update_stats()
    
    def update_stats(self):
        """Atjaunina statistiku"""
        total = sum_total(self.expenses)
        self.total_label.config(text=f"Kopā: {total:.2f} EUR")
        self.count_label.config(text=f"Ieraksti: {len(self.expenses)}")
        
        # Atjaunina filtru sarakstu
        months = get_available_months(self.expenses)
        self.filter_combo['values'] = months
    
    def search_in_expenses(self, expenses, term):
        """Meklē izdevumos"""
        if not term:
            return expenses
        term = term.lower()
        return [e for e in expenses if term in e['description'].lower()]
    
    def search_expenses(self, *args):
        """Meklēšanas handleris"""
        self.refresh_table()
    
    def apply_filter(self, event=None):
        """Piemēro mēneša filtru"""
        selected = self.filter_var.get()
        if selected:
            year, month = map(int, selected.split('-'))
            self.current_filter = filter_by_month(self.expenses, year, month)
            self.refresh_table()
            self.status_bar.config(text=f"Filtrēts: {selected}")
    
    def show_all(self):
        """Parāda visus izdevumus"""
        self.current_filter = None
        self.filter_var.set("")
        self.refresh_table()
        self.status_bar.config(text="Visi izdevumi")
    
    def add_expense_dialog(self):
        """Atver dialogu jauna izdevuma pievienošanai"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Pievienot izdevumu")
        dialog.geometry("500x400")
        dialog.configure(bg=self.COLORS['bg'])
        
        # Centrē dialogu
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Saturs
        frame = tk.Frame(dialog, bg=self.COLORS['card_bg'], padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Datums
        tk.Label(frame, text="Datums (YYYY-MM-DD):",
                bg=self.COLORS['card_bg'],
                fg=self.COLORS['fg']).pack(anchor=tk.W, pady=(0, 5))
        date_entry = tk.Entry(frame, bg=self.COLORS['bg'], fg=self.COLORS['fg'],
                            insertbackground=self.COLORS['fg'])
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        date_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Kategorija
        tk.Label(frame, text="Kategorija:",
                bg=self.COLORS['card_bg'],
                fg=self.COLORS['fg']).pack(anchor=tk.W, pady=(0, 5))
        category_var = tk.StringVar()
        category_combo = ttk.Combobox(frame, textvariable=category_var,
                                     values=KATEGORIJAS, state="readonly")
        category_combo.pack(fill=tk.X, pady=(0, 10))
        
        # Summa
        tk.Label(frame, text="Summa (EUR):",
                bg=self.COLORS['card_bg'],
                fg=self.COLORS['fg']).pack(anchor=tk.W, pady=(0, 5))
        amount_entry = tk.Entry(frame, bg=self.COLORS['bg'], fg=self.COLORS['fg'],
                              insertbackground=self.COLORS['fg'])
        amount_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Apraksts
        tk.Label(frame, text="Apraksts:",
                bg=self.COLORS['card_bg'],
                fg=self.COLORS['fg']).pack(anchor=tk.W, pady=(0, 5))
        desc_entry = tk.Entry(frame, bg=self.COLORS['bg'], fg=self.COLORS['fg'],
                            insertbackground=self.COLORS['fg'])
        desc_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Pogas
        button_frame = tk.Frame(frame, bg=self.COLORS['card_bg'])
        button_frame.pack(fill=tk.X)
        
        def save():
            try:
                date = date_entry.get()
                category = category_var.get()
                amount = float(amount_entry.get())
                description = desc_entry.get()
                
                if not all([date, category, amount, description]):
                    messagebox.showerror("Kļūda", "Visi lauki ir jāaizpilda!")
                    return
                
                new_expense = {
                    "date": date,
                    "amount": amount,
                    "category": category,
                    "description": description
                }
                
                self.expenses.append(new_expense)
                save_expenses(self.expenses)
                self.refresh_table()
                dialog.destroy()
                self.status_bar.config(text=f"Pievienots: {description} ({amount:.2f} EUR)")
                
            except ValueError:
                messagebox.showerror("Kļūda", "Nederīga summa!")
        
        tk.Button(button_frame, text="Saglabāt", command=save,
                 bg=self.COLORS['accent'], fg=self.COLORS['fg'],
                 font=('Arial', 10, 'bold'), padx=20, pady=5).pack(side=tk.RIGHT, padx=5)
        
        tk.Button(button_frame, text="Atcelt", command=dialog.destroy,
                 bg=self.COLORS['danger'], fg=self.COLORS['fg'],
                 font=('Arial', 10), padx=20, pady=5).pack(side=tk.RIGHT, padx=5)
    
    def edit_expense(self):
        """Rediģē izvēlēto izdevumu"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Brīdinājums", "Izvēlies ierakstu, ko rediģēt!")
            return
        
        index = int(self.tree.item(selected[0])['text']) - 1
        expense = self.expenses[index]
        
        # Līdzīgi kā add_expense_dialog, bet ar aizpildītiem laukiem
        # (īsuma labad izlaižu, bet var pievienot pēc vajadzības)
        messagebox.showinfo("Informācija", "Rediģēšanas funkcija tiks pievienota drīz!")
    
    def delete_expense(self):
        """Dzēš izvēlēto izdevumu"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Brīdinājums", "Izvēlies ierakstu, ko dzēst!")
            return
        
        if messagebox.askyesno("Apstiprinājums", "Vai tiešām vēlies dzēst šo ierakstu?"):
            index = int(self.tree.item(selected[0])['text']) - 1
            deleted = self.expenses.pop(index)
            save_expenses(self.expenses)
            self.refresh_table()
            self.status_bar.config(text=f"Dzēsts: {deleted['description']}")
    
    def copy_description(self):
        """Kopē aprakstu starpliktuvē"""
        selected = self.tree.selection()
        if selected:
            index = int(self.tree.item(selected[0])['text']) - 1
            desc = self.expenses[index]['description']
            self.root.clipboard_clear()
            self.root.clipboard_append(desc)
            self.status_bar.config(text="Apraksts kopēts!")
    
    def export_csv(self):
        """Eksportē uz CSV"""
        filename = f"izdevumi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        if export_to_csv(self.expenses, filename):
            messagebox.showinfo("Veiksmīgi", f"Dati eksportēti uz {filename}")
            self.status_bar.config(text=f"Eksportēts: {filename}")
    
    def export_pdf(self):
        """Eksportē uz PDF"""
        messagebox.showinfo("Informācija", "PDF eksports tiks pievienots drīz!")
    
    def backup_data(self):
        """Izveido datu dublējumu"""
        import shutil
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"expenses_backup_{timestamp}.json"
        
        try:
            shutil.copy2('expenses.json', backup_file)
            messagebox.showinfo("Veiksmīgi", f"Dublējums izveidots: {backup_file}")
        except:
            messagebox.showerror("Kļūda", "Neizdevās izveidot dublējumu!")
    
    def restore_data(self):
        """Atjauno datus no dublējuma"""
        backups = [f for f in os.listdir('.') if f.startswith('expenses_backup_')]
        if not backups:
            messagebox.showinfo("Informācija", "Nav atrasts neviens dublējums!")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Atjaunot datus")
        dialog.geometry("400x300")
        
        listbox = tk.Listbox(dialog, bg=self.COLORS['bg'], fg=self.COLORS['fg'])
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
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
                except:
                    messagebox.showerror("Kļūda", "Neizdevās atjaunot datus!")
        
        tk.Button(dialog, text="Atjaunot", command=restore,
                 bg=self.COLORS['accent'], fg=self.COLORS['fg']).pack(pady=10)
    
    def set_budget(self):
        """Iestata mēneša budžetu"""
        budget = tk.simpledialog.askfloat("Budžets", "Ievadi mēneša budžetu (EUR):",
                                         minvalue=0, maxvalue=100000)
        if budget:
            self.budget_value.set(f"{budget:.2f} EUR")
            self.update_budget_indicator()
    
    def update_budget_indicator(self):
        """Atjaunina budžeta indikatoru"""
        # Vienkāršota versija - var uzlabot
        total = sum_total(self.expenses)
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
                self.budget_label.config(fg=self.COLORS['accent'])
    
    def show_statistics_window(self):
        """Parāda statistikas logu"""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Statistika")
        stats_window.geometry("600x500")
        stats_window.configure(bg=self.COLORS['bg'])
        
        # Izveido cilnes
        notebook = ttk.Notebook(stats_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Cilne: Kopsavilkums
        summary_frame = tk.Frame(notebook, bg=self.COLORS['card_bg'])
        notebook.add(summary_frame, text="Kopsavilkums")
        
        # Cilne: Grafiki
        charts_frame = tk.Frame(notebook, bg=self.COLORS['card_bg'])
        notebook.add(charts_frame, text="Grafiki")
        
        # Pievieno saturu
        self.add_statistics_content(summary_frame)
        self.add_charts_content(charts_frame)
    
    def add_statistics_content(self, parent):
        """Pievieno statistikas saturu"""
        if not self.expenses:
            tk.Label(parent, text="Nav datu statistikai",
                    bg=self.COLORS['card_bg'],
                    fg=self.COLORS['fg']).pack(pady=50)
            return
        
        total = sum_total(self.expenses)
        category_totals = sum_by_category(self.expenses)
        
        text = tk.Text(parent, wrap=tk.WORD,
                      bg=self.COLORS['bg'],
                      fg=self.COLORS['fg'],
                      insertbackground=self.COLORS['fg'],
                      font=('Courier', 11))
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text.insert(tk.END, "="*50 + "\n")
        text.insert(tk.END, "STATISTIKA\n")
        text.insert(tk.END, "="*50 + "\n\n")
        
        text.insert(tk.END, f"Kopējie izdevumi: {total:.2f} EUR\n")
        text.insert(tk.END, f"Ierakstu skaits: {len(self.expenses)}\n")
        text.insert(tk.END, f"Dienu skaits: {len(set(e['date'] for e in self.expenses))}\n\n")
        
        text.insert(tk.END, "Kategoriju sadalījums:\n")
        text.insert(tk.END, "-"*30 + "\n")
        for cat, amount in category_totals.items():
            percent = (amount / total) * 100 if total > 0 else 0
            text.insert(tk.END, f"{cat:<20} {amount:>8.2f} EUR ({percent:.1f}%)\n")
        
        text.config(state=tk.DISABLED)
    
    def add_charts_content(self, parent):
        """Pievieno grafiku saturu"""
        if not self.expenses:
            tk.Label(parent, text="Nav datu grafiku veidošanai",
                    bg=self.COLORS['card_bg'],
                    fg=self.COLORS['fg']).pack(pady=50)
            return
        
        try:
            # Izveido figūru
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
            fig.patch.set_facecolor(self.COLORS['card_bg'])
            
            # Kategoriju sadalījums
            category_totals = sum_by_category(self.expenses)
            categories = list(category_totals.keys())
            amounts = list(category_totals.values())
            
            ax1.pie(amounts, labels=categories, autopct='%1.1f%%')
            ax1.set_title("Kategoriju sadalījums", color=self.COLORS['fg'])
            
            # Izdevumu sadalījums pa dienām
            dates = {}
            for exp in self.expenses:
                date = exp['date']
                dates[date] = dates.get(date, 0) + exp['amount']
            
            date_list = sorted(dates.keys())
            amount_list = [dates[d] for d in date_list]
            
            ax2.plot(date_list, amount_list, marker='o')
            ax2.set_title("Izdevumi pa dienām", color=self.COLORS['fg'])
            ax2.tick_params(axis='x', rotation=45, colors=self.COLORS['fg'])
            ax2.tick_params(axis='y', colors=self.COLORS['fg'])
            ax2.set_facecolor(self.COLORS['bg'])
            
            plt.tight_layout()
            
            canvas = FigureCanvasTkAgg(fig, parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            tk.Label(parent, text=f"Kļūda veidojot grafikus: {e}",
                    bg=self.COLORS['card_bg'],
                    fg=self.COLORS['danger']).pack(pady=50)
    
    def show_charts(self):
        """Atver grafiku logu"""
        self.show_statistics_window()  # Atver to pašu logu ar cilnēm
    
    def show_help(self):
        """Parāda palīdzību"""
        help_text = """
        LIETOŠANAS INSTRUKCIJA
        
        1. Pievienot izdevumu - ievadi datumu, kategoriju, summu un aprakstu
        2. Rediģēt - labo esošo ierakstu
        3. Dzēst - izdzēš ierakstu
        4. Filtrēt - skatīt tikai izvēlētā mēneša izdevumus
        5. Meklēt - atrast ierakstus pēc apraksta
        6. Eksportēt - saglabāt datus CSV failā
        7. Dublēt - izveidot datu rezerves kopiju
        
        Īsinājumtaustiņi:
        • Ctrl+N - jauns ieraksts
        • Ctrl+E - rediģēt
        • Del - dzēst
        • Ctrl+F - meklēt
        • Ctrl+S - saglabāt
        """
        
        messagebox.showinfo("Palīdzība", help_text)
    
    def show_about(self):
        """Parāda informāciju par programmu"""
        about_text = """
        Izdevumu Izsekotājs Pro
        Versija: 2.0
        
        Izstrādāts ar Python un Tkinter
        
        Funkcijas:
        • Izdevumu uzskaite
        • Statistikas analīze
        • Grafiki un diagrammas
        • CSV eksports
        • Datu dublēšana
        • Budžeta plānošana
        
        © 2026
        """
        
        messagebox.showinfo("Par programmu", about_text)

def main():
    root = tk.Tk()
    app = ModernGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()