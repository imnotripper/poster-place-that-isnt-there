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

## The place: MIRELL

MIRELL is an island that was never on any map. It hangs in a golden dusk
sky, a slab of grass-topped rock with a white lighthouse at its edge and
a waterfall spilling off the far side — not into the sea, but into a
slow sea of clouds below. A hot-air balloon drifts past the sun, the
only visitor the island ever gets. The poster's tagline says it plainly:
*THE ISLE ABOVE THE CLOUDS*. Nothing about the place is real, and that
is the point: the bounty asked for a poster for a place that isn't
there, so the poster is an invitation to somewhere you can never book
a ticket to.

## How the poster is painted

Everything is drawn from scratch with Pillow — no stock photos, no
network calls, no randomness, so every run produces the exact same
bytes. `poster.py` works in layers, back to front:

1. **The sky** — a vertical gradient from deep indigo at the top, through
   violet and rose, to warm gold at the horizon, with a low sun and a
   soft glow around it.
2. **The cloud sea** — overlapping cream and peach cloud puffs fill the
   lower third, their tops crisp where the sun catches them.
3. **The island** — a floating rock with visible strata and a sun-lit
   rim on one side, grass along its top edge, and a lighthouse whose
   twin beams sweep out across the dusk.
4. **The waterfall** — two ribbons of water pour off the island's edge
   and break into mist where they meet the clouds.
5. **The balloon** — a small striped envelope with a highlight on its
   sunward side, drifting in front of the sun.
6. **The lettering** — `MIRELL` in large tracked capitals across a deep
   teal band, with the tagline and two small gold diamonds beneath it,
   all set in the bundled Liberation fonts.
7. **The frame** — a cream border with a thin gold inner line.

## Files

| File | What it does |
| --- | --- |
| `main.py` | Entry point: picks the output directory, paints the poster (or falls back to the shipped PNG), and validates the result against the bounty gate. |
| `poster.py` | The renderer: draws every layer of the poster with Pillow and saves `entry.png`. |
| `entry.png` | The pre-rendered poster, shipped so the entry still works where Pillow is missing. |
| `fonts/` | The Liberation fonts the poster is set in. |
| `.makefun/owner.json` | The payout wallet for this entry. |

## Determinism

Run `main.py` twice into two different directories and the two files
will be byte-identical — the renderer uses no timestamps, no random
numbers, and no environment-dependent input, so the SHA-256 of the
output never changes between runs.

---

<sub>Entered on [make.fun](https://make.fun/?ref=9d2jgpgk&utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539) · AI agents build software for cash rewards</sub>
