# NPO-lijst op GitHub Pages: nieuwe repo, stap voor stap

Resultaat: drie CSV-bestanden per regio, elk uur ververst vanuit de master, geschoond van contactgegevens, op een kort adres dat Claude rechtstreeks kan ophalen:
`https://<organisatie>.github.io/npo-list/data/npo-flanders.csv` (en -brussels, -wallonia).

Vooraf: laat iemand in het Teams-project vragen "Haal https://pages.github.com op en zeg wat de paginatitel is." Lukt dat, dan is github.io bereikbaar en werkt dit. Lukt het niet, dan koppelen we een subdomein van giveaday.eu (zie onderaan).

## Bestanden in deze map (allemaal in de root van de repo zetten, met dezelfde paden)

| Bestand | Waarvoor |
|---|---|
| `.github/workflows/npo-mirror.yml` | De Action: draait elk uur het script en bewaart het resultaat |
| `scripts/npo_mirror.py` | Haalt de gepubliceerde CSV op, maskeert mails en nummers, splitst per regio |
| `index.html` | Lege startpagina, met noindex |
| `robots.txt` | Zoekmachines buiten |
| `.nojekyll` | Leeg bestand; zorgt dat GitHub Pages de bestanden ongewijzigd serveert |

## Stappen (20 minuten, één keer)

1. **Repo aanmaken.** Op github.com, ingelogd in de Give a Day-organisatie (of je eigen account als er geen organisatie is): New repository. Naam `npo-list`, zichtbaarheid **Public** (Pages op een gratis plan vereist dat; de inhoud is toch enkel organisatiedata), vink "Add a README" aan, Create.
2. **Bestanden toevoegen.** In de repo: Add file > Upload files, sleep de vijf bestanden uit deze map erin, inclusief de mappen `.github/workflows` en `scripts` (uploaden van mappen werkt door de hele map te slepen). Lukt dat niet, maak ze dan één voor één via Add file > Create new file, met het volledige pad als bestandsnaam (bijvoorbeeld `.github/workflows/npo-mirror.yml`); GitHub maakt de mappen zelf. Commit op `main`.
3. **Secret zetten.** Settings > Secrets and variables > Actions > New repository secret. Name: `NPO_SOURCE_URL`. Secret: de gepubliceerde CSV-URL van het tabblad "Claude" (eindigt op `gid=386448200&single=true&output=csv`). Add secret.
4. **Schrijfrechten voor de Action.** Settings > Actions > General > onderaan "Workflow permissions" > kies "Read and write permissions" > Save.
5. **Pages aanzetten.** Settings > Pages > Build and deployment > Source "Deploy from a branch" > Branch `main`, map `/ (root)` > Save. GitHub toont na een minuut de URL `https://<organisatie>.github.io/npo-list/`.
6. **Eerste keer draaien.** Tabblad Actions > links "NPO list mirror" > rechts "Run workflow" > Run. Na een minuut is de run groen; klik erop en open "Fetch, clean and split the list": je ziet "flanders: 167 rows, brussels: 87, wallonia: 44, total 257". De Action heeft nu een map `data/` gecommit.
7. **Controleren.** Open in de browser `https://<organisatie>.github.io/npo-list/data/npo-flanders.csv`. Downloadt een CSV? Klaar. 404? Wacht vijf minuten (Pages bouwt na elke commit) en herlaad. Blijft het 404: check stap 5 en of de map `data/` in de repo staat.
8. **Projectinstructies aanpassen.** Vervang de databronzin door:

   "Data source: three live CSV files, organisation data only, refreshed hourly: https://<organisatie>.github.io/npo-list/data/npo-flanders.csv (about 167 rows), .../npo-brussels.csv (about 87), .../npo-wallonia.csv (about 44). Fetch the part of the client's region at the start of every sourcing request; add Brussels for clients in Flemish or Walloon Brabant; for Brussels clients add Flanders for Dutch-speaking groups and Wallonia for French-speaking groups. State which parts you read and how many organisations each contained. If a fetch fails, say so and use the snapshot file in project knowledge, mentioning its date."

   Laat de snapshot als vangnet in de projectkennis staan.
9. **Test in het project.** "Haal de drie delen op en zeg per deel hoeveel organisaties je leest." Verwacht 167, 87 en 44.
10. **Beveiliging, eenmalig.** Settings van de organisatie > Authentication security > tweestapsverificatie verplicht. Schrijftoegang tot de repo enkel voor wie ze onderhoudt.

## Wat het script doet
- Haalt de gepubliceerde CSV op; GitHub volgt de Google-doorverwijzing zonder probleem.
- Houdt alle 15 kolommen, inclusief de accountmanager (beslissing 12 november). Een kolom weglaten kan via `DROP` in het script.
- Vervangt alles wat op een e-mailadres of gsm-nummer lijkt door [mail] of [gsm], in elke cel.
- Splitst per regio; organisaties zonder regio komen in alle drie.
- Weigert te overschrijven bij minder dan 50 rijen, zodat een storing bij Google de lijst niet leegmaakt.
- Commit enkel als er iets veranderd is.

## Later: eigen subdomein (enkel als github.io niet bereikbaar blijkt, of IT het netter wil)
Bij wie het DNS van giveaday.eu beheert: een CNAME-record `data` dat wijst naar `<organisatie>.github.io`. Dan in de repo Settings > Pages > Custom domain `data.giveaday.eu`, "Enforce HTTPS" aan. De bestanden staan dan op `https://data.giveaday.eu/data/npo-flanders.csv`; pas de URL's in de instructies aan.

## Onderhoud
Niets, tot de master van kolommen verandert. Dan faalt de Action met een melding over "Region"; pas de kolomnaam in het script aan. Wordt de Google-publicatie ooit stopgezet, dan blijft de laatste versie van de bestanden gewoon staan en meldt de Action een fout bij het ophalen.
