"""Hämtar från DMI: prognos för lutningen genom Öresund och uppmätt vind vid Drogden fyr.

    python3 scripts/fetch_dmi.py           # prognos -> data/prognos.json (en gång per modellkörning)
    python3 scripts/fetch_dmi.py vind      # vind -> data/vind.json (varje timme)

Vind: DMI:s väderstation 06183 Drogden fyr mitt i sundet, tiominutersmedel 10 m över havet. Riktningen är
varifrån det blåser, i grader. Det senaste dygnet sparas, en mätning per hel timme.

Havsmodellen DKSS, samlingen dkss_idw, via DMI:s öppna EDR-API (ingen nyckel sedan december 2025).
Modellen körs 00, 06, 12 och 18 UTC och är klar cirka 3 timmar 20 minuter senare, prognos 5 dygn.
Lutning = Skanör minus Viken i cm, positivt betyder att vattnet rinner norrut, som i current.json.
Bara riktningen används på sidan, inte modellens strömfart, som var 2 till 3 gånger för hög vid Flinten
jämfört med SMHI:s mätare (docs/datakallor.md).

Bara standardbiblioteket. Data: DMI, CC BY 4.0, bearbetat till skillnaden mellan två punkter.
"""
import json
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API = ("https://opendataapi.dmi.dk/v1/forecastedr/collections/dkss_idw/position"
       "?coords=POINT({lon}%20{lat})&parameter-name=sea-mean-deviation&crs=crs84&f=GeoJSON")
OBS = ("https://opendataapi.dmi.dk/v2/metObs/collections/observation/items"
       "?stationId=06183&parameterId={p}&period=latest-day&limit=300&sortorder=observed,DESC")
OUT = Path(__file__).resolve().parent.parent / "data"
# Modellens närmaste vattenpunkt. Viken flyttad till 12,56 E, eftersom stationens läge ligger på land i modellen.
POINTS = {"S": (12.8296, 55.4168), "V": (12.56, 56.14)}


def get(url):
    """GeoJSON-objekten från DMI. Ett nytt försök om DMI svarar långsamt eller ber oss vänta."""
    req = urllib.request.Request(url, headers={"User-Agent": "hur-mar-oresund/0.2"})
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.load(r)["features"]
        except OSError as e:
            if attempt == 2:
                raise
            # 429 betyder för många anrop: vänta så länge DMI ber om, annars en minut.
            wait = int(getattr(e, "headers", None) and e.headers.get("Retry-After") or 60)
            print(f"  varning: {e}, försöker igen om {wait} s", file=sys.stderr)
            time.sleep(min(wait, 300))


def series(lon, lat):
    """{tid: vattenstånd i m} från havsmodellen."""
    return {f["properties"]["step"][:13] + ":00:00Z": f["properties"]["sea-mean-deviation"] for f in get(API.format(lon=lon, lat=lat))}


def wind():
    obs = {p: {f["properties"]["observed"][:16]: f["properties"]["value"] for f in get(OBS.format(p=p))}
           for p in ("wind_speed", "wind_dir")}
    hourly = [{"time": t + ":00Z", "speed": obs["wind_speed"][t], "dir": obs["wind_dir"].get(t)}
              for t in sorted(obs["wind_speed"]) if t.endswith(":00")]
    if not hourly:
        raise SystemExit("Ingen vind från Drogden")
    meta = {
        "source": "DMI, väderstation Drogden fyr. CC BY 4.0.",
        "fetched": datetime.now(timezone.utc).isoformat(timespec="minutes").replace("+00:00", "Z"),
        "latest": hourly[-1]["time"],
    }
    OUT.mkdir(exist_ok=True)
    (OUT / "vind.json").write_text(json.dumps({"meta": meta, "hourly": hourly}, separators=(",", ":")))
    print(f"Klart: {len(hourly)} timmar vind, senaste {hourly[-1]}")


def forecast():
    s, v = (series(*POINTS[k]) for k in ("S", "V"))
    hourly = [{"time": t, "slope": round(100 * (s[t] - v[t]), 1)}
              for t in sorted(s) if s[t] is not None and v.get(t) is not None]
    if not hourly:
        raise SystemExit("Ingen prognos från DMI")
    meta = {
        "source": "DMI, havsmodellen DKSS, bearbetat till skillnaden i vattenstånd mellan Skanör och Viken. CC BY 4.0.",
        "fetched": datetime.now(timezone.utc).isoformat(timespec="minutes").replace("+00:00", "Z"),
        "first": hourly[0]["time"], "last": hourly[-1]["time"],
    }
    OUT.mkdir(exist_ok=True)
    (OUT / "prognos.json").write_text(json.dumps({"meta": meta, "hourly": hourly}, separators=(",", ":")))
    print(f"Klart: {len(hourly)} timmar, {meta['first']} till {meta['last']}, "
          f"lutning {min(h['slope'] for h in hourly)} till {max(h['slope'] for h in hourly)} cm")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "prognos"
    if mode not in ("prognos", "vind"):
        sys.exit("Användning: fetch_dmi.py [prognos|vind]")
    wind() if mode == "vind" else forecast()
