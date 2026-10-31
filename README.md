# SENTINEL-INFRA

An OSINT-driven infrastructure intelligence prototype for defence logistics planning, built for the Army internship selection assignment.

It reads scattered public updates (government handles, news, social posts) about roads, ports, rail and airports in eight states (Maharashtra, Gujarat, Goa, Tamil Nadu, Andhra Pradesh, Telangana, Kerala, Madhya Pradesh), and turns them into a verified project register with:

1. **Structured extraction** - cost, length, status, states, completion year pulled from free text.
2. **Verification** - every project gets a confidence score based on how many independent sources report it and how trustworthy they are. Conflicting numbers (for example a rumour that doubles a port's cost) are flagged, not silently averaged.
3. **Dual-use score (0-100)** - how useful a civilian asset would be for military movement.
4. **Delay-risk flags** - from words like "delayed", "land acquisition", and deadline checks.
5. **Mobilization model** - shortest-time convoy/rail routes between hubs, a single-failure test that finds critical links, and a "what do we gain when ongoing projects finish" comparison.
6. **Dashboard** - one static HTML file, no server needed.

> **Important:** the data in `data/` is *illustrative sample data* written to look like real feeds. It is not a live feed and figures must not be treated as authoritative. Speeds and scores are planning assumptions. See `docs/LIMITATIONS.md`.

## Quick start

Needs Python 3.9+ and nothing else (standard library only).

```bash
git clone <your-repo-url>
cd sentinel-infra
PYTHONPATH=src python -m sentinel        # runs the pipeline
python -m unittest discover -s tests     # runs the tests
```

Open `outputs/dashboard.html` in a browser. Machine-readable results are in `outputs/analysis.json` and `outputs/projects.csv`.

## Project layout

```
data/        feeds.json, nodes.csv, network.csv  (sample inputs)
src/sentinel extract, verify, dualuse, risk, bottleneck, geo, pipeline, dashboard
tests/       unit tests
docs/        ARCHITECTURE.md, LIMITATIONS.md, ROADMAP.md
outputs/     generated results
```

## Plugging in real data

Replace `data/feeds.json` with items shaped like `{"id","source","source_type","date","text"}`. `source_type` is `official`, `news` or `social`. A scraper/RSS/API collector can write this file; the rest of the pipeline stays the same. Add new projects to `PROJECT_KEYS` in `extract.py` and `CENTROIDS` in `dualuse.py`.

## Sample result (from the included data)

- 12 projects registered, 1 unverified lead (an anonymous Telegram post) kept out of the register.
- Vadhavan port, Vizhinjam port and NH-65 flagged for review because of conflicting cost claims.
- The Hyderabad-Visakhapatnam road is a single point of failure in the model until Hyderabad-Vijayawada six-laning finishes.
- Bhopal to Visakhapatnam movement drops from about 36.8 to 27.6 hours once ongoing links are completed.

## Licence

MIT. Prototype for educational/selection purposes; uses public information only.
