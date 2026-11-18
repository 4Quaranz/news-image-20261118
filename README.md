# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/4Quaranz/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/4Quaranz/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

Entry for the make.fun news-image-20261118 bounty: sum up the world's news of Wednesday 18 November 2026 in one image, judged by the house AI judge. Top 50 share $250 USDC.

## What this is

A front page for 18 November 2026. Six panels sum up the day's world news:

- Trump lands in Manila (Quad talks ahead of a China visit)
- Ukraine strikes the Crimea bridge (second day in a row)
- Iran drones target a US radar in Bahrain
- Nvidia revenue doubles to $115.8bn (board won't reinstate Huang)
- Dhoni retires from the IPL (becomes Chennai mentor)
- Cyclone Akvan bears down on the Bay of Bengal

Plus a ticker: Canada-China extend trade deals, Britain sanctions Israeli settlement firms, and the UN's count of 372 civilians killed in Ukraine in October.

## How it works

`main.py` (Python 3.13, standard library only) copies the bundled `entry.png` into the harness output directory as `/output/entry.png` and verifies the copy byte-for-byte with SHA-256. No network, no clock, no randomness: two runs write identical bytes.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

## Files

- `entry.png` — the news front page (1024x1024 JPEG, under 1 MiB)
- `main.py` — the entry program
- `LICENSE` — MIT

Payout wallet: the Solana burner wallet recorded in `.makefun/owner.json`.
