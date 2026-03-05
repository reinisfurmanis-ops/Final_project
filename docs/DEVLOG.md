# Izstrādes žurnāls (DEVLOG)

## 1. solis: Plānošana (2025-03-05)
**Izpildītais darbs:**
- Izveidoju `docs/plan.md` ar projekta plānu
- Aprakstīju datu struktūru (JSON formāts ar laukiem: date, amount, category, description)
- Plānoju moduļu struktūru (app.py, storage.py, logic.py, export.py)
- Definēju robežgadījumus un lietotāja scenārijus

**Grūtības:**
Sākumā bija grūti izdomāt, kādas tieši funkcijas būs nepieciešamas `logic.py` modulī. 
Pēc vairākiem variantiem beidzot nonācu pie 6 pamatfunkcijām.

**Iemācītais:**
Plānošana pirms kodēšanas ļauj ietaupīt laiku vēlāk - uzreiz redzu, kādas funkcijas man būs nepieciešamas.

---

## 2. solis: Datu slānis un pamata darbības (2025-03-06)
**Izpildītais darbs:**
- Implementēju `storage.py` ar `load_expenses()` un `save_expenses()`
- Izveidoju `logic.py` ar summu validāciju un datuma validāciju
- Uzrakstīju `app.py` ar pamata izvēlni un 3 komandām (pievienot, parādīt, iziet)
- Pievienoju ievades validāciju visiem laukiem

**Grūtības:**
Visgrūtāk bija ar datuma validāciju - sākumā nemaz nezināju par `datetime.strptime()`.
Pēc dokumentācijas izlasīšanas sapratu, kā to pareizi lietot.

**Iemācītais:**
- `datetime` moduļa lietošana datumu apstrādei
- JSON failu lasīšana/rakstīšana ar latviešu rakstzīmēm
- Ievades validācijas nozīme - programma nekrīt ārā pie nederīgas ievades

---

## 3. solis: Filtrēšana, kopsavilkums un dzēšana (2025-03-07)
**Izpildītais darbs:**
- Pievienoju `filter_by_month()` funkciju
- Implementēju `sum_by_category()` grupēšanai
- Izveidoju `get_available_months()` pieejamo mēnešu iegūšanai
- Papildināju `app.py` ar 3 jaunām komandām (filtrēt, kopsavilkums, dzēst)

**Grūtības:**
Dzēšanas funkcijā bija jāpārliecinās, ka pēc dzēšanas dati tiek saglabāti pareizi.
Sākumā aizmirsu izsaukt `save_expenses()`, tāpēc pēc programmas restart datus vēlreiz parādījās.

**Iemācītais:**
- defaultdict lietošana datu grupēšanai
- Kā veidot interaktīvas izvēlnes ar lietotāja ievadi
- Svarīgi vienmēr pārbaudīt, vai saraksts nav tukšs pirms darbībām

---

## 4. solis: CSV eksports un dokumentācija (2025-03-08)
**Izpildītais darbs:**
- Izveidoju `export.py` ar CSV eksporta funkcijām
- Pievienoju iespēju eksportēt visus vai tikai viena mēneša izdevumus
- Uzrakstīju `README.md` ar projekta aprakstu un lietošanas instrukcijām
- Papildināju `DEVLOG.md` ar visu soļu aprakstiem

**Grūtības:**
CSV kodējums - sākumā latviešu burti Excel neatvērās pareizi.
Atrisināju, lietojot `encoding='utf-8-sig'` (ar BOM), ko Excel atpazīst.

**Iemācītais:**
- `csv` moduļa lietošana datu eksportam
- utf-8-sig kodējuma nozīme CSV failiem
- Kā uzrakstīt labu README dokumentāciju

---

## Kopējais iespaids

Šis projekts bija lieliska iespēja izmantot visas kursa laikā apgūtās prasmes:
- 1. nedēļa: Git, termināļa lietošana
- 2. nedēļa: datu tipi, cikli, nosacījumi
- 3. nedēļa: funkcijas, moduļi, import
- 4. nedēļa: JSON, failu I/O
- 5. nedēļa: datetime, csv, plānošana, dokumentācija
