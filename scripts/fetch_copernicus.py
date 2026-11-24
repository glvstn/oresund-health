"""Hämtar klorofyll och klarhet vid ytan runt Flinten från Copernicus Marine och räknar dygnsvärde och normalspann.

    python3 scripts/fetch_copernicus.py     # -> data/klorofyll.json och data/klarhet.json

Satellitdata (Sentinel-3 OLCI, 300 m), bara ytan och bara molnfria dagar. Två produkter med var sitt dataset
för plankton (CHL) och genomskinlighet (KD490):
- Normalspann och äldre dygn: OCEANCOLOUR_BAL_BGC_L3_MY_009_133 (DOI 10.48670/moi-00296), OLCI från 2016.
- Senaste dygnen: OCEANCOLOUR_BAL_BGC_L3_NRT_009_131 (DOI 10.48670/moi-00294), sparar bara cirka tio dygn.
Där båda har samma dygn används MY, som är bearbetat på samma sätt som normalspannet.

Klarhet visas som djupet där ljuset (490 nm) har halverats, ln 2 / KD490 i meter. Det följer direkt av vad KD490 är
(ljuset avtar exponentiellt med djupet) och är ingen empirisk omräkning till siktdjup.

Dygnsvärde = median av pixlarna i rutan, bara om minst MIN_COVER av vattenpixlarna har värde.
Annars räknas dygnet som saknat (moln). Bara mars till oktober (SEASON): från november till början av februari står
solen så lågt vid 55,6 N att värdena blir orimliga, i december och januari 8 till 9 gånger över vattenproven från
Klagshamn i SHARK, mot 1,2 till 2,6 gånger resten av året (jämfört 2026-11-23). KD490 visar samma sak: siktdjupet
i proverna ligger kring 6 m hela året, men KD490 är 2 till 5 gånger högre november till februari (jämfört 2026-11-24). Normalspann som för SMHI-serierna: p10 till p90 inom +-7 dygn, basår 2017 till 2025.
Inget betyg, se docs/beslut.md.

Kräver paketet copernicusmarine och inloggning, antingen via `copernicusmarine login` eller
miljövariablerna COPERNICUSMARINE_SERVICE_USERNAME och COPERNICUSMARINE_SERVICE_PASSWORD.
Källangivelse: Generated using E.U. Copernicus Marine Service Information, bearbetat.
"""
import json
import math
import statistics
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import copernicusmarine as cm
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "data"
# namn: (MY-dataset, NRT-dataset, variabel, omräkning av dygnets median, enhet, rubrik)
PRODUCTS = {
    "klorofyll": ("cmems_obs-oc_bal_bgc-plankton_my_l3-olci-300m_P1D-m", "cmems_obs-oc_bal_bgc-plankton_nrt_l3-olci-300m_P1D",
                  "CHL", lambda v: v, "µg/l", "Klorofyll vid ytan, Flinten"),
    "klarhet": ("cmems_obs-oc_bal_bgc-transp_my_l3-olci-300m_P1D", "cmems_obs-oc_bal_bgc-transp_nrt_l3-olci-300m_P1D",
                "KD490", lambda v: math.log(2) / v, "m", "Klarhet vid ytan, djup där ljuset halverats, Flinten"),
}
# Ruta på cirka 6 x 6 km kring Flinten 7 (55,589 N, 12,845 E), söder om Saltholm.
BOX = dict(minimum_latitude=55.56, maximum_latitude=55.62, minimum_longitude=12.79, maximum_longitude=12.90)
START = "2016-05-01"
BASE = (2017, 2025)
DAYS = 366
WINDOW = 7
MIN_COVER = 0.25
SEASON = range(3, 11)  # månader som används, se ovan


def doy(d):
    """Dag på året 0 till 364 i ett normalår. 29 februari räknas som 28 februari."""
    day = 28 if (d.month, d.day) == (2, 29) else d.day
    return date(2001, d.month, day).timetuple().tm_yday - 1


def quantile(sorted_vals, q):
    return sorted_vals[int(q * (len(sorted_vals) - 1))]


def r2(x):
    return None if x is None else round(x, 2)


def load(dataset_id, var, start):
    ds = cm.open_dataset(dataset_id=dataset_id, variables=[var], start_datetime=start, **BOX)
    da = ds[var].load()
    days = [str(t)[:10] for t in da["time"].values]
    return days, da.values.reshape(len(days), -1)


def daily_values(days, grid, water, conv):
    """{datum: (omräknad median, andel vattenpixlar med värde)} för dygn med tillräcklig täckning."""
    out = {}
    for d, row in zip(days, grid):
        if int(d[5:7]) not in SEASON:
            continue
        vals = row[water & np.isfinite(row)]
        cover = len(vals) / water.sum()
        if cover >= MIN_COVER:
            out[d] = (conv(float(np.median(vals))), cover)
    return out


def normals(values):
    buckets = defaultdict(list)
    for ds, (v, _) in values.items():
        d = date.fromisoformat(ds)
        if BASE[0] <= d.year <= BASE[1]:
            buckets[doy(d)].append(v)
    out, counts = [], []
    for i in range(365):
        vals = sorted(x for k in range(-WINDOW, WINDOW + 1) for x in buckets[(i + k) % 365])
        counts.append(len(vals))
        in_season = (date(2001, 1, 1) + timedelta(days=i)).month in SEASON
        ok = in_season and len(vals) >= 10
        out.append([r2(quantile(vals, 0.1)), r2(statistics.median(vals)), r2(quantile(vals, 0.9))] if ok else None)
    return out, counts


def build(key):
    my_id, nrt_id, var, conv, unit, name = PRODUCTS[key]
    my_days, my_grid = load(my_id, var, START)
    water = np.isfinite(my_grid).any(axis=0)  # pixlar som någon gång haft värde, resten är land
    my = daily_values(my_days, my_grid, water, conv)
    print(f"{key} MY: {len(my_days)} dygn, {water.sum()} vattenpixlar, {len(my)} dygn med minst {MIN_COVER:.0%} täckning")

    since = (datetime.now(timezone.utc).date() - timedelta(days=30)).isoformat()
    nrt_days, nrt_grid = load(nrt_id, var, since)
    nrt = daily_values(nrt_days, nrt_grid, water, conv)
    print(f"{key} NRT: {len(nrt_days)} dygn ({nrt_days[0] if nrt_days else '-'} till {nrt_days[-1] if nrt_days else '-'}), {len(nrt)} användbara")

    norm, counts = normals(my)
    values = {**nrt, **my}
    cutoff = (datetime.now(timezone.utc).date() - timedelta(days=DAYS)).isoformat()
    daily = []
    for ds in sorted(d for d in values if d >= cutoff):
        v, cover = values[ds]
        p10, normal, p90 = norm[doy(date.fromisoformat(ds))] or (None, None, None)
        daily.append({
            "date": ds, "value": r2(v), "cover": round(cover, 2),
            "source": "MY" if ds in my else "NRT",
            "p10": p10, "normal": normal, "p90": p90,
        })

    meta = {
        "name": name, "unit": unit,
        "source": "Generated using E.U. Copernicus Marine Service Information, bearbetat (median över rutan, normalspann).",
        "doi": ["https://doi.org/10.48670/moi-00294", "https://doi.org/10.48670/moi-00296"],
        "box": BOX, "base": f"{BASE[0]}–{BASE[1]}", "min_cover": MIN_COVER, "season": [SEASON.start, SEASON.stop - 1],
        "fetched": datetime.now(timezone.utc).isoformat(timespec="minutes").replace("+00:00", "Z"),
        "latest": daily[-1]["date"] if daily else None,
        "normal_days": counts,  # antal dygn bakom normalspannet per dag på året
    }
    OUT.mkdir(exist_ok=True)
    (OUT / f"{key}.json").write_text(json.dumps(
        {"meta": meta, "daily": daily, "normals": norm}, ensure_ascii=False, separators=(",", ":")))
    print(f"{key} klart: {len(daily)} dygn med värde senaste året, senaste {meta['latest']}")


def main():
    for key in PRODUCTS:
        build(key)


if __name__ == "__main__":
    main()
