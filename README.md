# 💰 Izdevumu izsekotājs

Komandrindas un grafiskā lietojumprogramma personīgo finanšu uzskaitei un analīzei. Izstrādāts Python valodā, pieejams gan kā avota kods, gan kā gatava .exe programma.

## Par projektu
Šis ir mācību projekts, kas izstrādāts programmēšanas pamatu kursa ietvaros. Tā mērķis ir izveidot pilnvērtīgu, praktiski lietojamu programmu, kas apvieno visas kursā apgūtās prasmes. Projekta ietvaros tika realizēti visi 4 pamata soļi (plānošana, datu slānis, filtrēšana, eksports), 4 bonusa uzdevumi (budžets, statistika, meklēšana, teksta eksports), grafiskā interfeisa (GUI) versija un gatava .exe programma bez Python instalācijas.

## Funkcionalitāte
Pamata funkcijas: 
1) Pievienot izdevumu - ievadi datumu, kategoriju, summu un aprakstu; 
2) Parādīt izdevumus - attēlo visus izdevumus tabulas formātā; 
3) Filtrēt pēc mēneša - skatīt tikai izvēlētā mēneša izdevumus; 
4) Kopsavilkums pa kategorijām - grupē izdevumus pa kategorijām; 
5) Dzēst izdevumu - izdzēst nevajadzīgu ierakstu; 
6) Eksportēt CSV - saglabāt datus CSV failā (Excel saderīgs); 
7) Iziet - pārtraukt programmas darbu.

Bonusa funkcijas: 
8) Iestatīt budžetu - noteikt mēneša tēriņu limitu; 
9) Budžeta pārbaude - pārbaudīt, cik daudz no budžeta izlietots; 
10) Statistika - vidējie izdevumi, dārgākā kategorija, grafiki; 
11) Meklēt izdevumos - meklēt pēc atslēgvārdiem aprakstā; 
12) Eksportēt uz teksta failu - cilvēklasāms pārskats .txt formātā.

GUI versijas papildus iespējas(Izveidota treniņā nolūkā ar MI, lai saprastu kā veidojas): moderns interfeiss ar tumšo tēmu, pogām, kartēm un gradientiem; reāllaika validācija - 
ievades lauki maina krāsu, rakstot; 
rediģēšana - iespēja labot esošos ierakstus; 
meklēšanas lauks - ātra atlase pēc atslēgvārdiem; 
grafiki un diagrammas - vizuāla datu analīze; 
budžeta indikators - progresa josla ar brīdinājuma krāsām; statusa josla ar pulksteni, ierakstu skaitu un darbību apstiprinājumiem; konteksta izvēlne - labā klikšķa izvēlne ar papildus opcijām; 
īsinājumtaustiņi - Ctrl+N, Ctrl+E, Delete u.c.

## Uzstādīšana
1. variants: Python avota kods - git clone https://github.com/reinisfurmanis-ops/Final_project.git, cd Final_project, python expense_tracker/app.py (komandrindas versija) vai python expense_tracker/gui_app.py (grafiskā versija). Prasības: Python 3.10 vai jaunāks, GUI versijai papildus -  pip install matplotlib.

2. variants: Gatavā programma (.exe) - lejupielādē jaunāko versiju no Releases sadaļas, izvēlies failu IzdevumuIzsekotajs.exe, saglabā vēlamajā mapē (piemēram, darbvirsmā), palaid ar dubultklikšķi. Dati tiek saglabāti tajā pašā mapē, kur atrodas .exe fails. Ieteicams izveidot atsevišķu mapi programmai.

## Lietošana
   IZDEVUMU IZSEKOTĀJS
══════════════════════════════════════════

1) Pievienot izdevumu
2) Parādīt izdevumus
3) Filtrēt pēc mēneša
4) Kopsavilkums pa kategorijām
5) Dzēst izdevumu
6) Eksportēt CSV
7) Iziet
──────────────────────────────────────────
🎁 BONUSA FUNKCIJAS:
8) Iestatīt budžetu
9) Budžeta pārbaude
10) Statistika
11) Meklēt izdevumos
12) Eksportēt uz teksta failu
──────────────────────────────────────────
Izvēlies darbību (1-12):

## Pievienošanas piemērs
Izvēlies: > 1

Datums (YYYY-MM-DD) [2026-03-05]: > 
Kategorija: 
  1) Ēdiens
  2) Transports
  3) Izklaide
  4) Komunālie maksājumi
  5) Veselība
  6) Iepirkšanās
  7) Cits
Izvēlies (1-7): > 1
Summa (EUR): > 12.50
Apraksts: > Pusdienas

✓ Pievienots: 2026-03-05 | Ēdiens | 12.50 EUR | Pusdienas

## Izdevumu apskates piemērs
Izvēlies: > 2

────────────────────────────────────────────────────────────────
Nr.  Datums         Summa     Kategorija      Apraksts
────────────────────────────────────────────────────────────────
1    2026-03-05    12.50 EUR  Ēdiens          Pusdienas
2    2026-03-06     5.60 EUR  Transports      Autobusa biļete
3    2026-03-07    45.00 EUR  Izklaide        Kino
────────────────────────────────────────────────────────────────
KOPĀ:                          63.10 EUR
Ierakstu skaits:               3

## Statistikas piemērs
Izvēlies: > 10

══════════════════════════════════════════
          STATISTIKA
══════════════════════════════════════════

Kopējie izdevumi:    187.50 EUR
Ierakstu skaits:     15
Vidēji dienā:        12.50 EUR

Kategoriju sadalījums:
──────────────────────────────────────────
Ēdiens               85.20 EUR  ██████████
Transports           32.30 EUR  ████
Izklaide             45.00 EUR  █████
Veselība             25.00 EUR  ███

## Budžeta pārbaudes piemērs
Izvēlies: > 9

Mēneša budžets: 500.00 EUR

2026. gada Marts:
Izlietots: 425.50 EUR (85.1%)
Atlikums:  74.50 EUR

⚠️ UZMANĪBU! Izlietoti 85% no budžeta!

## Meklēšanas piemērs
Izvēlies: > 11

Meklējamais teksts: kafija

Atrasti 3 ieraksti:
────────────────────────────────────────────────────────────────
1    2026-02-15    4.50 EUR  Ēdiens     Kafija un kūka
2    2026-02-22    3.20 EUR  Ēdiens     Rīta kafija
3    2026-03-01    4.00 EUR  Ēdiens     Kafija ar pienu
────────────────────────────────────────────────────────────────

## Izmantotās tehnoloģijas
Python 3.10+ -	Programmas pamatvaloda
Tkinter	Grafiskā - interfeisa izveide
Matplotlib - Grafiku un diagrammu zīmēšana
JSON - Datu saglabāšana
CSV - Datu eksports
PyInstaller - .exe faila izveide

## GIT branch struktūra
main (galvenais branch)
├── feature/planning      # 1. solis: plānošana
├── feature/core          # 2. solis: datu slānis
├── feature/filters       # 3. solis: filtrēšana
├── feature/export-docs   # 4. solis: eksports
├── feature/bonus         # Bonusa funkcijas
└── feature/gui           # Grafiskā versija


## Projekta struktūra
05-Final-project/ satur expense_tracker/ mapi ar programmas kodu (app.py, gui_app.py, storage.py, logic.py, export.py), docs/ mapi ar dokumentāciju (plan.md un DEVLOG.md), dist/ mapi ar izveidoto .exe programmu (IzdevumuIzsekotajs.exe), expenses.json datu failu, icon.ico ikonu, README.md un .gitignore.

## Tehniskās detaļas
Vēlos norādīt ka izstrādāta mini aplikācija, ko var atvērt python expense_tracker/gui_app.py ir tīri vairākas reizes ģenerēts kods. Vēlējos saprast vai un cik vienkārši ir šādu termināl izdevumu izsekotāju pārvērst reālā programā. Bet arī iemācijos dažas lietas, piemērām kā formatēt galveni app.py 109-111 rindas.

Git branch struktūra: main (galvenais branch) ar atzariem feature/planning (1. solis: plānošana), feature/core (2. solis: datu slānis), feature/filters (3. solis: filtrēšana), feature/export-docs (4. solis: eksports), feature/bonus (bonusa funkcijas) un feature/gui (grafiskā versija). Kopējais commit skaits: 14+.

Eksporta formāti: CSV (komanda 6) - dati atverami Excel un Google Sheets, teksta fails (komanda 12) - cilvēklasāms formāts, piemērots drukāšanai. Eksportētie faili tiek automātiski saglabāti projekta saknes mapē ar nosaukumu izdevumi_YYYYMMDD_HHMMSS.csv (visi izdevumi), izdevumi_YYYY-MM.csv (tikai viena mēneša izdevumi) un izdevumi_YYYYMMDD_HHMMSS.txt (teksta eksports).

## Autors
Reinis, 
Programmēšanas pamati, 2026. 
GitHub: @reinisfurmanis-ops, repozitorijs: github.com/reinisfurmanis-ops/Final_project, 
izstrādes laiks: 2026. gada marts.