# Beslutslogg

Nyast överst. Varje beslut: vad, varför, och vad det påverkar.

## 2026-11-23

- **Salthalt visas i procent.** SMHI mäter i PSU, som i praktiken är promille, så sidan visar PSU / 10 med två decimaler. Procent är lättare att förstå för den som inte är oceanograf. Kortet förklarar omräkningen, och källangivelsen säger att salthalten är omräknad. Datafilerna behåller PSU.
- **Näringsämnen visas som årsstatus under Vitala värden och påverkar inte hälsobetyget.** Källa SHARK (CC0), station Klagshamn, treårsmedel bedömt enligt HaV för kusttyp 7, så som myndigheten själv bedömer. Varför inget betyg i helheten: näringsämnen verkar över år, och senaste data är från 2023 eftersom SHARK ligger ett till två år efter. Hämtas för hand en gång per år, inte varje timme. Typ 7 valdes för att SHARK placerar Klagshamn där. Klorofyll från samma prov bedöms för sig. Egen tolkning: sammanvägningen använder normaliserat EK (bilaga 4, formel 1), eftersom föreskriften inte definierar Nklass för kustvatten.
- **Vitala värden har valbar period: dygn, vecka, månad, år.** Dygn visar senaste timvärdet och bedömer dagens dygnsmedel. Vecka, månad och år visar snitt, lägsta och högsta av hela dygn, och räknar hur många dygn som låg utanför det normala för sitt datum (syre: sämsta status och hur många dygn den gällde). Att räkna dygn säger mer än att jämföra ett snitt med ett spann, och ett årssnitt har inget normalspann. Det pågående dygnet räknas inte i perioderna. `current.json` innehåller därför 366 dygn. Hälsobetygen påverkas inte av perioden. I dygnsvyn ritas timvärdena mot dagens normalspann, som bygger på dygnsmedel. Timvärden svänger mer än dygnsmedel, så att en enskild timme hamnar utanför bandet betyder mindre. Sidan säger det i texten.
- **Bara värme som håller i sig ger temperaturvarning.** Ersätter "Utanför p10 till p90 ger Avvikande" från 2026-11-22. Nu ges "För varm" först när dygnsmedlet legat över p90 tre hela dygn i rad, och kallare än normalt ger aldrig varning. Varför: värme är det som stressar sundet (mindre löst syre, snabbare nedbrytning, starkare skiktning, algblomning), medan kyla på hösten mest är väder (princip 1). Med p10 till p90 hamnar ungefär var femte dag utanför spannet, så ett enda dygn gav för många falska varningar: av de senaste 90 dagarna låg temperaturen under spannet 10 dagar och över 1. Tre dygn i rad liknar hur marina värmeböljor brukar definieras (flera dagar över en hög percentil), men gränsen är vår egen och inte en myndighets. Bara hela dygn räknas, det pågående dygnet visas men bedöms inte. Påverkar helhetsbetyget.
- **Drift: GitHub Actions hämtar, Vercel visar.** Vercels gratisplan tillåter bara schemalagda jobb en gång per dygn. Därför kör GitHub Actions `scripts/fetch_smhi.py` varje timme och laddar upp `current.json` till Vercel Blob. Sajten i `app/` är statisk och läser bara den filen. Besökare frågar aldrig SMHI.
- **Arkivet hämtas en gång per dygn.** Normalspann och de senaste 370 dygnens timvärden sparas i `base.json` och cachas i Actions. Varje timme hämtas bara senaste dygnet (sju små anrop). Följer SMHI:s villkor om onödiga nedladdningar.
- **Inget betyg på gamla data.** Är senaste mätningen äldre än 6 timmar visar sidan inget hälso- eller flödesbetyg, bara ett meddelande. SMHI:s senaste värde ligger normalt cirka 2 timmar efter, och hämtning varje timme plus cache lägger till upp till 1,5 timme, så 6 timmar ger marginal utan att visa gamla data som aktuella. SMHI:s villkor säger att inaktuella data inte ska spridas.
- **Dagens dygn betygsätts trots att det pågår**, men märks med antal mätningar hittills.
- **Syre får inget normalspann**, bara de fasta gränserna. Två basår räcker inte.
- **Inget viktat index (0 till 100).** Prövat och avfärdat. Ett viktat snitt låter bra delvärden dölja syrebrist (princip 3), vikterna saknar stöd hos någon myndighet (princip 2), och förslagen gav betyg åt ström, vågor och trafik (princip 1). Helhetsbetyget förblir det sämsta delbetyget.

## 2026-11-22

- **Badvatten stryks.** Proverna tas bara under badsäsongen och publiceras ungefär en vecka efter provtagning, så de säger inget om hur sundet mår just nu.
- **Prototypen är en ögonblicksbild.** Hämtad via webbläsaren eftersom artefaktsidor inte får anropa externa API:er. Får inte publiceras skarpt så här, SMHI:s villkor säger att inaktuella data inte ska spridas.
- **Arkitektur: server hämtar, sajten läser.** Ett schemalagt jobb hämtar från SMHI en gång i timmen och cachar. Följer SMHI:s villkor om att inte hämta samma data upprepade gånger.
- **Källangivelsen ska säga att datat är bearbetat** (dygnsmedel, normalspann, syre i mg/l). Krav enligt CC BY.
- **Hälsa och rörelse hålls isär.** Bara syre och temperatur betygsätts. Vattenstånd, salthalt, ström och flöde beskrivs.
- **Helhetsbetyget är det sämsta delbetyget**, samma princip som vattendirektivet och HELCOM använder.
- **Syre bedöms mot fasta gränser**, 6, 4 och 2 mg/l (HaV:s klassning av syrebrist i kustvatten), eftersom SMHI:s syremätningar bara finns sedan 2024.
- **Temperatur bedöms mot normalt för årstiden.** Utanför p10 till p90 ger "Avvikande".
- **Flödesriktning räknas från vattenstånd**, Skanör minus Viken. Positivt betyder flöde norrut. Strömmätarens riktning används inte, eftersom det är oklart om SMHI anger "från" eller "mot".
- **Stationer:** Flinten 7 bottensystem (temperatur, salthalt, 8 m), Flinten 16 (syre 8 m, ström ytskiktet), Klagshamn, Skanör, Viken (vattenstånd).
- **Basår för normalt:** temperatur och salthalt 2017 till 2025, ström 2009 till 2025, vattenstånd 1996 till 2025.

## Öppna frågor

- Tre dygn i rad över p90 är vår egen gräns för temperaturvarning. Kontrollera om HaV, HELCOM eller SMHI har en definition av marin värmebölja för svenska kustvatten som kan lånas i stället.
- **Klorofyll från Copernicus Marine** (undersökt 2026-11-23, inget byggt).
  - Värdet just nu: `OCEANCOLOUR_BAL_BGC_L3_NRT_009_131` (DOI 10.48670/moi-00294). Dagligen, cirka 1 dygn efter, 300 m, Sentinel-3 OLCI. Sparar bara senaste veckorna.
  - Normalspann: `OCEANCOLOUR_BAL_BGC_L3_MY_009_133` (DOI 10.48670/moi-00296), dagligen sedan 1997. Använd OLCI-varianten för att matcha dagsprodukten, exakt ID ej kontrollerat.
  - Valdes bort: `009_202` (Sentinel-2, bara 20 km kustzon, fler molnluckor) och `009_208` (cirka 50 dygn efter).
  - Satellitvärdet gäller ytan, inte botten på 8 m. Mulna dagar ger inget värde, hur ofta över Öresund är okänt. Båda ska sägas på sidan.
  - Kräver konto (gratis, registrering på data.marine.copernicus.eu/register). Inloggningen läggs som `COPERNICUSMARINE_SERVICE_USERNAME` och `COPERNICUSMARINE_SERVICE_PASSWORD` i GitHub Actions. Hämtas med Python-paketet `copernicusmarine` i ett eget skript, så att `fetch_smhi.py` kan behålla bara standardbiblioteket.
  - Källangivelse enligt Copernicus: "Generated using E.U. Copernicus Marine Service Information" plus DOI-länkarna. Licensavtalet går före hjälpsidorna och är inte läst.
  - Bedömning: HaV:s klassning av klorofyll bygger på sommarmedel över flera år från provtagning, inte på enskilda dygn. Ett dagsbetyg mot de gränserna vore att hitta på vetenskap (princip 2). Förslag: beskriv dagens värde mot eget normalspann utan betyg, som salthalt. Ett årligt betyg på sommarmedlet kan läggas till när gränserna är kontrollerade.
- **HaV:s gränser för klorofyll och näringsämnen i Öresund** (läst ur HVMFS 2019:25, bilaga 4 tabell 3.4 och bilaga 5 tabell 2.2 till 2.7, 2026-11-23). Vilken kusttyp som gäller vid Flinten är oklart: SHARK placerar Klagshamn i typ 7, Skånes kustvatten (vattenförekomsten S Öresunds kustvatten), typ 6 är Öresunds kustvatten. Kontrollera Flintens läge i VISS.
  - Gränserna gäller medelvärden över minst tre år från månadsvis provtagning i ytvattnet (0 till 10 m), inte enskilda prov. Näringsämnen bedöms på vinter (dec till mars för typ 6, dec till feb för typ 7) och sommar (juni till aug för typ 6, juli till aug för typ 7). Klorofyll på sommarhalter.
  - EK = referensvärde delat med uppmätt värde. Referensvärdet beror på salthalten.
  - God/Måttlig i µmol/l vid salthalt 15 (typ 6 / typ 7): totalkväve vinter 22,1 / 20,2, DIN vinter 3,4 / 3,4, totalfosfor vinter 0,80 / 0,72, DIP vinter 0,51 / 0,40, totalkväve sommar 17,2 / 19,5, totalfosfor sommar 0,49 / 0,40. Klorofyll sommar 1,59 / 1,94 µg/l.
  - Osäkert: tabell 3.4 markerar med grått vilka typer som ska salthaltskorrigeras för klorofyll. Färgen syns inte i textutdraget.
  - Slutsats: passar som årsstatus, inte som läget nu.
- Alger (cyanobakterier): SMHI:s Algsituationen ger expertkartor från satellit dagligen under sommaren, inga mätvärden. Passar som säsongsinformation.
- Näringsämnen och klorofyll från vattenprov: SHARK (`shark.smhi.se/api`, CC0). Provtagning ungefär månadsvis, men data för Öresund finns bara till och med 2023 (kontrollerat 2026-11-23). Passar som årsstatus mot HaV:s gränser eller lång trend, inte som läget nu. Närmaste station: ÖVF 5:2 Klagshamn.
- Längre syrehistorik från SHARK för ett bättre normalspann.
- Skiktning, skillnaden mellan ytsalt och bottensalt, som beskriven parameter utan betyg. Kan förklara varför syret sjunker vid botten. Kräver en ytmätning av salthalt vid Flinten eller en närliggande station, inte kontrollerat än.
- Danska sidan via DMI (kräver API-nyckel; deras vattentemperatur mäts i hamnar och är inte standardiserad).
- Expertgranskning av tolkningen, till exempel SMHI:s oceanografer, DTU Aqua eller Öresundsvattensamarbetet.
- Fisk och biologisk mångfald: årsdata, passar som långsiktig trend snarare än levande värde. Källor: SLU:s kustfiskövervakning vid Barsebäck (sedan 1999), DTU Aqua för danska sidan.
