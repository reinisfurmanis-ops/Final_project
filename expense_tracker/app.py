# expense_tracker/app.py
import sys
from datetime import datetime
from storage import load_expenses, save_expenses
from logic import KATEGORIJAS, sum_total, validate_amount, validate_date

def show_menu():
    """Parāda galveno izvēlni"""
    print("\n" + "="*50)
    print("          IZDEVUMU IZSEKOTĀJS")
    print("="*50)
    print("1) Pievienot izdevumu")
    print("2) Parādīt izdevumus")
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

def main():
    """Galvenā programmas funkcija"""
    expenses = load_expenses()
    
    while True:
        show_menu()
        choice = input("Izvēlies darbību (1, 2 vai 7): ").strip()
        
        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            show_expenses(expenses)
        elif choice == "7":
            print("\nPaldies par izmantošanu! Uz redzēšanos!")
            sys.exit(0)
        else:
            print("Nepareiza izvēle. Lūdzu, izvēlieties 1, 2 vai 7.")
        
        input("\nSpied Enter, lai turpinātu...")

if __name__ == "__main__":
    main()