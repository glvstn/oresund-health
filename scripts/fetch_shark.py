"""Hämtar näringsämnen och klorofyll för Klagshamn från SMHI:s havsarkiv SHARK och bedömer dem enligt HaV.

Datat kommer till SHARK ett till två år efter provtagning, så skriptet körs för hand ungefär en gång per år
(npm run naring) och resultatet app/naring.json checkas in. Se docs/datakallor.md.

Bedömning enligt HVMFS 2019:25, kusttyp 7 (Skånes kustvatten, där SHARK placerar Klagshamn):
- Näringsämnen (bilaga 5, tabell 2.2 till 2.7): vinter dec till feb (DIN, DIP, tot-N, tot-P) och sommar
  juli till aug (tot-N, tot-P), medel av de tre senaste åren med data, ytvattnet 0 till 10 m.
  Referensvärdet beror på salthalten. EK = referens / uppmätt.
- Sammanvägning: EK normaliseras klassvis linjärt till skalan 0,8 / 0,6 / 0,4 / 0,2 (bilaga 4, formel 1).
  Medel för vinter, medel för sommar, sedan medel av de två.
- Klorofyll (bilaga 4, tabell 3.4): sommar juli till aug, 0,5 m. Bedöms för sig.
Värden under rapporteringsgränsen räknas som halva gränsen.

Bara standardbiblioteket. Data: SMHI, SHARK, insamlat av NIRAS på uppdrag av Öresunds vattenvårdsförbund. CC0.
"""
import json
import statistics
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

API = "https://shark.smhi.se/api/sample/table"
STATION = "ÖVF 5:2 KLAGSHAMN"
YEARS = 3
OUT = Path(__file__).resolve().parent.parent / "app" / "naring.json"

COL = {
    "totN": "Total Nitrogen Tot-N (umol/l)",
    "totP": "Total phosphorus Tot-P (umol/l)",
    "dip": "Phosphate PO4-P (umol/l)",
    "no3": "Nitrate NO3-N (umol/l)",
    "no2": "Nitrite NO2-N (umol/l)",
    "nh4": "Ammonium NH4-N (umol/l)",
    "sal": "Salinity CTD (o/oo psu)",
    "chl": "Chlorophyll-a bottle (ug/l)",
}

# Typ 7: referens som funktion av salthalt (gäller 0 till 7 psu, högre räknas som 7) och EK-gränser HG, GM, MO, OD.
TYPE7 = {
    ("totN", "vinter"): (lambda s: -6.516 * s + 62.6, (0.91, 0.84, 0.67, 0.50)),
    ("din", "vinter"): (lambda s: -6.371 * s + 46.9, (0.80, 0.67, 0.44, 0.29)),
    ("totP", "vinter"): (lambda s: -0.076 * s + 1.03, (0.82, 0.69, 0.47, 0.31)),
    ("dip", "vinter"): (lambda s: -0.007 * s + 0.32, (0.80, 0.67, 0.44, 0.29)),
    ("totN", "sommar"): (lambda s: -2.856 * s + 35.0, (0.86, 0.77, 0.55, 0.38)),
    ("totP", "sommar"): (lambda s: -0.046 * s + 0.62, (0.85, 0.74, 0.53, 0.36)),
    ("chl", "sommar"): (lambda s: 1.3, (0.80, 0.67, 0.35, 0.15)),
}
SAL_MAX = 7.0
CLASSES = ["Hög", "God", "Måttlig", "Otillfredsställande", "Dålig"]
NAMES = {"totN": "Totalkväve", "totP": "Totalfosfor", "din": "Löst oorganiskt kväve", "dip": "Löst oorganiskt fosfor", "chl": "Klorofyll"}
UNITS = {"chl": "µg/l"}


def fetch():
    rows, headers, offset = [], None, 0
    year = date.today().year
    while True:
        body = {
            "params": {"tableView": "sharkdata_physicalchemical_columns", "limit": 500, "offset": offset, "headerLang": "internal_key"},
            "query": {"fromYear": year - 8, "toYear": year, "dataTypes": ["Physical and Chemical"], "stationName": [STATION]},
        }
        req = urllib.request.Request(API, data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json", "User-Agent": "hur-mar-oresund/0.2"})
        with urllib.request.urlopen(req, timeout=300) as r:
            d = json.load(r)
        headers = d["headers"]
        rows += d.get("rows", [])
        if len(d.get("rows", [])) < 500:
            return headers, rows
        offset += 500


def value(row, idx, key):
    """Talvärde, halva gränsen om under rapporteringsgränsen, None om saknas."""
    raw = row[idx[COL[key]]]
    if raw in ("", None):
        return None
    v = float(raw)
    qflag = "QFLAG " + COL[key].split(" (")[0]
    return v / 2 if qflag in idx and row[idx[qflag]] == "<" else v


def samples(headers, rows):
    idx = {h: i for i, h in enumerate(headers)}
    out = []
    for r in rows:
        depth = float(r[idx["sample_depth_m"]])
        if depth > 10:
            continue
        s = {k: value(r, idx, k) for k in COL}
        parts = [s["no3"], s["no2"], s["nh4"]]
        s["din"] = sum(parts) if all(p is not None for p in parts) else None
        s["date"] = r[idx["visit_date"]]
        s["depth"] = depth
        out.append(s)
    return out


def season(d):
    """('vinter', år) för dec till feb, där december räknas till nästa års vinter. ('sommar', år) för juli till aug."""
    y, m = int(d[:4]), int(d[5:7])
    if m == 12:
        return "vinter", y + 1
    if m in (1, 2):
        return "vinter", y
    if m in (7, 8):
        return "sommar", y
    return None, None


def ek_norm(ek, bounds):
    """Klassvis linjär normalisering till 0,8 / 0,6 / 0,4 / 0,2 (HVMFS 2019:25 bilaga 4, formel 1)."""
    ek = min(ek, 1.0)
    edges = [1.0, *bounds, 0.0]          # övre gräns för Hög är 1
    norm = [1.0, 0.8, 0.6, 0.4, 0.2, 0.0]
    for i in range(5):
        hi, lo = edges[i], edges[i + 1]
        if ek >= lo:
            return (ek - lo) / (hi - lo) * 0.2 + norm[i + 1]
    return 0.0


def klass(norm):
    for c, edge in zip(CLASSES, (0.8, 0.6, 0.4, 0.2)):
        if norm >= edge:
            return c
    return CLASSES[-1]


def r2(x):
    return None if x is None else round(x, 2)


def main():
    headers, rows = fetch()
    ss = samples(headers, rows)
    if not ss:
        raise SystemExit("Inga prov hittades för " + STATION)
    have = {}
    for s in ss:
        per, y = season(s["date"])
        if per:
            have.setdefault(y, set()).add(per)
    years = sorted(y for y, p in have.items() if p == {"vinter", "sommar"})[-YEARS:]
    if len(years) < YEARS:
        raise SystemExit(f"Bara {len(years)} år med både vinter och sommar, HaV kräver {YEARS}.")

    params, norms = [], {"vinter": [], "sommar": []}
    for (key, per), (ref, bounds) in TYPE7.items():
        sel = [s for s in ss if season(s["date"]) in [(per, y) for y in years] and s[key] is not None
               and (key != "chl" or s["depth"] <= 1)]
        if not sel:
            continue
        mean = statistics.fmean(s[key] for s in sel)
        sal = statistics.fmean(s["sal"] for s in sel if s["sal"] is not None)
        rv = ref(min(sal, SAL_MAX))
        ek = rv / mean
        n = ek_norm(ek, bounds)
        if key != "chl":
            norms[per].append(n)
        params.append({
            "key": key, "season": per, "name": NAMES[key], "unit": UNITS.get(key, "µmol/l"),
            "value": r2(mean), "samples": len(sel), "salinity": round(sal, 1),
            "reference": r2(rv), "good_moderate": r2(rv / bounds[1]), "ek": r2(ek), "class": klass(n),
        })

    overall = statistics.fmean([statistics.fmean(norms["vinter"]), statistics.fmean(norms["sommar"])])
    out = {
        "station": "Klagshamn (ÖVF 5:2)", "lat": 55.5133, "lon": 12.8808, "type": "7 - Skånes kustvatten",
        "years": [years[0], years[-1]], "latest_sample": max(s["date"] for s in ss),
        "nutrients_class": klass(overall), "nutrients_ek_norm": r2(overall),
        "params": params,
        "source": "SMHI, SHARK. Insamlat av NIRAS på uppdrag av Öresunds vattenvårdsförbund. CC0. Bearbetat enligt HVMFS 2019:25.",
        "fetched": datetime.now(timezone.utc).isoformat(timespec="minutes").replace("+00:00", "Z"),
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
    print(f"Klart: {out['station']} {years[0]}–{years[-1]}, näringsämnen {out['nutrients_class']}, senaste prov {out['latest_sample']}")
    for p in params:
        print(f"  {p['name']} {p['season']}: {p['value']} {p['unit']} (gräns god/måttlig {p['good_moderate']}), {p['class']}")


if __name__ == "__main__":
    main()
