# Field report — 300 random Y Combinator companies

Run on 300 domains sampled at random (seed 42) from the public Y Combinator
company API, `maxContactPages: 3`, `renderJs: off`, on the live Store build.
The list was picked independently of this Actor and is deliberately hard:
modern startup sites, mostly Framer/Next.js, often with a contact form instead
of a published address.

Unlike `golden_set.json` — which measures *accuracy* against hand-verified
labels — this measures **yield**: on a list nobody curated, how many domains
give you something usable, and at what price.

## Results

| Metric | Value |
|---|---|
| Domains scanned | 300 |
| Yielded at least one contact | **244 (81.3%)** |
| Yielded an email | 182 (60.7%) |
| Yielded a social profile | 197 (65.7%) |
| Could not be fetched (`unreachable`) | 3 (1.0%) |
| Emails found | 247 — 116 named (47%), 236 MX-valid (96%) |
| Phones found | 27 |
| Social profiles found | 506 |
| Pages fetched | 494 (1.6 per domain) |
| **Total cost** | **$1.33** ($0.0044 per domain) |

Notably, **47% of the emails are addressed to a person**, not a role
inbox — those are the ones worth an outreach sequence.

## What browser rendering is worth, measured

The 56 domains that yielded nothing were then re-run with `renderJs: auto`
(2048 MB) — the honest test, since these are exactly the sites a no-JS pass
could not crack:

| | Result |
|---|---|
| Domains recovered | **24 of 56 (42.9%)** — 23 of them via the browser |
| Emails recovered | 19 (10 addressed to a person) |
| Social profiles recovered | 35 |
| Cost of the retry | **$0.09** |

End to end, that moves coverage of the 300-domain list from **81.3% to 89.3%**,
and domains with an email from **60.7% to 66.3%**, for a total of **$1.42**.

Two things worth noting: `auto` only starts a browser for sites the fast path
could not read, so the retry cost nine cents rather than a multiple of the main
run; and 32 of the 56 still yielded nothing, which is the honest answer — a
browser is not a skeleton key, and many startup sites simply publish a contact
form and nothing else.

## What it costs against the incumbent

The incumbent bills per page scraped; we bill per result. On this exact run:

| | Cost for these 300 domains |
|---|---|
| This Actor | $1.33 |
| Incumbent, FREE tier ($0.002/page × 494) | $0.99 |
| Incumbent, GOLD tier ($0.00105/page × 494) | $0.52 |
| Incumbent, FREE + email verification ($0.10 × 247) | $25.69 |

So on a realistic list we are about **34% more expensive** than the
incumbent's base rate — not the 10x that a contact-page-only benchmark
suggests — and dramatically cheaper as soon as a FREE-tier user wants their
emails verified, which we include.

The 56 domains that yielded nothing cost **$0.00** here; a per-page model
charges for them regardless.

## Reproducing

```bash
python benchmark/field_report.py --file <dataset export> --markdown
```

The sample lives in `field_sample_yc300.json` (and `.txt` for pasting into the
Console), so the same 300 domains can be re-run after any engine change.
