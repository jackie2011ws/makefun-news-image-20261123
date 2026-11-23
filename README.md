# Sum up 23 November's world news in one image

make.fun bounty `news-image-20261123` — $100, 50 paid places.
Deadline: Wed 25 Nov 2026 00:00 UTC (11:00 AEDT).

## The entry

A clean, text-first newspaper front page, "THE WORLD IN ONE PAGE",
for Monday 23 November 2026. Six stories, chosen for breadth and
consequence, all as reported on 23 November 2026:

1. **COP31 collapses** — Antalya, Turkey. No deal on fossil fuels; the EU
   and about 130 countries reject a text that never mentions fossil fuels.
2. **Markets slide** — Nikkei -5.06%, S&P 500 -3.7% on AI fears.
3. **Strike hits Dymer** — Kyiv region. At least 10 killed; a 7-year-old
   boy pulled alive from the rubble.
4. **'El Chapo Isidro' captured** — Sinaloa, Mexico.
5. **The penny ends** — Trump signs the Common Cents Act, closing the
   penny's 232-year run.
6. **South Korea tops $1 trillion** — annual exports pass $1 trillion
   for the first time, driven by AI chip demand.

Also today: Marc Márquez wins an eighth MotoGP title; a Delta outage
delays 1,600+ flights; Denmark accuses Russia of a plot to kill a rapper
in Copenhagen.

## How it is built

- `render.py` draws `entry.png` (1024×1024, 143 KB) from `news.json`
  with Pillow, locally, no network, no randomness. Re-running it
  produces the same bytes.
- `entry.png.b64` is that same image as base64 text, so the repo
  carries it without a binary file.
- `main.ts` (Node 22, standard library only) decodes `entry.png.b64`
  and writes it to `/output/entry.png`. That is the graded program.
  Verified: two runs give identical bytes, sha256
  `90cdf31d6c40557d1e761c383ce56389c6cfed94e9a880f4b61e6cd4bf443d27`.

## Verify

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# out/entry.png — 1024x1024 PNG, under 1 MiB
# Run twice and compare sha256: identical.
python3 render.py   # regenerates entry.png deterministically
```
