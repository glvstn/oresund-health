# Datakällor

Uppdaterad 2026-11-22. Kontrollera villkoren igen innan sajten publiceras.

## Används

### SMHI, oceanografiska observationer
- API: https://opendata-download-ocobs.smhi.se/api (version 1.0), ingen nyckel.
- Perioder per station: `latest-day` (JSON, senaste dygnet) och `corrected-archive` (CSV, semikolonseparerad, hela historiken). Vissa stationer har även `latest-hour` och `latest-months`.
- Licens: CC BY 4.0 (Erkännande 4.0 SE). Kommersiell användning tillåten.
- Källangivelse: ange SMHI som källa och att materialet är ändrat.
- Villkor för hämtning: bara dokumenterade API:er, inga onödiga nedladdningar, hämta inte samma data upprepade gånger, sprid inte inaktuella data, cacha enligt metadata.
- Villkor: https://www.smhi.se/data/om-smhis-data/villkor-for-anvandning

Parametrar (nyckel): 1 våghöjd, 2 strömriktning, 3 strömhastighet (cm/s), 4 salthalt (PSU), 5 havstemperatur (°C), 6 vattenstånd (cm), 15 syrehalt (ml/l).

| Station | Id | Används för |
|---|---|---|
| Flinten 16 | 35136 | Syre (8 m), ström (djupkod 0) |
| Flinten 7 bottensystem | 33047 | Temperatur och salthalt (8 m) |
| Klagshamn | 2095 | Vattenstånd, sedan 1929 |
| Skanör | 30488 | Vattenstånd, södra infarten |
| Viken | 2228 | Vattenstånd, norra infarten |

Andra aktiva stationer i sundet: Malmö Hamn, Barsebäck, Landskrona Hamn, Helsingborg.

## Kandidater

### SHARK, svensk havsmiljöövervakning (SMHI)
- Syre, näringsämnen, klorofyll, plankton, sälar, tumlare. Provtagning, inte realtid.
- Licens: CC0. REST-API via SHARKdata.

### DMI, danska oceanografiska observationer
- Vattenstånd och vattentemperatur var 10:e minut. OGC API, kräver gratis API-nyckel.
- Licens: CC BY 4.0, kommersiellt tillåtet. Källa: DMI.

### Copernicus Marine
- Klorofyll från satellit, biogeokemiska modeller (syre, näring, pH, siktdjup) för Östersjön.
- Fritt för alla syften, kräver konto.
- Källangivelse för egna produkter: "Generated using E.U. Copernicus Marine Service Information".

## Avförda

- **HaV badvatten:** säsongsdata med en veckas fördröjning. Licensen för själva datat är dessutom oklar (API-avtalet hänvisar till villkor på HaV:s webbplats).
