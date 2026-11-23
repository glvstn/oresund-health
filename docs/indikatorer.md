# Indikatorer

## Hälsa (betygsätts)

| Del | Mått | Bedömning |
|---|---|---|
| Andning | Syrehalt vid botten, mg/l (SMHI ml/l x 1,429) | 6 eller mer: God. 4 till 6: Ansträngd. 2 till 4: Syrebrist. Under 2: Akut syrebrist |
| Temperatur | Dygnsmedel vid botten mot normalt, hela dygn | Över p90 tre dygn i rad: För varm. Annars: Normal. Kallare än normalt ger ingen varning |
| Helhet | Sämsta delbetyget | Mår bra, Lite ansträngd, Mår dåligt, Mår mycket dåligt |

## Rörelse (beskrivs)

| Mått | Beskrivning |
|---|---|
| Vattenstånd Klagshamn | Lågvatten, normalt eller högvatten mot normalspannet |
| Salthalt vid botten | Över normalt betyder att salt Kattegattvatten trängt in, under normalt Östersjövatten |
| Strömhastighet | Lugnare, normal eller kraftigare än normalt |
| Flöde | Skanör minus Viken. Över +5 cm norrut, under -5 cm söderut, däremellan nästan stilla |

## Näringsämnen (årsstatus, påverkar inte helheten)

| Mått | Bedömning |
|---|---|
| Totalkväve, totalfosfor, DIN, DIP vinter (dec till feb) och totalkväve, totalfosfor sommar (juli till aug), Klagshamn 0 till 10 m | Treårsmedel mot HVMFS 2019:25 bilaga 5, kusttyp 7, salthaltsberoende referens. Sammanvägt med normaliserat EK (bilaga 4, formel 1): Hög, God, Måttlig, Otillfredsställande, Dålig |
| Klorofyll sommar (juli till aug), 0,5 m | Treårsmedel mot bilaga 4 tabell 3.4, typ 7. Bedöms för sig |

Värden under rapporteringsgränsen räknas som halva gränsen.

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
