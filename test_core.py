import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from sentinel.extract import extract
from sentinel.verify import consolidate
from sentinel import bottleneck as bn
from sentinel.geo import load_edges

ROOT = Path(__file__).resolve().parents[1]

def item(t, st="official"):
    return {"id": "X", "source": "S", "source_type": st, "date": "2026-01-01", "text": t}

class T(unittest.TestCase):
    def test_extract_cost_km_state(self):
        r = extract(item("Samruddhi Mahamarg 701 km in Maharashtra, Rs 55,000 crore, operational."))
        self.assertEqual(r["cost_crore"], 55000.0)
        self.assertEqual(r["length_km"], 701.0)
        self.assertEqual(r["states"], ["Maharashtra"])
        self.assertEqual(r["status"], "operational")

    def test_airport_not_port(self):
        self.assertEqual(extract(item("Mopa airport Goa"))["asset_type"], "airport")

    def test_conflict_flagged(self):
        a = extract(item("Vadhavan port Rs 76,000 crore"))
        b = extract(item("Vadhavan port Rs 1,10,000 crore", "social"))
        proj, _ = consolidate([a, b])
        self.assertIsNotNone(proj[0]["cost_conflict"])
        self.assertEqual(proj[0]["cost_crore"], 76000.0)  # official wins

    def test_social_alone_low_confidence(self):
        proj, _ = consolidate([extract(item("Vadhavan port rumour", "social"))])
        self.assertLess(proj[0]["confidence"], 0.6)

    def test_routing_and_failure(self):
        edges = load_edges(ROOT / "data" / "network.csv")
        t, path = bn.shortest(bn._graph(edges), "Pune", "Mumbai")
        self.assertAlmostEqual(t, 150 / 40)
        self.assertTrue(bn.critical_edges(edges, [("Pune", "Mumbai")]))

if __name__ == "__main__":
    unittest.main()
