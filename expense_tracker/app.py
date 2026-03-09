import sys
from datetime import datetime
from storage import load_expenses, save_expenses
from logic import KATEGORIJAS, sum_total, validate_amount, validate_date
from logic import filter_by_month, sum_by_category, get_available_months
from export import export_to_csv, export_filtered_by_month
from logic import check_budget, set_budget, get_statistics, display_statistics
from logic import search_expenses, export_to_txt
monthly_budget = None

def show_menu():
    """Parāda galveno izvēlni"""
    print("\n" + "="*50)
    print("          IZDEVUMU IZSEKOTĀJS")
    print("="*50)
    print("1) Pievienot izdevumu")
    print("2) Parādīt izdevumus")
    print("3) Filtrēt pēc mēneša")
    print("4) Kopsavilkums pa kategorijām")
    print("5) Dzēst izdevumu")
    print("6) Eksportēt CSV")
    print("7) Iziet")
    print("-"*50)
    print("🎁 BONUSA FUNKCIJAS:")
    print("8) Iestatīt budžetu")
    print("9) Budžeta pārbaude")
    print("10) Statistika")
    print("11) Meklēt izdevumos")
    print("12) Eksportēt uz teksta failu")
    print("-"*50)

def add_expense(expenses):
    """
    Pievieno jaunu izdevumu.
    Args:
        expenses (list): Esošo izdevumu saraksts
    """
    print("\n--- PIEVIENOT IZDEVUMU ---")
    
    # Datuma ievade ar validāciju
    while True:
        today = datetime.now().strftime("%Y-%m-%d")
        date_input = input(f"Datums (YYYY-MM-DD) [{today}]: ").strip()
        date = validate_date(date_input)
        if date is not None:
            break
    
    # Kategorijas izvēle
    print("\nKategorijas:")
    for i, cat in enumerate(KATEGORIJAS, 1):
        print(f"  {i}) {cat}")
    
    while True:
        try:
            cat_choice = int(input(f"Izvēlies (1-{len(KATEGORIJAS)}): "))
            if 1 <= cat_choice <= len(KATEGORIJAS):
                category = KATEGORIJAS[cat_choice - 1]
                break
            else:
                print(f"Kļūda: izvēlieties skaitli no 1 līdz {len(KATEGORIJAS)}")
        except ValueError:
            print("Kļūda: ievadiet skaitli")
    
    # Summas ievade ar validāciju
    while True:
        amount_str = input("Summa (EUR): ")
        amount = validate_amount(amount_str)
        if amount is not None:
            break
    
    # Apraksta ievade ar validāciju
    while True:
        description = input("Apraksts: ").strip()
        if description:
            break
        else:
            print("Kļūda: apraksts nevar būt tukšs")
    
    # Jaunā izdevuma izveide
    new_expense = {
        "date": date,
        "amount": amount,
        "category": category,
        "description": description
    }
    
    expenses.append(new_expense)
    
    if save_expenses(expenses):
        print(f"\n✓ Pievienots: {date} | {category} | {amount:.2f} EUR | {description}")
    else:
        print("\n✗ Kļūda: izdevumu neizdevās saglabāt")

def show_expenses(expenses):
    """
    Parāda visus izdevumus tabulas formātā.
    Args:
        expenses (list): Izdevumu saraksts
    """
    print("\n--- VISI IZDEVUMI ---")
    
    if not expenses:
        print("Nav pievienots neviens izdevums.")
        return
    
    # Tabulas galvene
    print("-"*70)
    print(f"{'Nr.':<4} {'Datums':<12} {'Summa':>8} {'Kategorija':<15} {'Apraksts'}")
    print("-"*70)
    
    # Izdevumu rindas
    for i, exp in enumerate(expenses, 1):
        print(f"{i:<4} {exp['date']:<12} {exp['amount']:>8.2f} EUR  {exp['category']:<15} {exp['description']}")
    
    print("-"*70)
    total = sum_total(expenses)
    print(f"{'KOPĀ:':<30} {total:>8.2f} EUR")
    print(f"{'Ierakstu skaits:':<30} {len(expenses)}")
    print("-"*70)

def filter_by_month_interactive(expenses):
    """
    Interaktīva izdevumu filtrēšana pēc mēneša.
    """
    print("\n--- FILTRĒT PĒC MĒNEŠA ---")
    
    if not expenses:
        print("Nav pievienots neviens izdevums.")
        return
    
    # Iegūst pieejamos mēnešus
    available_months = get_available_months(expenses)
    
    if not available_months:
        print("Nav pieejamu mēnešu.")
        return
    
    print("Pieejamie mēneši:")
    for i, month in enumerate(available_months, 1):
        print(f"  {i}) {month}")
    
    try:
        choice = int(input("\nIzvēlies mēnesi (0 lai atceltu): "))
        if choice == 0:
            return
        if 1 <= choice <= len(available_months):
            selected_month = available_months[choice - 1]
            year, month = map(int, selected_month.split('-'))
            
            filtered = filter_by_month(expenses, year, month)
            
            print(f"\n{selected_month} izdevumi:")
            show_expenses(filtered)
        else:
            print("Nederīga izvēle.")
    except ValueError:
        print("Ievadiet skaitli.")

def show_category_summary(expenses):
    """
    Parāda kopsavilkumu pa kategorijām.
    """
    print("\n--- KOPSAVILKUMS PA KATEGORIJĀM ---")
    
    if not expenses:
        print("Nav pievienots neviens izdevums.")
        return
    
    category_totals = sum_by_category(expenses)
    total = sum_total(expenses)
    
    print("-" * 40)
    for category in KATEGORIJAS:
        if category in category_totals:
            print(f"{category:<20} {category_totals[category]:>8.2f} EUR")
    print("-" * 40)
    print(f"{'KOPĀ:':<20} {total:>8.2f} EUR")
    print("-" * 40)

def delete_expense(expenses):
    """
    Dzēš izdevumu pēc numura.
    """
    print("\n--- DZĒST IZDEVUMU ---")
    
    if not expenses:
        print("Nav ko dzēst - izdevumu saraksts ir tukšs.")
        return
    
    # Parāda numurētu sarakstu
    print("Izdevumi:")
    print("-" * 70)
    print(f"{'Nr.':<4} {'Datums':<12} {'Summa':>8} {'Kategorija':<15} {'Apraksts'}")
    print("-" * 70)
    
    for i, exp in enumerate(expenses, 1):
        print(f"{i:<4} {exp['date']:<12} {exp['amount']:>8.2f} EUR  {exp['category']:<15} {exp['description']}")
    
    try:
        choice = int(input("\nKuru dzēst? (numurs vai 0 lai atceltu): "))
        if choice == 0:
            print("Dzēšana atcelta.")
            return
        if 1 <= choice <= len(expenses):
            deleted = expenses.pop(choice - 1)
            if save_expenses(expenses):
                print(f"\n✓ Dzēsts: {deleted['date']} | {deleted['amount']:.2f} EUR | {deleted['category']} | {deleted['description']}")
            else:
                print("\n✗ Kļūda: izdevumu neizdevās saglabāt pēc dzēšanas")
                # Atjauno izdzēsto, ja saglabāšana neizdevās
                expenses.insert(choice - 1, deleted)
        else:
            print(f"Ievadiet numuru no 1 līdz {len(expenses)}")
    except ValueError:
        print("Ievadiet derīgu skaitli.")

def export_csv_interactive(expenses):
    """
    Interaktīva CSV eksportēšana.
    """
    print("\n--- EKSPORTĒT CSV ---")
    
    if not expenses:
        print("Nav ko eksportēt - izdevumu saraksts ir tukšs.")
        return
    
    print("Eksportēt:")
    print("  1) Visus izdevumus")
    print("  2) Tikai viena mēneša izdevumus")
    print("  0) Atcelt")
    
    try:
        choice = input("\nIzvēlies (0-2): ").strip()
        
        if choice == "0":
            print("Eksports atcelts.")
            return
        
        elif choice == "1":
            from export import export_to_csv
            export_to_csv(expenses)
        
        elif choice == "2":
            from logic import get_available_months
            months = get_available_months(expenses)
            
            if not months:
                print("Nav pieejamu mēnešu.")
                return
            
            print("\nPieejamie mēneši:")
            for i, m in enumerate(months, 1):
                print(f"  {i}) {m}")
            
            m_choice = int(input("\nIzvēlies mēnesi: "))
            if 1 <= m_choice <= len(months):
                year, month = map(int, months[m_choice-1].split('-'))
                from export import export_filtered_by_month
                export_filtered_by_month(expenses, year, month)
            else:
                print("Nederīga izvēle.")
        else:
            print("Nederīga izvēle.")
            
    except ValueError:
        print("Ievadiet derīgu skaitli.")
    except Exception as e:
        print(f"Kļūda: {e}")

def main():
    """Galvenā programmas funkcija"""
    global monthly_budget
    expenses = load_expenses()
    
    while True:
        show_menu()
        choice = input("Izvēlies darbību (1-12): ").strip()
        
        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            show_expenses(expenses)
        elif choice == "3":
            filter_by_month_interactive(expenses)
        elif choice == "4":
            show_category_summary(expenses)
        elif choice == "5":
            delete_expense(expenses)
        elif choice == "6":
            export_csv_interactive(expenses)
        elif choice == "7":
            print("\nPaldies par izmantošanu! Uz redzēšanos!")
            sys.exit(0)
        elif choice == "8":
            budget_setup()
        elif choice == "9":
            budget_check(expenses)
        elif choice == "10":
            show_statistics(expenses)
        elif choice == "11":
            search_interactive(expenses)
        elif choice == "12":
            export_txt_interactive(expenses)
        else:
            print("Nepareiza izvēle. Lūdzu, izvēlieties 1-12.")
        
        if choice != "7":
            input("\nSpied Enter, lai turpinātu...")

# ============= BONUSA FUNKCIJAS =============

def budget_setup():
    """Iestata mēneša budžetu"""
    global monthly_budget
    monthly_budget = set_budget()
    print(f"✓ Budžets iestatīts: {monthly_budget:.2f} EUR")

def budget_check(expenses):
    """Pārbauda budžeta izlietojumu"""
    global monthly_budget
    
    if monthly_budget is None:
        print("Vispirms iestati budžetu (opcija 8).")
        return
    
    print("\n--- BUDŽETA PĀRBAUDE ---")
    
    # Iegūst mēnesi no lietotāja
    from logic import get_available_months
    months = get_available_months(expenses)
    
    if not months:
        print("Nav pieejamu mēnešu.")
        return
    
    print("Pieejamie mēneši:")
    for i, m in enumerate(months, 1):
        print(f"  {i}) {m}")
    
    try:
        m_choice = int(input("\nIzvēlies mēnesi: "))
        if 1 <= m_choice <= len(months):
            year, month = map(int, months[m_choice-1].split('-'))
            total, remaining, percent, warning = check_budget(expenses, month, year, monthly_budget)
            
            print(f"\nMēnesis: {months[m_choice-1]}")
            print(f"Izlietots: {total:.2f} EUR ({percent}%)")
            print(f"Atlikums: {remaining:.2f} EUR")
            print(warning)
        else:
            print("Nederīga izvēle.")
    except ValueError:
        print("Ievadiet skaitli.")

def show_statistics(expenses):
    """Parāda statistiku"""
    print("\n--- STATISTIKA ---")
    stats = get_statistics(expenses)
    display_statistics(stats)

def search_interactive(expenses):
    """Interaktīva meklēšana"""
    print("\n--- MEKLĒT IZDEVUMOS ---")
    
    if not expenses:
        print("Nav datu.")
        return
    
    search_term = input("Ievadi meklējamo tekstu: ").strip()
    if not search_term:
        print("Tukšs meklēšanas teksts.")
        return
    
    results = search_expenses(expenses, search_term)
    
    if not results:
        print(f"Nekas netika atrasts ar '{search_term}'.")
        return
    
    print(f"\nAtrasti {len(results)} ieraksti ar '{search_term}':")
    print("-"*70)
    print(f"{'Nr.':<4} {'Datums':<12} {'Summa':>8} {'Kategorija':<15} {'Apraksts'}")
    print("-"*70)
    
    for i, exp in enumerate(results, 1):
        print(f"{i:<4} {exp['date']:<12} {exp['amount']:>8.2f} EUR  {exp['category']:<15} {exp['description']}")

def export_txt_interactive(expenses):
    """Teksta faila eksports"""
    print("\n--- EKSPORTĒT UZ TEKSTA FAILU ---")
    
    if not expenses:
        print("Nav ko eksportēt.")
        return
    
    print("Eksportēt:")
    print("  1) Visus izdevumus")
    print("  2) Tikai viena mēneša izdevumus")
    print("  0) Atcelt")
    
    try:
        choice = input("\nIzvēlies (0-2): ").strip()
        
        if choice == "0":
            return
        elif choice == "1":
            from logic import export_to_txt
            export_to_txt(expenses)
        elif choice == "2":
            from logic import get_available_months
            months = get_available_months(expenses)
            
            if not months:
                print("Nav pieejamu mēnešu.")
                return
            
            print("\nPieejamie mēneši:")
            for i, m in enumerate(months, 1):
                print(f"  {i}) {m}")
            
            m_choice = int(input("\nIzvēlies mēnesi: "))
            if 1 <= m_choice <= len(months):
                year, month = map(int, months[m_choice-1].split('-'))
                from logic import filter_by_month
                filtered = filter_by_month(expenses, year, month)
                export_to_txt(filtered, f"izdevumi_{months[m_choice-1]}.txt")
            else:
                print("Nederīga izvēle.")
        else:
            print("Nederīga izvēle.")
    except ValueError:
        print("Ievadiet skaitli.")

if __name__ == "__main__":
    main()