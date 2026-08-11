import sys, re
sys.path.insert(0, "/Users/rosswalker/projects/3sm_code/mcp-servers/gsc")
from gsc_client import GSCClient

c = GSCClient()
rows = c.query_analytics("sc-domain:accuriteexcavation.com", days=90, dimension="query", row_limit=5000)
print(f"total query rows (90d): {len(rows)}")

TERMS = ["clear", "grub", "stump", "road", "grade", "grading", "site prep", "site work",
         "topsoil", "dirt work", "subgrade", "compact", "dozer", "bulldoz", "lot ", "acre",
         "brush", "gps", "pad", "driveway", "gravel", "tree"]

hits = [r for r in rows if any(t in r["key"] for t in TERMS)]
hits.sort(key=lambda r: r["impressions"], reverse=True)
print(f"\n=== topic-relevant queries with impressions, last 90d (n={len(hits)}) ===")
print(f"{'query':<48}{'impr':>7}{'clk':>5}{'pos':>7}")
for r in hits[:45]:
    print(f"{r['key'][:48]:<48}{r['impressions']:>7}{r['clicks']:>5}{r['position']:>7.1f}")

print("\n=== of those: impressions>=15 and position 8-40 (real gap set) ===")
gap = [r for r in hits if r["impressions"] >= 15 and 8 <= r["position"] <= 40]
gap.sort(key=lambda r: r["impressions"], reverse=True)
for r in gap[:30]:
    print(f"{r['key'][:48]:<48}{r['impressions']:>7}{r['clicks']:>5}{r['position']:>7.1f}")
