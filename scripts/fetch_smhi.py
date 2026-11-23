"""Hämtar Öresunds-data från SMHI och räknar dygnsmedel och normalspann.

Två steg, så att det stora arkivet bara hämtas en gång per dygn:

    python3 scripts/fetch_smhi.py base      # arkivet -> data/base.json (normalspann och senaste 100 dygnens timvärden)
    python3 scripts/fetch_smhi.py current   # senaste dygnet + base.json -> data/current.json
    python3 scripts/fetch_smhi.py           # båda

data/current.json innehåller meta, daily (senaste 90 dygnen mot normalt) och hourly (senaste 24 timmarna).
Varje dygnsrad har "n" (antal mätningar) och "partial" (dygnet pågår). Syre saknar normalspann.
Tider är UTC i ISO-format med Z.

Bara standardbiblioteket. Se docs/indikatorer.md för metoden och docs/datakallor.md för villkoren.
Data från SMHI, bearbetat. Licens CC BY 4.0.
"""
import json
import statistics
import sys
import urllib.request
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

API = "https://opendata-download-ocobs.smhi.se/api/version/1.0/parameter/{p}/station/{s}/period/{period}"
OUT = Path(__file__).resolve().parent.parent / "data"
DAYS = 90       # dygn som visas
KEEP = 100      # dygn med timvärden som sparas i base.json, så att senaste dygnet kan slås ihop
WINDOW = 7      # +-dygn kring samma datum för normalspannet

# namn: (parameter, station, djup, basår, skala, rubrik, enhet)
SERIES = {
    "temp":  (5, 33047, "8", (2017, 2025), 1.0, "Temperatur vid botten", "°C"),
    "salt":  (4, 33047, "8", (2017, 2025), 1.0, "Salthalt vid botten", "PSU"),
    "speed": (3, 35136, "0", (2009, 2025), 1.0, "Strömhastighet, ytskiktet", "cm/s"),
    # Syre: för kort historik för normalspann, bedöms mot fasta gränser (docs/beslut.md).
    "oxy":   (15, 35136, "8", None, 1.429, "Syrehalt vid botten", "mg/l"),
    "level": (6, 2095, "0", (1996, 2025), 1.0, "Vattenstånd Klagshamn", "cm"),
}
LEVELS = {"levelS": 30488, "levelV": 2228}  # Skanör (söder), Viken (norr)


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "hur-mar-oresund/0.2"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read().decode("utf-8")


def norm_depth(d):
    """Samma djup ska ge samma nyckel oavsett om SMHI skickar "8", "8.0" eller 8."""
    try:
        return f"{float(d):g}"
    except (TypeError, ValueError):
        return str(d).strip()


def archive(p, s):
    """Rader (tid, värde, djup) ur corrected-archive CSV."""
    rows = []
    for line in get(API.format(p=p, s=s, period="corrected-archive/data.csv")).splitlines():
        parts = line.split(";")
        if len(parts) >= 4 and len(parts[0]) == 19 and parts[0][4] == "-":
            try:
                rows.append((parts[0], float(parts[1]), norm_depth(parts[3])))
            except ValueError:
                pass
    return rows


def latest(p, s):
    """Rader (tid, värde, djup) ur latest-day JSON. Tom lista om stationen inte svarar."""
    try:
        values = json.loads(get(API.format(p=p, s=s, period="latest-day/data.json"))).get("value") or []
    except Exception as e:
        print(f"  varning: latest-day {p}/{s}: {e}", file=sys.stderr)
        return []
    out = []
    for v in values:
        t = datetime.fromtimestamp(v["date"] / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        out.append((t, float(v["value"]), norm_depth(v.get("depth", ""))))
    return out


def merge(archive_rows, latest_rows):
    """En mätning per (tid, djup). Granskade arkivvärden går före senaste dygnet."""
    rows = {(t, d): v for t, v, d in latest_rows}
    rows.update({(t, d): v for t, v, d in archive_rows})
    return [(t, v, d) for (t, d), v in sorted(rows.items())]


def daily_means(rows, depth, scale):
    """Dygnsmedel och antal mätningar per dygn."""
    acc = defaultdict(list)
    for t, v, d in rows:
        if d == depth:
            acc[t[:10]].append(v * scale)
    return {d: (sum(v) / len(v), len(v)) for d, v in sorted(acc.items())}


def doy(d):
    """Dag på året 0 till 364 i ett normalår. 29 februari räknas som 28 februari."""
    day = 28 if (d.month, d.day) == (2, 29) else d.day
    return date(2001, d.month, day).timetuple().tm_yday - 1


def quantile(sorted_vals, q):
    return sorted_vals[int(q * (len(sorted_vals) - 1))]


def r1(x):
    return None if x is None else round(x, 1)


def normals(means, base):
    """Lista med 365 [p10, normal, p90], en per dag på året. None om basår saknas."""
    if not base:
        return None
    buckets = defaultdict(list)
    for ds, (v, _) in means.items():
        d = date.fromisoformat(ds)
        if base[0] <= d.year <= base[1]:
            buckets[doy(d)].append(v)
    out = []
    for i in range(365):
        vals = sorted(x for k in range(-WINDOW, WINDOW + 1) for x in buckets[(i + k) % 365])
        out.append([r1(quantile(vals, 0.1)), r1(statistics.fmean(vals)), r1(quantile(vals, 0.9))] if vals else None)
    return out


def iso(t):
    return t.replace(" ", "T") + "Z"


def build_base():
    cutoff = (datetime.now(timezone.utc).date() - timedelta(days=KEEP)).isoformat()
    series = {}
    for key, (p, s, depth, base, scale, *_ ) in SERIES.items():
        rows = [r for r in archive(p, s) if r[2] == depth]
        series[key] = {
            "normals": normals(daily_means(rows, depth, scale), base),
            "recent": [[t, v] for t, v, _ in rows if t[:10] >= cutoff],
        }
        print(f"{key}: {len(rows)} arkivrader, {len(series[key]['recent'])} sparade")
    out = {"built": datetime.now(timezone.utc).isoformat(timespec="minutes").replace("+00:00", "Z"), "series": series}
    OUT.mkdir(exist_ok=True)
    (OUT / "base.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
    return out


def build_current(base_data):
    now = datetime.now(timezone.utc)
    today = now.date().isoformat()
    daily, hourly = [], defaultdict(dict)
    for key, (p, s, depth, base, scale, name, unit) in SERIES.items():
        lat = latest(p, s)
        b = base_data["series"][key]
        recent = [(t, v, depth) for t, v in b["recent"]]
        means = daily_means(merge(recent, lat), depth, scale)
        for ds in list(means)[-DAYS:]:
            value, n = means[ds]
            norm = b["normals"][doy(date.fromisoformat(ds))] if b["normals"] else None
            p10, normal, p90 = norm or (None, None, None)
            daily.append({
                "param": key, "name": name, "unit": unit,
                "base": f"{base[0]}–{base[1]}" if base else None,
                "date": ds, "value": r1(value), "n": n,
                "partial": ds >= today,  # dygnet pågår fortfarande (UTC)
                "p10": p10, "normal": normal, "p90": p90,
            })
        for t, v, d in lat:
            if d == depth:
                hourly[t][key] = r1(v * scale)
    for key, s in LEVELS.items():
        for t, v, _ in latest(6, s):
            hourly[t][key] = r1(v)
    hourly_rows = []
    for t, v in sorted(hourly.items())[-24:]:
        row = {"time": iso(t), **v}
        if "levelS" in v and "levelV" in v:
            row["flow"] = r1(v["levelS"] - v["levelV"])  # positivt = norrut
        hourly_rows.append(row)

    meta = {
        "source": "SMHI, bearbetat (dygnsmedel, normalspann, syre i mg/l). CC BY 4.0.",
        "fetched": now.isoformat(timespec="minutes").replace("+00:00", "Z"),
        "base_built": base_data["built"],
        "latest": hourly_rows[-1]["time"] if hourly_rows else None,
    }
    OUT.mkdir(exist_ok=True)
    (OUT / "current.json").write_text(json.dumps(
        {"meta": meta, "daily": daily, "hourly": hourly_rows}, ensure_ascii=False, separators=(",", ":")))
    print(f"Klart: {len(daily)} dygnsrader, {len(hourly_rows)} timrader, senaste {meta['latest']}")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode not in ("base", "current", "all"):
        sys.exit("Användning: fetch_smhi.py [base|current]")
    base_data = build_base() if mode in ("base", "all") else None
    if mode in ("current", "all"):
        if base_data is None:
            base_data = json.loads((OUT / "base.json").read_text())
        build_current(base_data)


if __name__ == "__main__":
    main()
