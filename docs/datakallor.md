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

## SHARK, SMHI:s havsarkiv (används för näringsämnen)

- Näringsämnen och klorofyll vid ÖVF 5:2 Klagshamn (55,513 N, 12,881 E, 7 m djup). Provtas varje månad på 0,5 och cirka 5,5 m av NIRAS på uppdrag av Öresunds vattenvårdsförbund (kontrollprogram 2021).
- Licens: CC0. SHARK vill att man anger att datat laddats ner från SMHI:s nationella oceanografiska datacentrum och samlats in inom svensk samordnad havsövervakning av beställaren eller utföraren.
- REST-API på `shark.smhi.se/api` (dokumentation `/api/docs/`). Gamla `sharkdata.smhi.se` finns inte längre. Ett anrop tar ungefär en minut.
- Fördröjning: data lämnas till SMHI först när förbundet har godkänt årsrapporten (senast 30 april året efter). Kontrollerat 2026-11-23: Öresund finns till och med 2023, nationellt finns 9 dataset för 2024 och inga för 2025 och 2026.
- Hämtas för hand med `npm run naring` ungefär en gång per år, resultatet `app/naring.json` checkas in.
- Förbundets månadsrapporter (oresunds-vvf.se) kommer en månad efter provtagning men innehåller bara text, inga värden, och har ingen angiven licens. Frågat om tillstånd och tabeller (utkast till mejl 2026-11-23).

## Kandidater

### DMI, danska oceanografiska observationer
- Vattenstånd och vattentemperatur var 10:e minut. OGC API, kräver gratis API-nyckel.
- Licens: CC BY 4.0, kommersiellt tillåtet. Källa: DMI.

### Copernicus Marine
- Klorofyll från satellit, biogeokemiska modeller (syre, näring, pH, siktdjup) för Östersjön.
- Fritt för alla syften, kräver konto.
- Källangivelse för egna produkter: "Generated using E.U. Copernicus Marine Service Information".

### HELCOM, oljeutsläpp från flygövervakning
- Undersökt 2026-11-23, inget byggt.
- HELCOM Map and Data Service, lager "Detected spills of mineral oil and other substances": `maps.helcom.fi/arcgis/rest/services/MADS/Shipping/MapServer/323`. ArcGIS REST, ingen nyckel, frågbart på yta.
- Fält: datum, land, position, kategori (olja och annat), uppskattad volym, utsträckning, vind.
- Inom 12,4 till 13,1 E, 55,3 till 56,2 N: 162 utsläpp 1998 till 2025 (122 svenska, 40 danska observationer). 1 till 15 per år, de senaste åren 1 till 8. Nästan alla under 1 m³. Rutan tar med lite av Köge bukt och Kattegatt.
- Uppdateras årsvis, 2025 finns redan. Inte läget nu.
- Antalet beror på hur mycket som flygs, flygtimmarna har minskat enligt HELCOM. Färre fynd behöver inte betyda färre utsläpp.
- Licens: HELCOM anger CC BY för MADS men varnar för att vissa lager kommer från andra källor. Lagrets eget metadata är inte läst. Källangivelse enligt HELCOM: "[Datamängd], [år]. HELCOM Map and Data Service. https://maps.helcom.fi".
- Bedömning: tryck, inte tillstånd. Passar som årsvis bakgrund ("X observerade utsläpp i fjol"), utan betyg.

### HELCOM, undervattensbuller
- Undersökt 2026-11-23, inget byggt.
- Indikatorn för kontinuerligt buller (fartygsbuller) är bara "pre-core". HELCOM har inte antagit några gränsvärden. EU:s TG-Noise har föreslagit gränser, men de är rekommendationer och inte anpassade till Östersjön.
- Data: modellerade årsvärden från 2018 (HOLAS 3) i MADS, lagren "Input of continuous anthropogenic sound" och "Potential effect of continuous noise to mobile species" under `MADS/Pressures`. Mätdata i ICES Continuous Noise Database. Danska DCE har en rapport (TR204) för danska farvatten 2019 till 2020.
- Bedömning: inget att visa löpande och inga gränser att låna (princip 2). Avvakta HOLAS 4.

### HELCOM, AIS-trafik
- Samma tjänst har årliga täthetskartor per fartygstyp 2006 till 2024.
- Passager över linjer (`MADS/Shipping/MapServer/0`, undersökt 2026-11-23): 14 linjer i Östersjön, en i Öresund. Den heter "Drogden" men går Stevns till Falsterbo (12,42 till 12,85 E, cirka 55,4 N), alltså södra infarten. Fångar genomfart, inte färjorna Helsingör till Helsingborg.
  - Per år och typ (last, passagerare, tank, övrigt, totalt) 2006 till 2020. Inte uppdaterat sedan dess.
  - Totalt 33 099 (2006), botten 23 613 (2010), sedan 26 000 till 29 400 per år. 2020: 28 377, varav 15 502 last och 4 761 tank.
  - Svackan 2009 till 2010 följer finanskrisen. Siffran speglar ekonomin, inte havet.
  - Bedömning: bakgrund ("cirka 28 000 fartyg passerar södra infarten per år"), inget betyg och inget levande värde.

## Avförda

- **HaV badvatten:** säsongsdata med en veckas fördröjning. Licensen för själva datat är dessutom oklar (API-avtalet hänvisar till villkor på HaV:s webbplats).
