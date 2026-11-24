"""Hämtar observerade oljeutsläpp i Öresund från HELCOM:s flygövervakning och räknar dem per år.

    python3 scripts/fetch_helcom_oil.py     # -> app/olja.json (npm run olja)

HELCOM uppdaterar lagret en gång per år, så skriptet körs för hand ungefär en gång per år och
app/olja.json checkas in, som näringsämnena. Se docs/datakallor.md.

Rutan 12,5 till 13,0 E, 55,35 till 56,1 N täcker sundet från Falsterbo till Helsingborg, utan Köge bukt
och utan större delen av Kattegatt. Antalet beror på hur mycket som flygs: färre fynd behöver inte betyda
färre utsläpp. Volymen är HELCOM:s uppskattning från flyget.

Bara standardbiblioteket. Data: Detected spills of mineral oil and other substances, HELCOM Map and Data Service.
"""
import json
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

LAYER = "https://maps.helcom.fi/arcgis/rest/services/MADS/Shipping/MapServer/323/query"
BOX = (12.5, 55.35, 13.0, 56.1)  # väst, syd, öst, nord
FIRST_YEAR = 1998
OUT = Path(__file__).resolve().parent.parent / "app" / "olja.json"


def fetch():
    rows, offset = [], 0
    while True:
        q = urllib.parse.urlencode({
            "where": "1=1", "geometry": ",".join(map(str, BOX)), "geometryType": "esriGeometryEnvelope",
            "inSR": 4326, "spatialRel": "esriSpatialRelIntersects",
            "outFields": "Year,Date,Country,Spill_cat,EstimVol_m", "returnGeometry": "false",
            "resultOffset": offset, "resultRecordCount": 1000, "f": "json",
        })
        req = urllib.request.Request(f"{LAYER}?{q}", headers={"User-Agent": "hur-mar-oresund/0.2"})
        with urllib.request.urlopen(req, timeout=120) as r:
            d = json.load(r)
        if "error" in d:
            raise SystemExit(f"HELCOM svarade med fel: {d['error']}")
        rows += [f["attributes"] for f in d["features"]]
        if not d.get("exceededTransferLimit"):
            return rows
        offset += len(d["features"])


def main():
    rows = fetch()
    last = max(r["Year"] for r in rows)
    years = {y: {"year": y, "count": 0, "oil": 0, "volume": 0.0} for y in range(FIRST_YEAR, last + 1)}
    countries = defaultdict(int)
    for r in rows:
        y = years.get(r["Year"])
        if not y:
            continue
        y["count"] += 1
        y["oil"] += r["Spill_cat"] == "Oil"
        y["volume"] += max(r["EstimVol_m"] or 0, 0)
        countries[r["Country"]] += 1
    for y in years.values():
        y["volume"] = round(y["volume"], 2)
    out = {
        "source": "Detected spills of mineral oil and other substances, HELCOM Map and Data Service, bearbetat till antal och volym per år inom Öresund.",
        "fetched": datetime.now(timezone.utc).date().isoformat(),
        "box": BOX, "total": len(rows), "countries": dict(countries),
        "largest": round(max(max(r["EstimVol_m"] or 0, 0) for r in rows), 1),
        "years": list(years.values()),
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    recent = [y["count"] for y in years.values()][-5:]
    print(f"Klart: {len(rows)} utsläpp {FIRST_YEAR} till {last}, senaste fem åren {recent}, största {out['largest']} m³")


if __name__ == "__main__":
    main()
