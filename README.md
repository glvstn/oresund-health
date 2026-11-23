# Hur mår Öresund

En dashboard som visar hur havet utanför Malmö mår, ungefär som Apple Health om Öresund vore en människa.

## Idén

Havsdata är många parametrar med komplexa värden. Sidan ska göra dem begripliga för någon som inte är oceanograf:

- **Hälsa** får betyg: syre vid botten och temperatur mot normalt för årstiden.
- **Rörelse** beskrivs men betygsätts inte: vattenstånd, salthalt, ström och flödesriktning.
- Varje värde jämförs med vad som är **normalt för samma vecka** under tidigare år.

## Status

- Prototyp som ögonblicksbild, 22 november 2026: https://claude.ai/artifact/NBfdH9skWg3CzdSAwW3qyE
- Sajten finns i `app/`. Den ska driftas på Vercel med data som GitHub Actions hämtar varje timme.

## Mappar

- `docs/beslut.md` beslutslogg
- `docs/datakallor.md` licenser, källangivelse, åtkomst
- `docs/indikatorer.md` parametrar, gränser, hur normalt räknas
- `scripts/fetch_smhi.py` hämtar från SMHI och räknar dygnsmedel och normalspann
- `app/` sajten, en statisk sida som läser `data/current.json`
- `.github/workflows/refresh.yml` hämtar varje timme och laddar upp till Vercel Blob
- `data/` uttag (inte incheckat)

## Kom igång

```
python3 scripts/fetch_smhi.py          # hämtar arkiv och senaste dygnet
cd app && python3 -m http.server 8000  # öppna http://localhost:8000
```

Skriptet använder bara Pythons standardbibliotek. `base` hämtar arkivet och skriver `data/base.json`, `current` hämtar senaste dygnet och skriver `data/current.json`. Utan argument körs båda. `app/data` är en länk till `data/`.

## Drift

1. GitHub Actions kör `scripts/fetch_smhi.py` varje timme. Arkivet hämtas bara första körningen varje dygn och cachas.
2. `data/current.json` laddas upp till Vercel Blob som `oresund/current.json`.
3. Vercel servar `app/` och skickar `/data/current.json` vidare till Blob (se `vercel.json`).
4. Är senaste mätningen äldre än 3 timmar visar sidan inget betyg.

## Källor

Data från SMHI, bearbetat (dygnsmedel, normalspann, syre omräknat till mg/l). Licens CC BY 4.0. Se `docs/datakallor.md`.
