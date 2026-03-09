# Expense Tracker - Izstrādes plāns

## A. Programmas apraksts

Programma ir komandrindas rīks, kas ļauj lietotājam pievienot, apskatīt un analizēt personīgos izdevumus. Tā glabā datus JSON failā, lai izdevumi saglabātos starp palaišanām. Programma paredzēta vienkāršai ikdienas finanšu uzskaitei (piem., “ēdiens”, “transports”, “abonementi”).

Programma ir domāta ikvienam, kas vēlas vienkāršā veidā sekot līdzi saviem tēriņiem bez sarežģītām grāmatvedības sistēmām.

## B. Datu struktūra

### Izdevuma ieraksta piemērs

{
    "date": "2026-03-09",
    "category": "Pārtika",
    "amount": 15.50,
    "note": "Veikals Rimi"
}

Saraksts ar vārdnīcām (list[dict]) ir ērts, jo izdevumi ir secīgi ieraksti (notikumi laikā), un tos vienkārši pievienot ar append().
Lauki ir skaidri un minimāli:
date kā teksts ISO formātā (YYYY-MM-DD) ir viegli salīdzināms un filtrējams.
category ļauj grupēt izdevumus.
amount ir skaitlis aprēķiniem (summa, kopsavilkumi).
note ir brīvs paskaidrojums (nav obligāts).


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