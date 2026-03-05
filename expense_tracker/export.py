# expense_tracker/export.py
import csv
import os
from datetime import datetime

def export_to_csv(expenses, filepath=None):
    """
    Eksportē izdevumus CSV failā.
    Args:
        expenses (list): Eksportējamo izdevumu saraksts
        filepath (str, optional): CSV faila nosaukums. Ja nav norādīts, ģenerē automātiski.
    Returns:
        bool: True ja eksports veiksmīgs, False ja radās kļūda
        str: Eksportētā faila nosaukums
    """
    if not expenses:
        print("Nav ko eksportēt - izdevumu saraksts ir tukšs.")
        return False, None
    
    # Ja faila nosaukums nav norādīts, ģenerē ar datuma zīmogu
    if not filepath:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"izdevumi_{timestamp}.csv"
    
    # Pārliecinās, ka faila nosaukums beidzas ar .csv
    if not filepath.endswith('.csv'):
        filepath += '.csv'
    
    try:
        with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            
            # Raksta virsrakstus
            writer.writerow(['Datums', 'Summa (EUR)', 'Kategorija', 'Apraksts'])
            
            # Raksta datus
            for expense in expenses:
                writer.writerow([
                    expense['date'],
                    f"{expense['amount']:.2f}",
                    expense['category'],
                    expense['description']
                ])
        
        print(f"\n✓ Eksportēti {len(expenses)} ieraksti uz {filepath}")
        return True, filepath
        
    except PermissionError:
        print(f"Kļūda: nav tiesību rakstīt failu {filepath}")
        return False, None
    except Exception as e:
        print(f"Kļūda eksportējot CSV: {e}")
        return False, None

def export_filtered_by_month(expenses, year, month, filepath=None):
    """
    Eksportē tikai noteiktā mēneša izdevumus uz CSV.
    Args:
        expenses (list): Visi izdevumi
        year (int): Gads
        month (int): Mēnesis
        filepath (str, optional): CSV faila nosaukums
    Returns:
        bool: True ja eksports veiksmīgs
    """
    from logic import filter_by_month
    
    filtered = filter_by_month(expenses, year, month)
    if not filtered:
        print(f"Nav izdevumu {year}-{month:02d} mēnesī.")
        return False
    
    if not filepath:
        filepath = f"izdevumi_{year}-{month:02d}.csv"
    
    return export_to_csv(filtered, filepath)