#!/usr/bin/env python3
"""Extract all to-build episodes from the manifest into Context/episodes/<slug>.json,
then print a QA table and flag duplicate Spotify IDs / empty transcripts."""
import json, os, sys
from collections import Counter
from extract_episode import extract

HERE = os.path.dirname(os.path.abspath(__file__))
man = json.load(open(os.path.join(HERE, "podcast-build-manifest.json")))
todo = [r for r in man if not r["built"]]
outdir = os.path.join(HERE, "episodes")
os.makedirs(outdir, exist_ok=True)

rows = []
for r in todo:
    d = extract(r["url"])
    d["num"] = r["num"]
    d["date"] = r["date"]
    json.dump(d, open(os.path.join(outdir, r["slug"] + ".json"), "w"), ensure_ascii=False, indent=1)
    rows.append(d)
    spk = sum(1 for p in d["transcript"] if p["speaker"])
    print(f"ep{r['num']:>3} {r['date']} | notes {len(d['show_notes']):2} | tx {d['transcript_para_count']:3} (spk {spk:3}) "
          f"| spot {str(d['spotify_id'])[:12]:12} | {d['title'][:42]}")

print("\n--- QA ---")
# Spotify trust: an ID on >1 page means a copy-paste error on the later page(s).
# Keep the ID on the EARLIEST episode (likely the rightful owner), null the duplicates;
# nulled pages fall back to the per-episode YouTube embed. Flag all for manual review.
ids = Counter(d["spotify_id"] for d in rows if d["spotify_id"])
shared = {k for k, v in ids.items() if v > 1}
owner = {}
for k in shared:
    owner[k] = min(d["num"] for d in rows if d["spotify_id"] == k)
unreliable = []
for d in rows:
    sid = d["spotify_id"]
    nulled = sid in shared and d["num"] != owner[sid]
    d["spotify_unreliable"] = nulled
    if nulled:
        unreliable.append((d["num"], bool(d["youtube"])))
        d["spotify_id"] = None
    json.dump(d, open(os.path.join(outdir, d["slug"] + ".json"), "w"), ensure_ascii=False, indent=1)

print("kept Spotify on earliest, nulled duplicates:", [n for n, _ in unreliable] or "none")
print("  of those, NO youtube fallback:", [n for n, yt in unreliable if not yt] or "none (all have YouTube)")
print("empty transcript     :", [d["num"] for d in rows if d["transcript_para_count"] == 0] or "none")
print("thin transcript (<15):", [d["num"] for d in rows if 0 < d["transcript_para_count"] < 15] or "none")
print("no show notes        :", [d["num"] for d in rows if not d["show_notes"]] or "none")
print("\ntranscript-tail check (should be sign-offs, not bios/footer):")
for d in rows:
    if d["num"] in (2, 49, 50, 51):
        t = d["transcript"]
        print(f"  ep{d['num']}: {len(t)} paras; last = {repr((t[-1]['text'][:70]) if t else None)}")
print(f"\nsaved {len(rows)} episode JSONs to {outdir}")
