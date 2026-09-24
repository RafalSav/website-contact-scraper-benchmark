# German field sample — 150 random `.de` domains

`field_sample_de150.json` is to the Impressum listing what `field_sample_yc300.json`
is to the main one: a list nobody curated, used to measure what the engine returns
on German sites and to compare engine versions.

## How it was drawn

From the Tranco top-1M list `L5PV4` (created 2026-09-23, permanent download at
<https://tranco-list.eu/download/L5PV4/1000000>): every domain ending in `.de`
ranked below 10,000 — the top of the list is platforms and CDNs — then 150 of them
at random with `random.seed(42)`.

```python
import csv, random
rows = [(int(r[0]), r[1]) for r in csv.reader(open('top-1m.csv'))
        if r[1].endswith('.de') and int(r[0]) > 10000]
random.seed(42)
sample = random.sample(rows, 150)
```

## What it is and is not

A popularity ranking, not a business register: next to shops, manufacturers and
agencies it holds associations, public bodies, publishers and hosts that serve no
website at all. On the first run (2026-09-24) 44 of the 150 could not be fetched.
That makes it a fair test of precision on German legal pages, and a rough one of
yield for any particular customer's list.
