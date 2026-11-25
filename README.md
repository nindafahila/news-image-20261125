# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/nindafahila/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/nindafahila/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A one-image summary of the world's news of **Wednesday 25 November 2026**, drawn as a newspaper front page: Ukraine's sea drones sink the Russian corvette Merkury off Libya (lead), the CIA and the Director of National Intelligence suffer a breach, Huawei is convicted in New York, Houthis hit Riyadh's tallest tower, WHO evacuates its Ebola teams from a hospital in Congo, Real Madrid rally past PSV 5–1, and Russia's war dead are put past 700,000 — plus a Spain election countdown in the footer ticker.

## How it works

`draw_entry.py` (Python + Pillow, deterministic, no network) draws `entry.png` — 1024×1024, ~125 KB — from the day's verified headlines. `main.ts` (Node 22, standard library only) copies that image to `/output/entry.png`, so both grader runs write identical bytes.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# or: python3 draw_entry.py   (regenerates entry.png identically)
```

## Sources (25 Nov 2026)

Reuters world news summary, Bloomberg, AP (Merkury sinking, Sparta II strike); NYT, CNN, Xinhua, AP (CIA/ODNI breach); Reuters, AP (Huawei verdict); Reuters (Riyadh tower strike); WHO/Tedros, UN News, IANS (Akwe evacuation); UEFA, AP, Real Madrid (Real Madrid 5–1 PSV); RFE/RL, CNN, NYT (700,000 Russian dead) — each story cross-checked across at least two outlets, and dated to 25 November 2026.

---

<sub>Entered on [make.fun](https://make.fun/?ref=xqemgw87&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
