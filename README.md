# news-image-20261118 — The World Today

[![make.fun bounty](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![make.fun rank](https://make.fun/badge/news-image-20261118/4Quaranz/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118)
[![make.fun reward](https://make.fun/badge/news-image-20261118/4Quaranz/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118)

A front page that sums up Wednesday 18 November 2026 in a single
image, built for make.fun's "Sum up 18 November's world news in one
image" bounty. The page leads with the day's biggest stories — the
Kerch Bridge strike, the Hormuz tanker mines, the Manila summit,
the JPMorgan outage, the lost Vulcan payload, and the Rwanda
returns hubs — with a ticker of the day's smaller headlines below.

## What it does

The repository holds the finished artwork as `entry.png` (a
1024×1024 JPEG, under 1 MiB). The program `main.py` publishes it to
`/output/entry.png`: a straight deterministic copy, no network, no
clock, no randomness. After copying, it hashes the source and the
copy and only reports success when the two SHA-256 digests match,
so a short or corrupted write can never slip through unnoticed.

## Files in this repository

- `main.py` — the publishing program (Python 3.13, standard library only)
- `entry.png` — the finished front page artwork
- `LICENSE` — MIT license

## Run it

```sh
python3 main.py
```

Useful options:

- `--out <path>` — write somewhere other than `/output/entry.png`
- `--artwork <path>` — publish a different image file
- `--no-verify` — skip the digest check after copying
- `--quiet` — print nothing on success

## Verify the output

Run the program twice and compare the two outputs — they must be
byte-identical, and their digest must match the artwork in this
repository:

```sh
python3 main.py
sha256sum /output/entry.png
python3 main.py --quiet
sha256sum /output/entry.png
```

A non-zero exit means something went wrong: `2` the artwork is
missing, `3` the destination cannot be written, `4` the digests do
not match after copying, `5` source and destination are the same file.

---

Built with [make.fun](https://make.fun/bounty/news-image-20261118) — [join with my referral link](https://make.fun/?ref=scveefga)
