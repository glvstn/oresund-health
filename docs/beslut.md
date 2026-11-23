# Beslutslogg

Nyast överst. Varje beslut: vad, varför, och vad det påverkar.

## 2026-11-23

- **Drift: GitHub Actions hämtar, Vercel visar.** Vercels gratisplan tillåter bara schemalagda jobb en gång per dygn. Därför kör GitHub Actions `scripts/fetch_smhi.py` varje timme och laddar upp `current.json` till Vercel Blob. Sajten i `app/` är statisk och läser bara den filen. Besökare frågar aldrig SMHI.
- **Arkivet hämtas en gång per dygn.** Normalspann och de senaste 100 dygnens timvärden sparas i `base.json` och cachas i Actions. Varje timme hämtas bara senaste dygnet (sju små anrop). Följer SMHI:s villkor om onödiga nedladdningar.
- **Inget betyg på gamla data.** Är senaste mätningen äldre än 3 timmar visar sidan inget hälso- eller flödesbetyg, bara ett meddelande. SMHI:s villkor säger att inaktuella data inte ska spridas.
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

- Klorofyll och alger från Copernicus Marine (kräver konto, satellitdata med molnluckor, troligen veckovärde).
- Längre syrehistorik från SHARK för ett bättre normalspann.
- Skiktning, skillnaden mellan ytsalt och bottensalt, som beskriven parameter utan betyg. Kan förklara varför syret sjunker vid botten. Kräver en ytmätning av salthalt vid Flinten eller en närliggande station, inte kontrollerat än.
- Danska sidan via DMI (kräver API-nyckel; deras vattentemperatur mäts i hamnar och är inte standardiserad).
- Expertgranskning av tolkningen, till exempel SMHI:s oceanografer, DTU Aqua eller Öresundsvattensamarbetet.
- Fisk och biologisk mångfald: årsdata, passar som långsiktig trend snarare än levande värde.
