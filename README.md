# Hur mår Öresund

En dashboard som visar hur havet utanför Malmö mår, ungefär som Apple Health om Öresund vore en människa.

## Idén

Havsdata är många parametrar med komplexa värden. Sidan ska göra dem begripliga för någon som inte är oceanograf:

- **Hälsa** får betyg: syre vid botten och temperatur mot normalt för årstiden.
- **Vitala värden** visar temperatur, syre, salthalt och klorofyll över tid. Salthalt och klorofyll jämförs med det normala men betygsätts inte.
- **Rörelse** beskrivs men betygsätts inte: vattenstånd, ström och flödesriktning.
- **Påverkan** beskrivs men betygsätts inte: det människor gör mot sundet, i dag sjöfart.
- Varje värde jämförs med vad som är **normalt för samma vecka** under tidigare år.

## Status

Live: https://oresund-health.vercel.app (Vercel, Hobby). Data hämtas varje timme av GitHub Actions i https://github.com/glvstn/oresund-health, startat av cron-job.org.

## Mappar

- `docs/beslut.md` beslutslogg
- `docs/datakallor.md` licenser, källangivelse, åtkomst
- `docs/indikatorer.md` parametrar, gränser, hur normalt räknas
- `scripts/fetch_smhi.py` hämtar från SMHI och räknar dygnsmedel och normalspann
- `app/` sajten, en statisk sida som läser `data/current.json`
- `.github/workflows/refresh.yml` hämtar och laddar upp till Vercel Blob, startas varje timme av cron-job.org
- `data/` uttag (inte incheckat)

## Kör sidan lokalt

```
npm run dev       # öppna http://localhost:8000
npm run data      # hämta senaste dygnet från SMHI, högst en gång i timmen
npm run data:all  # hämta om arkivet och normalspannet
npm run naring    # hämta näringsämnen från SHARK, en gång per år
```

`npm run dev` skapar länken `app/data` om den saknas och hämtar data om det inte finns någon än. Den hämtar inte ny data varje gång, så starta om servern hur ofta du vill. Ingen `npm install` behövs, projektet har inga beroenden. Själva hämtningen görs av Python 3.

### Samma sak för hand

Det här är vad npm-skripten gör.

1. Hämta data från SMHI. Första gången behövs båda stegen, det tar en stund eftersom hela arkivet hämtas:

   ```
   python3 scripts/fetch_smhi.py
   ```

   Sedan räcker det att hämta senaste dygnet. Gör det högst en gång i timmen, enligt SMHI:s villkor:

   ```
   python3 scripts/fetch_smhi.py current
   ```

2. Länka in datat i sajten. Behövs bara en gång efter kloning, länken är inte incheckad:

   ```
   ln -s ../data app/data
   ```

3. Starta en lokal server och öppna http://localhost:8000:

   ```
   cd app && python3 -m http.server 8000
   ```

   Sidan måste köras via en server. Öppnar du `index.html` direkt som fil kan webbläsaren inte läsa `data/current.json`.

`base` hämtar arkivet och skriver `data/base.json` (normalspann), `current` hämtar senaste dygnet och skriver `data/current.json`. Utan argument körs båda. Är `data/current.json` äldre än 6 timmar visar sidan inget betyg, kör då `current` igen.

## Näringsämnen

Näringsämnen och klorofyll från Klagshamn hämtas från SMHI:s havsarkiv SHARK med `npm run naring` och sparas i `app/naring.json`, som checkas in. Proverna når SHARK ett till två år efter provtagning, så det räcker att köra skriptet när ett nytt år har publicerats, ungefär en gång per år. Kör det, kontrollera utskriften och committa filen. Ett anrop tar ungefär en minut.

## Drift

1. cron-job.org startar workflowen minut 17 varje timme via GitHubs API (`workflow_dispatch`). GitHubs eget schema startade aldrig och används inte. Token för anropet gäller till 2027-11-22 och måste förnyas innan dess.
2. GitHub Actions kör `scripts/fetch_smhi.py`. Arkivet hämtas bara första körningen varje dygn och cachas.
3. `data/current.json` laddas upp till Vercel Blob som `oresund/current.json`.
4. Vercel servar `app/` och skickar `/data/current.json` vidare till Blob (se `vercel.json`).
5. Är senaste mätningen äldre än 6 timmar visar sidan inget betyg.

## Källor

Data från SMHI, bearbetat (dygnsmedel, normalspann, syre omräknat till mg/l). Licens CC BY 4.0. Se `docs/datakallor.md`.
