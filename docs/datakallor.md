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

## HELCOM, AIS-passager (används för sjöfart)

- Lager "AIS passage line crossings by ship type", `maps.helcom.fi/arcgis/rest/services/MADS/Shipping/MapServer/0`, linjen som heter "Drogden" men går Stevns till Falsterbo (södra infarten). Per år och typ (last, passagerare, tank, övrigt, totalt) 2006 till 2020. Uppdateras inte längre.
- Licens enligt metadataposten (`metadata.helcom.fi`, post 4987669b-262e-46ef-8800-3ccfb3b93313): fri att använda med källangivelse, ingen begränsning av allmän åtkomst. Källangivelse enligt HELCOM: "[Datamängd], [år]. HELCOM Map and Data Service. https://maps.helcom.fi".
- Siffrorna ligger statiskt i `app/index.html` (konstanten `SHIPS`). Ingen hämtning.

## Kandidater

### DMI, danska oceanografiska observationer
- Vattenstånd och vattentemperatur var 10:e minut. OGC API, kräver gratis API-nyckel.
- Licens: CC BY 4.0, kommersiellt tillåtet. Källa: DMI.

### Copernicus Marine
- Klorofyll från satellit, biogeokemiska modeller (syre, näring, pH, siktdjup) för Östersjön.
- Fritt för alla syften, även kommersiellt, kräver konto. Licensen läst 2026-11-24, se docs/beslut.md.
- Källangivelse för egna produkter: "Generated using E.U. Copernicus Marine Service Information".
- Används för klorofyll vid ytan (`scripts/fetch_copernicus.py`): `OCEANCOLOUR_BAL_BGC_L3_NRT_009_131` (DOI 10.48670/moi-00294) för senaste dygnen och `OCEANCOLOUR_BAL_BGC_L3_MY_009_133` (DOI 10.48670/moi-00296) för normalspannet, båda Sentinel-3 OLCI 300 m. Inloggning i GitHub Actions via `COPERNICUSMARINE_SERVICE_USERNAME` och `COPERNICUSMARINE_SERVICE_PASSWORD`.

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

### HELCOM, AIS-täthet
- Samma tjänst har årliga täthetskartor per fartygstyp 2006 till 2024. Passagerna används, se ovan.

### Danska Sjöfartsstyrelsen, AIS
- Undersökt 2026-11-23, inget byggt.
- Historisk AIS för danska vatten, gratis som CSV-filer. En zip-fil per dygn på `http://aisdata.ais.dk/` (S3-hink `aisdata.ais.dk.s3.eu-central-1.amazonaws.com`). Kontrollerat 2026-11-23: senaste fil `aisdk-2026-11-20.zip`, publicerad 2026-11-23, alltså cirka tre dygn efter. Äldre år ligger i mappar per år från 2021 (2025-mappen slutar i februari, resten av 2025 och 2026 ligger i roten).
- En dygnsfil är cirka 590 MB och täcker alla danska vatten, så den måste filtreras på Öresund. Hämtas en gång per dygn, inte per timme.
- Villkor: får användas kommersiellt och icke-kommersiellt, men inte så att det ser ut som att myndigheten står bakom. Villkorssidan är inte läst i sin helhet. Kontakten för AIS-data verkar ha flyttat till danska Beredskapsstyrelsen, kontrollera ägaren.
- Den färdiga statistiken över passager genom Öresund slutar 2023 (sidan listar 2015 till 2023) och uppdateras inte längre. Rådatan ovan är aktuell.
- Prövat 2026-11-23: att räkna fartyg i klass A som korsar en linje Dragør till Klagshamn tog cirka 20 s nedladdning och 30 s räkning per dygn och gav 60 fartyg för 2026-11-20. Ett normalspann kräver att minst ett års dygnsfiler räknas igenom (cirka 215 GB). Valdes bort till förmån för HELCOM:s årssiffra. Skriptet togs bort, upplägget finns här om sidan senare ska visa levande trafik.

### EMODnet Human Activities, fartygstäthet
- Undersökt 2026-11-23, inget byggt.
- Månatliga och årliga täthetskartor (GeoTIFF) per fartygstyp 2017 till 2023, plus WCS-tjänst.
- Återanvändning fri, kommersiellt och icke-kommersiellt, om EMODnet Human Activities och CLS anges. Licensfältet i katalogposten är inte kontrollerat.
- Bedömning: visar var trafiken går och hur den varierar över året, inte läget nu.

### Naturvårdsverket, Utsläpp i siffror (Sjölunda)
- Undersökt 2026-11-23, inget byggt.
- Årliga utsläpp per anläggning 2007 till 2023, Sjölunda har id 2664. Nedladdning som Excel eller CSV.
- Licens: ingen angiven för datat (kontrollerat 2026-11-23). Webbplatsens upphovsrättstext gäller bara bilder. Får inte användas förrän Naturvårdsverket bekräftat villkoren (princip 7).
- Bedömning: årsvärde för kväve och fosfor från Malmös största reningsverk, men ligger efter (senast 2023) och licensen är oklar.

### Danmarks Miljøportal, PULS (reningsverk och bräddning)
- Undersökt 2026-11-23, inget byggt.
- Nationell databas över punktutsläpp. Kommunerna rapporterar bräddningar per utlopp en gång per år. Volymerna har ofta varit modellerade, flödesmätare införs.
- Spildevandsvagten.dk visar PULS-utdrag (datamängden `regnbetingede-udloeb-udledning` på arealdata.miljoeportal.dk) och anger CC0. Senaste år 2025. Det är en tredje parts uppgift. Miljøportalens egen villkorssida svarar 404 och ingen licens har hittats hos källan. Bekräfta med Danmarks Miljøportal innan användning.
- Lynetten (BIOFOS) släpper ut i Öresund enligt tillstånd. Rapporteras i PULS.
- Bedömning: årsdata, inte löpande.

### VA SYD, bräddning i Malmö
- Undersökt 2026-11-23. Ingen öppen data hittad.
- Bräddningar rapporteras till Malmö stads miljöförvaltning i efterhand. Större händelser publiceras som nyheter, till exempel avloppsläckan i maj 2026.
- Bräddpunkter bland annat Limhamns hamn och sundet vid Ön och Sege kanal. De flesta bräddningar sker juni till augusti vid kraftigt regn.
- Bedömning: passar som händelse, inte som levande värde. Fråga VA SYD eller miljöförvaltningen om löpande data.

## Avförda

- **HaV badvatten:** säsongsdata med en veckas fördröjning. Licensen för själva datat är dessutom oklar (API-avtalet hänvisar till villkor på HaV:s webbplats).
