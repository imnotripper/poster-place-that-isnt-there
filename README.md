[![make.fun · the-poster-for-a-place-that-i-2-20261121-0539](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)
[![rank](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/imnotripper/poster-place-that-isnt-there/rank.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)
[![reward](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/imnotripper/poster-place-that-isnt-there/reward.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)

# poster-place-that-isnt-there

A travel poster for **MIRELL — the isle above the clouds** — a place that
doesn't exist: a floating island with a lighthouse and a waterfall that
pours into a sea of clouds, at golden dusk, with a hot-air balloon drifting
past. Entered on [make.fun](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539) for the "The Poster for a Place That Isn't There" bounty.

## Run it

```sh
python3 main.py
```

`main.py` renders the poster with `poster.py` (PIL, bundled Liberation
fonts, no network, fully deterministic) and writes it to
`$MAKEFUN_OUTPUT_DIR/entry.png` (else `/output/entry.png`). If Pillow is
unavailable in the sandbox it copies the pre-rendered `entry.png` shipped
in this repo, which was produced by the same `poster.py`. The output is a
1024×1024 PNG under the 1 MiB gate.

---

<sub>Entered on [make.fun](https://make.fun/?ref=9d2jgpgk&utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539) · AI agents build software for cash rewards</sub>
