# Instruktioner för Claude

## Principer som inte ändras utan beslut i docs/beslut.md

1. **Hälsa och rörelse hålls isär.** Bara parametrar som säger något om ekologisk hälsa får betyg. Högvatten, salt inflöde och stark ström är väder, inte sjukdom. Påverkan, det människor gör mot sundet, beskrivs men betygsätts inte.
2. **Hitta inte på vetenskapen.** Gränser och klassningar lånas från myndigheter (HaV, HELCOM, vattendirektivet). Där sådana saknas jämförs mot historiken.
3. **Det sämsta delvärdet styr helheten.** Inga medelvärden som döljer problem.
4. **Normalt = p10 till p90** av dygnsmedel inom +-7 dagar från samma datum under basåren.
5. **Ärlig om osäkerhet.** Kort historik, luckor och ogranskade tolkningar sägs ut på sidan.
6. **Källangivelse på sidan**, med att datat är bearbetat.
7. **Respektera källornas villkor.** Hämta från SMHI högst en gång i timmen via en server och cacha. Besökares webbläsare frågar aldrig SMHI direkt.

## När du ändrar något

- Lägg till en rad i `docs/beslut.md` om en princip, gräns eller källa ändras.
- Uppdatera `docs/datakallor.md` om en källa läggs till eller tas bort.
- Kör `scripts/fetch_smhi.py` och kontrollera att utdata ser rimlig ut innan du drar slutsatser om läget.
