# Indikatorer

## Hälsa (betygsätts)

| Del | Mått | Bedömning |
|---|---|---|
| Andning | Syrehalt vid botten, mg/l (SMHI ml/l x 1,429) | 6 eller mer: God. 4 till 6: Ansträngd. 2 till 4: Syrebrist. Under 2: Akut syrebrist |
| Temperatur | Dygnsmedel vid botten mot normalt, hela dygn | Över p90 tre dygn i rad: För varm. Annars: Normal. Kallare än normalt ger ingen varning |
| Helhet | Sämsta delbetyget | Mår bra, Lite ansträngd, Mår dåligt, Mår mycket dåligt |

## Vitala värden utan betyg (beskrivs mot normalt)

| Mått | Beskrivning |
|---|---|
| Salthalt vid botten | Över normalt betyder att salt Kattegattvatten trängt in, under normalt Östersjövatten. Ingen myndighetsgräns, och salt inflöde är väder (princip 1) |
| Klarhet vid ytan, satellit | Djupet där ljuset halverats, ln 2 / KD490, median över samma ruta som klorofyll, molnfria dygn mars till oktober. Grumligare, normalt eller klarare än normalt. Inte siktdjup |
| Klorofyll vid ytan, satellit | Median över en ruta kring Flinten, molnfria dygn mars till oktober. Mindre, normalt eller mer alger än normalt. Satelliten visar högre värden än vattenproven, så ingen jämförelse med HaV:s gränser |

## Rörelse (beskrivs)

| Mått | Beskrivning |
|---|---|
| Vattenstånd Klagshamn | Lågvatten, normalt eller högvatten mot normalspannet |
| Strömhastighet | Lugnare, normal eller kraftigare än normalt |
| Flöde | Skanör minus Viken. Över +5 cm norrut, under -5 cm söderut, däremellan nästan stilla |
| Vind vid Drogden fyr | Styrka enligt SMHI:s vindskala (svag, måttlig, frisk, hård, storm, orkan) och riktning varifrån det blåser. Förklarar strömmen, inget betyg |
| Prognos för flödet | DMI:s havsmodell, Skanör minus Viken per timme fem dygn framåt. Per dygn: norrut eller söderut efter medianen, osäkert under 10 cm, växlar om minst en fjärdedel av timmarna går åt vardera hållet |

## Näringsämnen (årsstatus, påverkar inte helheten)

| Mått | Bedömning |
|---|---|
| Totalkväve, totalfosfor, DIN, DIP vinter (dec till feb) och totalkväve, totalfosfor sommar (juli till aug), Klagshamn 0 till 10 m | Treårsmedel mot HVMFS 2019:25 bilaga 5, kusttyp 7, salthaltsberoende referens. Sammanvägt med normaliserat EK (bilaga 4, formel 1): Hög, God, Måttlig, Otillfredsställande, Dålig |
| Klorofyll sommar (juli till aug), 0,5 m | Treårsmedel mot bilaga 4 tabell 3.4, typ 7. Bedöms för sig |

Värden under rapporteringsgränsen räknas som halva gränsen.

## Påverkan (beskrivs, betygsätts aldrig)

| Mått | Beskrivning |
|---|---|
| Oljeutsläpp | Observerade av flygövervakningen inom Öresund per år, HELCOM 1998 till senaste år. Senaste årets antal och spannet de senaste tio åren. Ingen jämförelse mot normalt |
| Sjöfart | Fartyg per år som passerar Öresunds södra infart (Stevns till Falsterbo), HELCOM 2006 till 2020. Andel per fartygstyp och ungefär antal per dag. Statiskt, ingen jämförelse mot normalt |

## Hur normalt räknas

1. Dygnsmedel per dag från timvärden.
2. För varje dag på året: alla dygnsmedel inom +-7 dagar från samma datum under basåren.
3. Normalspann = p10 till p90 av dessa. Normalvärde = medel.

Varje timme räknas en gång. Överlappar arkivet och senaste dygnet går SMHI:s granskade arkivvärde före. Pågående dygn markeras som ofullständigt (`partial`), med antal mätningar (`n`). 29 februari jämförs som 28 februari.

Basår: temperatur och salthalt 2017 till 2025, ström 2009 till 2025, vattenstånd 1996 till 2025 (30 år, så landhöjning och havsnivåhöjning inte snedvrider för mycket), syre 2024 till 2025 (för kort, därför fasta gränser).

## Kandidater

- Klorofyll och siktdjup (Klarhet), Copernicus eller SHARK.
- Näringsämnen, kväve och fosfor, SHARK.
- Biologi: fisk, tumlare, ålgräs, som årstrend.
