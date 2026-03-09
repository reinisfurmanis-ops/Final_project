# Expense Tracker - Izstrādes plāns

## A. Programmas apraksts

**Expense Tracker** ir komandrindas lietotne personīgo izdevumu uzskaitei. Programma ļauj lietotājam pievienot, skatīt, filtrēt un dzēst izdevumu ierakstus, kā arī eksportēt tos CSV formātā. Dati tiek saglabāti JSON failā, nodrošinot to saglabāšanu starp programmas palaišanas reizēm.

Programma ir domāta ikvienam, kas vēlas vienkāršā veidā sekot līdzi saviem tēriņiem bez sarežģītām grāmatvedības sistēmām.

## B. Datu struktūra

### Izdevuma ieraksta piemērs

{
    "date": "2026-03-09",
    "category": "Pārtika",
    "amount": 15.50,
    "note": "Veikals Rimi"
}

### Kāpēc šāda struktūra?

- **date (YYYY-MM-DD)**: ISO formāts nodrošina vieglu datumu salīdzināšanu, filtrēšanu un kārtošanu.
- **category (string)**: Vienkāršs teksta lauks, kas ļauj lietotājam brīvi definēt savas kategorijas.
- **amount (float)**: Decimālskaitlis ļauj precīzi norādīt summu ar diviem cipariem aiz komata.
- **note (string)**: Opcionāls papildu apraksts, kas sniedz kontekstu par izdevumu.

## C. Moduļu plāns

### Projektā būs šādi faili:

expense_tracker/
├── app.py          # Galvenā programmas loģika un lietotāja saskarne
├── storage.py      # Datu ielāde un saglabāšana JSON failā
├── logic.py        # Datu apstrādes funkcijas (filtrēšana, summēšana)
├── export.py       # CSV eksporta funkcionalitāte
docs/
├── plans.md        # Šis plānošanas dokuments
├── DEVLOG.md       # Izstrādes dienasgrāmata
expenses.json       # Datu fails (tiek izveidots automātiski)
.gitignore          # Git ignorējamie faili
README.md           # Projekta apraksts

### storage.py

- `load_expenses(filepath)` - ielādē izdevumus no JSON faila; ja fails neeksistē, atgriež tukšu sarakstu
- `save_expenses(expenses, filepath)` - saglabā izdevumus JSON failā

### logic.py

- `sum_total(expenses)` - aprēķina visu izdevumu kopējo summu
- `filter_by_month(expenses, year, month)` - atgriež izdevumus konkrētajā mēnesī
- `sum_by_category(expenses)` - grupē izdevumus pēc kategorijām un aprēķina summas
- `get_available_months(expenses)` - atgriež visus mēnešus, kuros ir izdevumi (formātā "YYYY-MM")
- `validate_amount(amount_str)` - pārbauda, vai ievadītā summa ir derīga decimālskaitlis (>0)
- `validate_date(date_str)` - pārbauda, vai datums ir derīgs (YYYY-MM-DD formātā)

### export.py

- `export_to_csv(expenses, filepath)` - eksportē izdevumus uz CSV failu (UTF-8 kodējumā)

### app.py

- `show_menu()` - attēlo galveno izvēlni
- `add_expense(expenses)` - pievieno jaunu izdevumu
- `show_expenses(expenses)` - parāda visus izdevumus tabulas formātā
- `filter_by_month_interactive(expenses)` - interaktīva filtrēšana pēc mēneša
- `show_category_summary(expenses)` - parāda kopsavilkumu pa kategorijām
- `delete_expense(expenses)` - dzēš izdevumu pēc indeksa
- `export_csv_interactive(expenses)` - interaktīva CSV eksportēšana
- `main()` - galvenā programmas cilpa

## D. Lietotāja scenāriji

### 1. scenārijs: Izdevuma pievienošana
**Lietotājs**: Izvēlas opciju "Pievienot izdevumu", ievada datumu "2026-03-09", kategoriju "Pārtika", summu "15.50" un piezīmi "Rimi".
**Programma**: Pievieno ierakstu sarakstam, saglabā to failā un parāda apstiprinājumu "Izdevums veiksmīgi pievienots!".

### 2. scenārijs: Izdevumu filtrēšana
**Lietotājs**: Izvēlas opciju "Filtrēt pēc mēneša", programma parāda pieejamos mēnešus. Lietotājs izvēlas mēnesi.
**Programma**: Parāda tikai tā mēneša izdevumus tabulas formātā un kopējo summu.

### 3. scenārijs: Kļūdaina datuma ievade
**Lietotājs**: Pievienojot izdevumu, ievada datumu "2026/03/09" (nepareizs formāts).
**Programma**: Parāda kļūdas paziņojumu "Nederīgs datuma formāts! Izmantojiet YYYY-MM-DD" un ļauj mēģināt vēlreiz.

## E. Robežgadījumi

- **Ja expenses.json neeksistē**: Programma sāk ar tukšu sarakstu un izveido failu, kad pievieno pirmo izdevumu.
- **Ja lietotājs ievada negatīvu summu**: Programma parāda kļūdu "Summai jābūt pozitīvam skaitlim".
- **Ja lietotājs ievada tukšu aprakstu**: Piezīmes lauks var būt tukšs – tas ir opcionāls.
- **Ja lietotājs ievada nepareizu datumu**: Programma parāda kļūdu "Nepareizs datums! Lūdzu, ievadiet derīgu datumu".
- **Ja izdevumu saraksts ir tukšs un lietotājs izvēlas "Parādīt"**: Programma parāda ziņojumu "Nav neviena izdevuma. Pievienojiet pirmo izdevumu!".
- **Ja lietotājs mēģina dzēst izdevumu no tukša saraksta**: Programma paziņo "Nav ko dzēst – izdevumu saraksts ir tukšs".
- **Ja JSON fails ir bojāts**: Programma paziņo par problēmu un sāk ar tukšu sarakstu.

---

**Piezīme:** Šis plāns nav līgums – tas drīkst mainīties izstrādes gaitā. Galvenais ir padomāt pirms kodēšanas!

## Kā ievietot:

```powershell
# 1. Pārliecinies, ka esi feature/planning branch
git checkout feature/planning

# 2. Izveido docs mapi (ja vēl nav)
mkdir -p docs

# 3. Izveido failu un iekopē saturu
# Atver failu ar notepad
notepad docs/plans.md
# Ielīmē tekstu (Ctrl+V) un saglabā (Ctrl+S)

# 4. Pievieno Git
git add docs/plans.md

# 5. Commit
git commit -m "docs: add project plan with data structure and modules"

# 6. Push uz GitHub
git push origin feature/planning