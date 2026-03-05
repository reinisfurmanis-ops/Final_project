# Izdevumu izsekotājs

Komandrindas Python lietojums personīgo izdevumu uzskaitei un analīzei.

## Apraksts

Programma ļauj reģistrēt ikdienas izdevumus, grupēt tos pa kategorijām, 
skatīt mēneša kopsummas un eksportēt datus CSV failā. Dati saglabājas 
JSON failā starp programmas palaišanas reizēm.

## Uzstādīšana

```bash
git clone https://github.com/tavs-lietotajvards/05-Final-project.git
cd 05-Final-project
python expense_tracker/app.py

Lietošana:
1) Pievienot izdevumu
2) Parādīt izdevumus
3) Filtrēt pēc mēneša
4) Kopsavilkums pa kategorijām
5) Dzēst izdevumu
6) Eksportēt CSV
7) Iziet

Piemērs:
Datums (YYYY-MM-DD) [2025-03-05]: > 
Kategorija: 1) Ēdiens 2) Transports ...
Izvēlies (1-7): > 1
Summa (EUR): > 12.50
Apraksts: > Pusdienas

✓ Pievienots: 2025-03-05 | Ēdiens | 12.50 EUR | Pusdienas

CSV eksports
Eksportētie faili tiek saglabāti projekta mapē ar nosaukumu:
izdevumi_YYYYMMDD_HHMMSS.csv - visi izdevumi
izdevumi_YYYY-MM.csv - tikai viena mēneša izdevumi

Autors
Reinis  - Programmēšanas pamati, 2026