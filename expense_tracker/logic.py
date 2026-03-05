# expense_tracker/logic.py
from datetime import datetime

# Kategoriju saraksts (saskaņā ar plānu)
KATEGORIJAS = [
    "Ēdiens",
    "Transports",
    "Izklaide",
    "Komunālie maksājumi",
    "Veselība",
    "Iepirkšanās",
    "Cits"
]

def sum_total(expenses):
    """
    Aprēķina visu izdevumu kopsummu.
    Args:
        expenses (list): Izdevumu saraksts
    Returns:
        float: Kopējā summa ar 2 cipariem aiz komata
    """
    return round(sum(expense.get('amount', 0) for expense in expenses), 2)

def validate_amount(amount_str):
    """
    Pārbauda vai ievadītā summa ir derīga.
    Args:
        amount_str (str): Lietotāja ievadītā summa
    Returns:
        float or None: Summa kā float, ja derīga, citādi None
    """
    try:
        amount = float(amount_str)
        if amount <= 0:
            print("Kļūda: summai jābūt lielākai par 0")
            return None
        return round(amount, 2)
    except ValueError:
        print("Kļūda: ievadiet derīgu skaitli (piemēram, 12.50)")
        return None

def validate_date(date_str):
    """
    Pārbauda vai datums ir derīgā YYYY-MM-DD formātā.
    
    Args:
        date_str (str): Lietotāja ievadītais datums
    
    Returns:
        str or None: Datums kā string, ja derīgs, citādi None
    """
    # Ja datums nav ievadīts, izmanto šodienas datumu
    if not date_str:
        return datetime.now().strftime("%Y-%m-%d")
    
    try:
        # Pārbauda vai datums ir pareizā formātā
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        print("Kļūda: nepareizs datuma formāts. Izmantojiet YYYY-MM-DD (piemēram, 2025-02-25)")
        return None