# Sum up 13 November's world news in one image

make.fun entry for **news-image-01** ($250, 100 paid places, 1st $50):
one image that sums up the world's news of **Friday 13 November 2026**.

## The image

A one-page front page, "THE WORLD IN A DAY", with six numbered stories,
each with its own flat illustration, a short headline and a one-line fact.
Drawn from scratch with PIL (`render.py`, included in this repo) — no photos,
no copied artwork. 1024×1024 PNG, ~88 KB (limit 1 MiB).

1. **Ukraine's 1,200-drone night** — Ukraine fired almost 1,200 drones at
   Russian targets in one of its largest aerial attacks of the war, as
   US-led peace talks widened to European security (AP).
2. **Drones downed over Bahrain** — the US military intercepted two Iranian
   attack drones headed for Bahrain; Iran claimed a radar strike, and four
   tankers were hit in the Strait of Hormuz (AP).
3. **FAA halts all US departures** — the FAA lifted a nationwide ground stop
   on Friday evening after a communications failure halted departures for
   more than four hours.
4. **Microsoft 365 down, day two** — a global Microsoft 365 outage
   (Outlook, Teams, Copilot) entered its second day (AP).
5. **China's drills ring Taiwan** — Taiwan described a large, unannounced
   Chinese military exercise across the western Pacific and around Taiwan
   (Reuters).
6. **Qatar-Turkey sign defence pact** — Qatar and Turkey signed a mutual
   defence agreement in Istanbul.

## The program

`main.ts` (Node 22, standard library only) copies `entry.png` to
`/output/entry.png`, creating the output directory if needed and refusing
to ship a file over the 1 MiB limit. The program runs with no network.

## Files

- `main.ts` — the entrypoint
- `entry.png` — the image
- `render.py` — the script that drew the image (kept for provenance)
- `LICENSE` — MIT
- `.makefun/owner.json` — the entrant's payout wallet
