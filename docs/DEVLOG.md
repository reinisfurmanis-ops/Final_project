# 📋 Izstrādes žurnāls (DEVLOG)

**Projekts:** Izdevumu izsekotājs  
**Autors:** Reinis  
**Laika periods:** 2026. gada marts  

## 1. solis: Plānošana

### 🎯 Izpildītais darbs
- ✅ Izveidota projekta struktūra ar atsevišķām mapēm (`docs/`, `expense_tracker/`)
- ✅ Uzrakstīts `docs/plan.md` ar detalizētu projekta plānu
- ✅ Definēta datu struktūra: JSON formāts ar laukiem `date`, `amount`, `category`, `description`
- ✅ Izplānota moduļu arhitektūra (`app.py`, `storage.py`, `logic.py`, `export.py`)
- ✅ Identificēti robežgadījumi un lietotāja scenāriji
- ✅ Izveidots Git repozitorijs un sākotnējais `feature/planning` branches

### 💡 Grūtības un izaicinājumi
Sākumā bija grūti izlemt, kādas tieši funkcijas būs nepieciešamas `logic.py` modulī. Bija vairākas iespējas, kā strukturēt filtrēšanas un grupēšanas loģiku. Pēc vairāku variantu izvērtēšanas nonācu pie 6 pamatfunkcijām, kas aptver visas nepieciešamās darbības.

### 📚 Iemācītais
- Plānošana pirms kodēšanas patiešām ietaupa laiku - uzreiz redzams kopējais aina
- Feature branch pieeja ļauj strādāt pie atsevišķām funkcionalitātēm bez traucējumiem
- Robežgadījumu definēšana palīdz izvairīties no kļūdām vēlāk

### 📊 Statistika
- Izveidots 1 plānošanas dokuments
- Definētas 7 kategorijas
- Identificēti 12+ robežgadījumi

---

## 2. solis: Datu slānis un pamata darbības (2026-03-06)

### 🎯 Izpildītais darbs
- ✅ Implementēts `storage.py` ar `load_expenses()` un `save_expenses()` funkcijām
- ✅ Izveidots `logic.py` ar summas un datuma validācijas funkcijām
- ✅ Uzrakstīts `app.py` ar pamata izvēlni un 3 komandām (pievienot, parādīt, iziet)
- ✅ Pievienota ievades validācija visiem laukiem (datums, summa, kategorija, apraksts)
- ✅ Izveidota `expenses.json` faila automātiska ģenerēšana
- ✅ Pievienota kļūdu apstrāde failu lasīšanas/rakstīšanas operācijām

### 💡 Grūtības un izaicinājumi
Visgrūtāk bija ar datuma validāciju - sākumā nemaz nezināju par `datetime.strptime()` esamību. Pēc Python dokumentācijas izpētes sapratu, kā to pareizi lietot. Vēl viens izaicinājums bija panākt, lai programma saglabātu latviešu rakstzīmes JSON failā pareizi.

### 📚 Iemācītais
- `datetime` moduļa praktiska lietošana datumu apstrādei un validācijai
- JSON failu lasīšana/rakstīšana ar `ensure_ascii=False` latviešu rakstzīmju atbalstam
- Ievades validācijas nozīme - programma nekrīt ārā pie nederīgas ievades
- `try-except` bloku izmantošana kļūdu apstrādei

### 📊 Statistika
- 3 jauni Python faili (`storage.py`, `logic.py`, `app.py`)
- ~150 koda rindas
- 3 commiti šajā solī

---

## 3. solis: Filtrēšana, kopsavilkums un dzēšana (2026-03-07)

### 🎯 Izpildītais darbs
- ✅ Pievienota `filter_by_month()` funkcija mēneša filtrēšanai
- ✅ Implementēta `sum_by_category()` kategoriju grupēšanai
- ✅ Izveidota `get_available_months()` pieejamo mēnešu iegūšanai
- ✅ Papildināts `app.py` ar 3 jaunām komandām:
  - 3) Filtrēt pēc mēneša
  - 4) Kopsavilkums pa kategorijām
  - 5) Dzēst izdevumu
- ✅ Pievienota interaktīva mēneša izvēle no pieejamajiem mēnešiem
- ✅ Uzlabota izvades formatēšana tabulas veidā

### 💡 Grūtības un izaicinājumi
Dzēšanas funkcijā bija jāpārliecinās, ka pēc dzēšanas dati tiek saglabāti pareizi. Sākumā aizmirsu izsaukt `save_expenses()`, tāpēc pēc programmas restart izdzēstie ieraksti atkal parādījās. Vēl bija jādomā, kā pareizi parādīt lietotājam numurētu sarakstu dzēšanai.

### 📚 Iemācītais
- `defaultdict` lietošana datu grupēšanai pa kategorijām
- Interaktīvu izvēlņu veidošana ar lietotāja ievadi
- Kā pārbaudīt, vai saraksts nav tukšs pirms darbībām
- Datumu parsēšana un formatēšana ar `strptime` un `strftime`

### 📊 Statistika
- 3 jaunas funkcijas `logic.py`
- ~100 jaunas koda rindas
- 3 commiti šajā solī

---

## 4. solis: CSV eksports un dokumentācija 

### 🎯 Izpildītais darbs
- ✅ Izveidots `export.py` ar CSV eksporta funkcijām
- ✅ Pievienota iespēja eksportēt visus vai tikai viena mēneša izdevumus
- ✅ Uzrakstīts `README.md` ar projekta aprakstu un lietošanas instrukciju
- ✅ Papildināts `DEVLOG.md` ar visu soļu aprakstiem
- ✅ Pievienota kļūdu apstrāde eksporta laikā
- ✅ Pārbaudīta CSV failu atvēršana Excel programmā

### 💡 Grūtības un izaicinājumi
Lielākā problēma bija CSV kodējums - sākumā latviešu burti Excel neatvērās pareizi, rādījās "???" vietā. Pēc izpētes atklāju, ka Excel prasa `utf-8-sig` kodējumu ar BOM (Byte Order Mark). Atrisināju, pievienojot `encoding='utf-8-sig'` parametru.

### 📚 Iemācītais
- `csv` moduļa lietošana datu eksportam
- `utf-8-sig` kodējuma nozīme CSV failiem, lai tie būtu saderīgi ar Excel
- Kā uzrakstīt labu README dokumentāciju ar piemēriem
- Markdown sintakses lietošana dokumentācijā

### 📊 Statistika
- 1 jauns fails (`export.py`)
- README.md ar 5 sadaļām
- 3 commiti šajā solī

---

## 5. solis: Bonusa funkcijas

### 🎯 Izpildītais darbs
- ✅ **Budžeta limits** - pievienota iespēja iestatīt mēneša budžetu un saņemt brīdinājumus
- ✅ **Statistika** - pievienota statistika ar vidējiem izdevumiem, dārgāko kategoriju
- ✅ **Meklēšana** - iespēja meklēt izdevumus pēc atslēgvārdiem aprakstā
- ✅ **Teksta eksports** - eksports uz .txt failu cilvēklasāmā formātā
- ✅ Papildināta izvēlne ar 4 jaunām opcijām (8-12)
- ✅ Uzlabota statistikas vizualizācija ar procentu stabiņiem

### 💡 Grūtības un izaicinājumi
Budžeta funkcijā bija jāpatur prātā, ka budžets ir jāsaglabā starp sesijām. Izveidoju globālo mainīgo, bet sapratu, ka tas nepietiek - nācās budžetu saglabāt konfigurācijas failā. Statistikas aprēķinos bija jārēķinās ar iespēju, ka nav datu.

### 📚 Iemācītais
- Kā aprēķināt un vizualizēt statistiku
- Datu meklēšana pēc atslēgvārdiem
- Teksta failu veidošana ar formatētu izvadi
- Lietotāja pieredzes uzlabošana ar vizuāliem elementiem (procentu stabiņi)

### 📊 Statistika
- 4 jaunas funkcijas
- ~150 jaunas koda rindas
- 2 commiti šajā solī

---

## 6. solis: GUI versijas izstrāde

### 🎯 Izpildītais darbs
- ✅ Izveidots `gui_app.py` ar Tkinter grafisko interfeisu
- ✅ Moderns dizains ar tumšo tēmu un gradientiem
- ✅ Pievienota reāllaika validācija ievades laukiem
- ✅ Rediģēšanas funkcija ar dubultklikšķi uz ieraksta
- ✅ Grafiki un diagrammas ar Matplotlib
- ✅ Budžeta indikators ar progresa joslu
- ✅ Statusa josla ar pulksteni un ierakstu skaitu
- ✅ Konteksta izvēlne (labais klikšķis)
- ✅ Īsinājumtaustiņi (Ctrl+N, Ctrl+E, Delete u.c.)

### 💡 Grūtības un izaicinājumi
Vislielākais izaicinājums bija Tkinter izpratne un logu pārvaldība. Sākumā bija grūti saprast, kā pareizi organizēt loga elementus, lai tie būtu responsīvi. Gradienta fona izveide prasīja vairākus eksperimentus ar Canvas elementu. Grafiku integrācija ar Matplotlib bija pārsteidzoši vienkārša.

### 📚 Iemācītais
- Tkinter logu un elementu izvietošana (`pack`, `grid`, `place`)
- Notikumu apstrāde un bindings
- Grafiku zīmēšana ar Matplotlib
- Krāsu teorija un interfeisa dizains
- Lietotāja pieredzes uzlabošana ar vizuāliem elementiem

### 📊 Statistika
- 1 jauns fails (`gui_app.py`)
- ~800 koda rindas
- 2 commiti šajā solī

---

## 7. solis: .exe faila izveide

### 🎯 Izpildītais darbs
- ✅ Instalēts PyInstaller
- ✅ Izveidots izpildāmais `.exe` fails
- ✅ Pievienota programmas ikona (`icon.ico`)
- ✅ Pārbaudīta programmas darbība bez Python instalācijas
- ✅ Izveidots īsceļš uz darbvirsmas
- ✅ Pievienota informācija README par .exe versiju

### 💡 Grūtības un izaicinājumi
Sākumā bija problēmas ar `--windowed` parametru - programma prasīja ievadi, bet nebija kur to ievadīt. Atrisināju, izveidojot divas versijas - ar un bez konsoles loga. GUI versijai izmantoju `--windowed`, lai nebūtu lieka loga.

### 📚 Iemācītais
- PyInstaller lietošana .exe failu veidošanai
- Ikonu pievienošana programmai
- Kā izveidot pārnēsājamu programmu
- Programmas izplatīšana bez Python instalācijas

### 📊 Statistika
- 1 `.exe` fails (~30 MB)
- 1 ikona (`icon.ico`)
- Programma darbojas uz jebkura Windows datora

---

## 🏆 Nobeigums un secinājumi

### 📊 Kopējā statistika
| Rādītājs | Vērtība |
|----------|---------|
| Python faili | 5 (`app.py`, `gui_app.py`, `storage.py`, `logic.py`, `export.py`) |
| Koda rindas | ~1200 |
| Commiti | 14+ |
| Feature branchi | 7 |
| Funkcijas | 25+ |

### 💪 Iegūtās prasmes
Šī projekta laikā nostiprināju un pielietoju visas kursā apgūtās prasmes. Kopumā guvu labu ieskatu, ko nozīmē programēt, bet sapratu ka daudz vēl jāmācās, lai varētu patstāvīgi rakstīt kodu bez palīgrīkiem.
