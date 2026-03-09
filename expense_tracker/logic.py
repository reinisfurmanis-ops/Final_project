from datetime import datetime
from collections import defaultdict

# Kategoriju saraksts
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

def filter_by_month(expenses, year, month):
    """
    Atgriež izdevumus, kas atbilst norādītajam gadam un mēnesim.
    Args:
        expenses (list): Visi izdevumi
        year (int): Gads (piemēram, 2025)
        month (int): Mēnesis (1-12)
    Returns:
        list: Filtrētie izdevumi
    """
    filtered = []
    for expense in expenses:
        expense_date = datetime.strptime(expense['date'], "%Y-%m-%d")
        if expense_date.year == year and expense_date.month == month:
            filtered.append(expense)
    return filtered

def sum_by_category(expenses):
    """
    Grupē izdevumus pa kategorijām un aprēķina katras summu.
    Args:
        expenses (list): Izdevumu saraksts
    Returns:
        dict: Vārdnīca ar {kategorija: summa}
    """
    totals = defaultdict(float)
    for expense in expenses:
        category = expense['category']
        totals[category] += expense['amount']
    
    # Noapaļo un pārvērš par parastu vārdnīcu
    return {cat: round(amount, 2) for cat, amount in totals.items()}

def get_available_months(expenses):
    """
    Atrod visus mēnešus, kuros ir izdevumi.
    Args:
        expenses (list): Izdevumu saraksts
    Returns:
        list: Unikālu mēnešu saraksts formatētā kā "YYYY-MM"
    """
    months = set()
    for expense in expenses:
        date_obj = datetime.strptime(expense['date'], "%Y-%m-%d")
        months.add(date_obj.strftime("%Y-%m"))
    
    return sorted(list(months))