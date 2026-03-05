# expense_tracker/storage.py
import json
import os

DATA_FILE = "expenses.json"

def load_expenses():
    """
    Ielādē: izdevumus no JSON faila.
    Atgriež: Izdevumu saraksts. Ja neeksistē, atgriež tukšu sarakstu.
    """
    if not os.path.exists(DATA_FILE):
        return []
    
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("Brīdinājums: expenses.json fails ir bojāts. Sākam ar tukšu sarakstu.")
        return []
    except Exception as e:
        print(f"Kļūda ielādējot datus: {e}")
        return []

def save_expenses(expenses):
    """
    Saglabā izdevumus JSON failā.
    Args:
        expenses (list): Izdevumu saraksts, kas jāsaglabā
    Returns:
        bool: True ja saglabāšana veiksmīga, False ja radās kļūda.
    """
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as file:
            json.dump(expenses, file, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Kļūda saglabājot datus: {e}")
        return False