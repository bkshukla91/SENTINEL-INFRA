# Architecture

feeds.json -> extract.py -> verify.py -> dualuse.py + risk.py -> pipeline.py -> analysis.json / projects.csv / dashboard.html
nodes.csv + network.csv -> bottleneck.py (Dijkstra, edge-removal test) -> pipeline.py

- **extract**: regex + keyword rules, easy to read and audit. An LLM or spaCy NER can replace it later behind the same `extract(item)` signature.
- **verify**: noisy-OR confidence, `1 - prod(1 - w_i)`, weights official 0.90, news 0.65, social 0.20. Costs differing by more than 15% raise a conflict; the highest-credibility value is kept.
- **dualuse**: asset type + distance to nearest army/naval hub (haversine) + status + capacity + length.
- **bottleneck**: hub graph, convoy speed 40 km/h road, 35 km/h rail. Each operational link is removed in turn and routes recomputed.
