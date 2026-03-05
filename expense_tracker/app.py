import sys
from datetime import datetime
from storage import load_expenses, save_expenses
from logic import KATEGORIJAS, sum_total, validate_amount, validate_date
from logic import filter_by_month, sum_by_category, get_available_months

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
    print("6) Eksportēt CSV (būs pieejams 4. solī)")
    print("7) Iziet")
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

def main():
    """Galvenā programmas funkcija"""
    expenses = load_expenses()
    
    while True:
        show_menu()
        choice = input("Izvēlies darbību (1-7): ").strip()
        
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
            print("\nFunkcija 'Eksportēt CSV' būs pieejama 4. solī.")
            input("\nSpied Enter, lai turpinātu...")
        elif choice == "7":
            print("\nPaldies par izmantošanu! Uz redzēšanos!")
            sys.exit(0)
        else:
            print("Nepareiza izvēle. Lūdzu, izvēlieties 1-7.")
        
        if choice != "7":
            input("\nSpied Enter, lai turpinātu...")

if __name__ == "__main__":
    main()