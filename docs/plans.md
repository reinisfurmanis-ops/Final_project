# Plāns: Izdevumu pārvaldnieks (CLI + JSON)

## A. Programmas apraksts (2–3 teikumi)

Izdevumu izsekotājs ir komandrindas Python lietojums, kas palīdz lietotājiem reģistrēt un analizēt ikdienas izdevumus. Programma ļauj pievienot izdevumus ar kategorijām, skatīt tos tabulas formātā, filtrēt pēc mēneša, dzēst ierakstus un eksportēt datus CSV failā tālākai analīzei Excel vai Google Sheets. Dati tiek saglabāti JSON failā, tāpēc tie saglabājas starp programmas palaišanas reizēm.

---

## B. Datu struktūra

### Kā izskatās viens izdevuma ieraksts (piemērs)

```json
{
  "date": "2026-03-05",
  "category": "Ēdiens",
  "amount": 7.80,
  "note": "Pusdienas"
}

Saraksts ar vārdnīcām (list[dict]) ir ērts, jo izdevumi ir secīgi ieraksti (notikumi laikā), un tos vienkārši pievienot ar append().
Lauki ir skaidri un minimāli:
date kā teksts ISO formātā (YYYY-MM-DD) ir viegli salīdzināms un filtrējams.
category ļauj grupēt izdevumus.
amount ir skaitlis aprēķiniem (summa, kopsavilkumi).
note ir brīvs paskaidrojums (nav obligāts).

## C. Moduļi
- expense_tracker/app.py: izvēlne, input/output, validācija
- expense_tracker/storage.py: load/save JSON
- expense_tracker/logic.py: filter, summas, grupēšana
- expense_tracker/export.py: CSV eksports

logic.py
Funkcija	Apraksts
sum_total(expenses)	Aprēķina visu izdevumu kopsummu.
filter_by_month(expenses, year, month)	Atgriež tikai norādītā mēneša izdevumus.
sum_by_category(expenses)	Grupē izdevumus pa kategorijām un aprēķina katras summu.
get_available_months(expenses)	Atrod visus mēnešus, kuros ir izdevumi (formatēti kā "YYYY-MM").
validate_amount(amount_str)	Pārbauda, vai ievadītā summa ir derīga (pozitīvs skaitlis).
validate_date(date_str)	Pārbauda, vai datums ir derīgā YYYY-MM-DD formātā.

export.py
Funkcija	Apraksts
export_to_csv(expenses, filepath)	Eksportē izdevumus CSV failā ar utf-8-sig kodējumu Excel saderībai.

app.py
Galvenā programma saturēs šādas funkcijas:
show_menu() - attēlo izvēlni un saņem lietotāja izvēli
add_expense(expenses) - pievieno jaunu izdevumu
show_expenses(expenses) - parāda visus izdevumus tabulas formātā
filter_by_month_interactive(expenses) - interaktīva filtrēšana pēc mēneša
show_category_summary(expenses) - parāda kopsavilkumu pa kategorijām
delete_expense(expenses) - dzēš izdevumu pēc numura
export_csv_interactive(expenses) - interaktīva CSV eksportēšana
main() - galvenā programmas cilpa


## D. Lietotāja scenāriji
1) Lietotājs pievieno izdevumu ar tukšu datumu → izmanto šodienu.
2) Lietotājs ievada summu kā tekstu → programma parāda kļūdu un prasa vēlreiz.
3) Lietotājs izvēlas filtrēt pēc mēneša → redz tikai attiecīgā mēneša ierakstus un kopsummu.


## E. Robežgadījumi

Scenārijs 1: Pievieno izdevumu korekti
Lietotājs ievada: add 2026-03-05 Ēdiens 7.80 "Pusdienas"

Programma:
pārbauda datumu un summu,
pievieno ierakstu expenses.json,
izvada: ✓ Pievienots: 2026-03-05 — Ēdiens — 7.80 EUR (Pusdienas)

Scenārijs 2: Pievieno izdevumu ar negatīvu summu
Lietotājs ievada: add 2026-03-05 Transports -2.00

Programma:
noraida ievadi,
izvada kļūdu: Kļūda: summai jābūt pozitīvam skaitlim.
neizmaina expenses.json

Scenārijs 3: Lietotājs prasa kopsummu
Lietotājs ievada: total

Programma:
nolasa expenses.json,
saskaita summas,
izvada: Kopā: 123.45 EUR (N ieraksti)


