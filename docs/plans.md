# Plāns: Izdevumu pārvaldnieks (CLI + JSON)

## A. Programmas apraksts (2–3 teikumi)

Programma ir komandrindas rīks, kas ļauj lietotājam pievienot, apskatīt un analizēt personīgos izdevumus. Tā glabā datus JSON failā, lai izdevumi saglabātos starp palaišanām. Programma paredzēta vienkāršai ikdienas finanšu uzskaitei (piem., “ēdiens”, “transports”, “abonementi”).

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


