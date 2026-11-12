"""Fetch the published 'Claude' tab of the NPO view sheet, optionally drop columns,
strip anything that looks like an email or phone number, split by region, write CSV files.
Runs on GitHub Actions every hour. Source URL comes from the repository secret NPO_SOURCE_URL."""
import csv, io, os, re, sys, urllib.request

SRC = os.environ.get("NPO_SOURCE_URL")
if not SRC:
    sys.exit("NPO_SOURCE_URL secret is missing")

DROP = set()                                # columns to leave out of the public files, e.g. {"Account GaD"}
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE = re.compile(r"(\+32|\b0)[1-9](?:[ .\/-]?\d){7,8}\b")
REGIONS = {"flanders": "Flanders", "brussels": "Brussels", "wallonia": "Wallonia"}

raw = urllib.request.urlopen(SRC, timeout=60).read().decode("utf-8-sig")
rows = list(csv.reader(io.StringIO(raw)))
if len(rows) < 50:
    sys.exit(f"Only {len(rows)} rows fetched, refusing to overwrite")   # protects against a broken fetch

header = [h.split("\n")[0].strip() for h in rows[0]]
keep = [i for i, h in enumerate(header) if h not in DROP]
header = [header[i] for i in keep]
region_col = header.index("Region")

def clean(v):
    v = EMAIL.sub("[mail]", v)
    v = PHONE.sub("[gsm]", v)
    return v.strip()

data = []
for r in rows[1:]:
    if not any(c.strip() for c in r):
        continue
    r = r + [""] * (len(rows[0]) - len(r))
    data.append([clean(r[i]) for i in keep])

os.makedirs("data", exist_ok=True)
for slug, word in REGIONS.items():
    part = [r for r in data if word.lower() in r[region_col].lower() or not r[region_col]]
    with open(f"data/npo-{slug}.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(part)
    print(f"{slug}: {len(part)} rows")
with open("data/README.txt", "w") as f:
    f.write("Give a Day NPO list, organisation data only, no contact details. Refreshed hourly from the master sheet. "
            "Not for distribution; questions: info@giveaday.eu\n")
print(f"total {len(data)} organisations")
