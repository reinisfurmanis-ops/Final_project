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

# ============= BONUSA FUNKCIJAS =============

# 1. BUDŽETA LIMITS
def check_budget(expenses, month, year, budget):
    """
    Pārbauda vai mēneša izdevumi nepārsniedz budžetu.
    Args:
        expenses (list): Visi izdevumi
        month (int): Mēnesis
        year (int): Gads
        budget (float): Mēneša budžets
    Returns:
        tuple: (kopējā summa, atlikums, procenti, brīdinājums)
    """
    month_expenses = filter_by_month(expenses, year, month)
    total = sum_total(month_expenses)
    
    remaining = budget - total
    percent = (total / budget) * 100 if budget > 0 else 0
    
    warning = ""
    if percent >= 100:
        warning = "❌ BUDŽETS PĀRSNIEGTS!"
    elif percent >= 90:
        warning = "⚠️ UZMANĪBU! Izlietoti 90% no budžeta!"
    elif percent >= 75:
        warning = "⚠️ Izlietoti 75% no budžeta."
    
    return total, remaining, round(percent, 1), warning

def set_budget():
    """
    Interaktīva budžeta iestatīšana.
    Returns:
        float: Iestatītais budžets
    """
    while True:
        try:
            budget = float(input("Ievadi mēneša budžetu (EUR): "))
            if budget <= 0:
                print("Budžetam jābūt lielākam par 0.")
                continue
            return budget
        except ValueError:
            print("Ievadi derīgu skaitli.")

# 2. STATISTIKA
def get_statistics(expenses):
    """
    Aprēķina dažādus statistikas rādītājus.
    Args:
        expenses (list): Izdevumu saraksts
    Returns:
        dict: Statistikas dati
    """
    if not expenses:
        return None
    
    # Dienu skaits (unikālie datumi)
    unique_dates = set(exp['date'] for exp in expenses)
    days_count = len(unique_dates)
    
    # Kopējie rādītāji
    total = sum_total(expenses)
    avg_per_day = total / days_count if days_count > 0 else 0
    avg_per_expense = total / len(expenses)
    
    # Dārgākais izdevums
    most_expensive = max(expenses, key=lambda x: x['amount'])
    
    # Kategoriju analīze
    category_totals = sum_by_category(expenses)
    top_category = max(category_totals.items(), key=lambda x: x[1]) if category_totals else ("Nav", 0)
    
    # Izdevumu skaits pa dienām
    expenses_by_date = {}
    for exp in expenses:
        date = exp['date']
        expenses_by_date[date] = expenses_by_date.get(date, 0) + 1
    
    stats = {
        'total': total,
        'count': len(expenses),
        'days': days_count,
        'avg_per_day': round(avg_per_day, 2),
        'avg_per_expense': round(avg_per_expense, 2),
        'most_expensive': most_expensive,
        'top_category': top_category,
        'expenses_by_date': expenses_by_date
    }
    
    return stats

def display_statistics(stats):
    """
    Attēlo statistiku terminālī.
    """
    if not stats:
        print("Nav datu statistikai.")
        return
    
    print("\n" + "="*50)
    print("📊 STATISTIKA")
    print("="*50)
    
    print(f"Kopējie izdevumi:    {stats['total']:.2f} EUR")
    print(f"Ierakstu skaits:     {stats['count']}")
    print(f"Dienu skaits:        {stats['days']}")
    print(f"Vidēji dienā:        {stats['avg_per_day']:.2f} EUR")
    print(f"Vidēji ierakstā:     {stats['avg_per_expense']:.2f} EUR")
    
    print(f"\n🏆 Dārgākais ieraksts:")
    print(f"   {stats['most_expensive']['date']} | {stats['most_expensive']['amount']:.2f} EUR | {stats['most_expensive']['category']} | {stats['most_expensive']['description']}")
    
    print(f"\n📈 Populārākā kategorija: {stats['top_category'][0]} ({stats['top_category'][1]:.2f} EUR)")
    
    print("\n📅 Izdevumu skaits pa dienām:")
    print("-" * 40)
    for date, count in sorted(stats['expenses_by_date'].items()):
        bars = "█" * count
        print(f"{date}: {count} {bars}")

# 3. MEKLĒŠANA
def search_expenses(expenses, search_term):
    """
    Meklē izdevumus pēc teksta aprakstā.
    Args:
        expenses (list): Izdevumu saraksts
        search_term (str): Meklējamais teksts
    Returns:
        list: Atrastie izdevumi
    """
    search_term = search_term.lower()
    results = []
    
    for exp in expenses:
        if search_term in exp['description'].lower():
            results.append(exp)
    
    return results

# 4. TEKSTA EKSPORTS
def export_to_txt(expenses, filepath=None):
    """
    Eksportē izdevumus uz teksta failu.
    Args:
        expenses (list): Eksportējamie izdevumi
        filepath (str, optional): Faila nosaukums
    Returns:
        bool: True ja eksports veiksmīgs
    """
    if not expenses:
        print("Nav ko eksportēt.")
        return False
    
    if not filepath:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"izdevumi_{timestamp}.txt"
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("IZDEVUMU PĀRSKATS\n")
            f.write("="*60 + "\n\n")
            
            total = sum_total(expenses)
            
            for i, exp in enumerate(expenses, 1):
                f.write(f"{i}. {exp['date']} | {exp['amount']:.2f} EUR | {exp['category']}\n")
                f.write(f"   {exp['description']}\n\n")
            
            f.write("-"*60 + "\n")
            f.write(f"KOPĀ: {total:.2f} EUR ({len(expenses)} ieraksti)\n")
            f.write("="*60 + "\n")
        
        print(f"✓ Eksportēts uz '{filepath}'")
        return True
        
    except Exception as e:
        print(f"Kļūda eksportējot: {e}")
        return False