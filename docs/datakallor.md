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
- Vattenstånd och vattentemperatur var 10:e minut. OGC API, ingen nyckel sedan 2 december 2025.
- Vind används sedan 2026-11-24 (`scripts/fetch_dmi.py vind`): väderstationen 06183 Drogden fyr, `opendataapi.dmi.dk/v2/metObs`, parametrarna `wind_speed` och `wind_dir` (tiominutersmedel, riktning varifrån det blåser). Hämtas varje timme, en mätning per hel timme sparas.
- Licens: CC BY 4.0, kommersiellt tillåtet. Källa: DMI.

### DMI, prognos från havsmodellen DKSS
- Undersökt 2026-11-24, används för prognosen i Ström-kortet (`scripts/fetch_dmi.py`).
- `opendataapi.dmi.dk/v1/forecastedr`, OGC EDR. Svarade utan API-nyckel 2026-11-24. Samlingen `dkss_idw` (inre danska farvatten) täcker Öresund. Fråga per punkt: `/collections/dkss_idw/position?coords=POINT(lon lat)&parameter-name=...&crs=crs84&f=GeoJSON`.
- Timvärden cirka fem dygn framåt: vattenstånd (`sea-mean-deviation`, m), ström (`current-u`, `current-v` i m/s, öst och nord, plus per djup), salthalt, vattentemperatur per djup, vind (`wind-u`, `wind-v`).
- Modellens punkt vid Viken (12,5792 E) ligger på land, 12,56 E 56,14 N fungerar.
- Jämfört med SMHI 2026-11-24 00 till 06 UTC: lutningen Skanör minus Viken var 49 till 62 cm i modellen mot 61 till 71 cm uppmätt, alltså samma riktning och cirka 8 cm lägre. Skanör ligger cirka 10 cm lägre i modellen, troligen delvis olika nollnivå. Strömmen vid Flinten 16 gick mot nordost (51 grader) i modellen men var 80 till 98 cm/s mot 22 till 41 cm/s uppmätt, så modellens fart går inte att visa som Flintens.
- Licens: CC BY 4.0 enligt DMI:s villkor (läst 2026-11-24), som gäller data från DMI:s API:er. Prognoser nämns inte uttryckligen men levereras via samma API. Ange källa, länk till licensen och att datat är bearbetat, utan att antyda att DMI står bakom sidan.
- Ingen API-nyckel sedan 2 december 2025. DMI kan strypa vid missbruk och ber om cache och att följa modellens uppdateringstakt. Svarade 429 efter ett tiotal anrop på några minuter vid testerna 2026-11-24.
- Modellen körs 00, 06, 12 och 18 UTC, klar cirka 3 timmar 20 minuter efter start. Workflowen hämtar en gång per körning.
- Bedömning: passar som prognos för strömmens riktning (lutningens tecken och storlek), inte för fart. Ingen betygsättning.

### Copernicus Marine
- Klorofyll från satellit, biogeokemiska modeller (syre, näring, pH, siktdjup) för Östersjön.
- Fritt för alla syften, även kommersiellt, kräver konto. Licensen läst 2026-11-24, se docs/beslut.md.
- Källangivelse för egna produkter: "Generated using E.U. Copernicus Marine Service Information".
- Används för klarhet (KD490) sedan 2026-11-24, samma produkter, dataset `cmems_obs-oc_bal_bgc-transp_my_l3-olci-300m_P1D` och `cmems_obs-oc_bal_bgc-transp_nrt_l3-olci-300m_P1D`. Visas som djupet där ljuset halverats, ln 2 / KD490.
- Används för klorofyll vid ytan (`scripts/fetch_copernicus.py`): `OCEANCOLOUR_BAL_BGC_L3_NRT_009_131` (DOI 10.48670/moi-00294) för senaste dygnen och `OCEANCOLOUR_BAL_BGC_L3_MY_009_133` (DOI 10.48670/moi-00296) för normalspannet, båda Sentinel-3 OLCI 300 m. Inloggning i GitHub Actions via `COPERNICUSMARINE_SERVICE_USERNAME` och `COPERNICUSMARINE_SERVICE_PASSWORD`.

### HELCOM, oljeutsläpp från flygövervakning
- Undersökt 2026-11-23. Används sedan 2026-11-24 för kortet Oljeutsläpp (`scripts/fetch_helcom_oil.py`, körs för hand en gång per år, resultatet `app/olja.json` checkas in).
- Kortet använder rutan 12,5 till 13,0 E, 55,35 till 56,1 N, alltså sundet utan Köge bukt och större delen av Kattegatt: 120 utsläpp 1998 till 2025 (88 svenska, 32 danska observationer), 0 till 15 per år, största 6,9 m³, 112 olja och 8 okänt.
- HELCOM Map and Data Service, lager "Detected spills of mineral oil and other substances": `maps.helcom.fi/arcgis/rest/services/MADS/Shipping/MapServer/323`. ArcGIS REST, ingen nyckel, frågbart på yta.
- Fält: datum, land, position, kategori (olja och annat), uppskattad volym, utsträckning, vind.
- Inom 12,4 till 13,1 E, 55,3 till 56,2 N: 162 utsläpp 1998 till 2025 (122 svenska, 40 danska observationer). 1 till 15 per år, de senaste åren 1 till 8. Nästan alla under 1 m³. Rutan tar med lite av Köge bukt och Kattegatt.
- Uppdateras årsvis, 2025 finns redan. Inte läget nu.
- Antalet beror på hur mycket som flygs, flygtimmarna har minskat enligt HELCOM. Färre fynd behöver inte betyda färre utsläpp.
- Licens: HELCOM anger CC BY för MADS men varnar för att vissa lager kommer från andra källor. Lagrets metadata (läst 2026-11-24) saknar licenstext. Datat sammanställs av HELCOM själva från ländernas flygövervakning, så MADS-licensen bedöms gälla. Bekräfta med HELCOM om det blir viktigt. Källangivelse enligt HELCOM: "[Datamängd], [år]. HELCOM Map and Data Service. https://maps.helcom.fi".
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

### SLU, KUL (kustfiskdatabasen)
- Undersökt 2026-11-24, inget byggt.
- SLU Aqua är datavärd för kustprovfisken på uppdrag av HaV. Data hämtas via webbrapporter på `aquarapport.slu.se` (fångstdata `default.aspx?ID=5`, individdata `ID=11`), en karttjänst och API:er hos SBDI (biodiversitydata.se). Rapporterna och SBDI är inte prövade, så det är okontrollerat om antal fiskar per redskap och natt (CPUE) per station och år går att få ut direkt.
- Kopia på GBIF (datasetet `1b7e83a0-0c61-11dd-84ce-b8a03c50a862`, CC0): bara förekomster utan antal, ändrad senast 2024 och slutar 2018 i sundet. Inom 12,5 till 13,1 E, 55,3 till 56,1 N finns 21 531 poster 1988 till 2018, bland annat Barsebäck (Barsebäckshamn, Barsebäcksverket, Lundåkrabukten, Tjuvakroken, Sjöbobadet) och Öresund (Lillgrund, SO Bredgrund, Sjollen). Duger inte för trend.
- Licens hos SLU: ingen angiven på KUL-sidan (läst 2026-11-24). Källangivelse enligt SLU: "[yyyy]. Databasen för kustprovfisken – KUL. Uppsala: Institutionen för akvatiska resurser, Sveriges lantbruksuniversitet (SLU). [slu.se/kul]. [yyyy-mm-dd]." Bekräfta villkoren med SLU innan användning, GBIF-kopians CC0 bör gälla även källan men det står inte hos SLU.
- Barsebäck provfiskas med ryssjor i augusti varje år sedan 1999. Sammanfattat i Aqua notes 2023:11, som inte är läst.
- Bedömning: bästa källan för en lokal årstrend för fisk, jämförd mot historiken (princip 2). Nästa steg: pröva fångstrapporten för Barsebäck och fråga SLU (kontakt för KUL: Peter Ljungberg) om licens och om CPUE per år.

### Fiskbarometern (SLU på uppdrag av HaV)
- Undersökt 2026-11-24, inget byggt.
- Årlig resursöversikt över svenska fisk- och skaldjursbestånd, 2025 års bedömningar publicerade i januari till mars 2026. Webbsidor per art och område på fiskbarometern.se, PDF per art. Ingen dokumenterad nedladdning av data eller öppet API. Sidan hämtar data från ett internt API som inte är avsett för andra.
- Licens: "Upphovsrätt av Fiskbarometern. Alla rättigheter förbehållna." Rekommenderad källangivelse: "SLU Fiskbarometern (publiceringsår). Resursöversikt 'årtal för analys'. [https://fiskbarometern.se] [åtkomstdatum]."
- Öresund bedöms inte för sig. Torsken i sundet räknas till västra Östersjöbeståndet (Ices-delområden 22 till 24), där Ices råd för 2026 och 2027 är noll ton. Inget kustfiskbestånd för Öresund hittades i översikten.
- Bedömning: myndighetens klassning finns (princip 2), men den gäller större områden än sundet och får inte återpubliceras fritt. Kan nämnas med länk som sammanhang, inte som betyg för Öresund.

### ICES, fångster och beståndsanalyser
- Undersökt 2026-11-24 bara i förbigående, inget byggt.
- Fångster per delområde (Öresund är 27.3.b.23) är tryck, alltså Påverkan utan betyg (princip 1). Beståndsanalyserna gäller större områden, se Fiskbarometern ovan. Trålfiske är förbjudet i större delen av sundet sedan 1932, vilket gör fångstsiffrorna svårtolkade.

## Avförda

- **SMHI strömprognos, NEMO-Nordic 60 timmar** (2026-11-24): prognos var sjätte timme, skulle kunna säga åt vilket håll vattnet väntas rinna. Realtidsfilerna nås bara via en webbtjänst mot leveransavgift och beställs via kundtjanst@smhi.se (enligt datasetsidan, läst 2026-11-24). Avförd eftersom sidan bara använder fria källor. Kan tas upp igen om SMHI släpper prognosen fritt.
- **HaV badvatten:** säsongsdata med en veckas fördröjning. Licensen för själva datat är dessutom oklar (API-avtalet hänvisar till villkor på HaV:s webbplats).
