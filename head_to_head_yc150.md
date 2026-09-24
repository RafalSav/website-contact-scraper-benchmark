# Head-to-head on an uncurated list — 150 identical domains

Both Actors, same 150 domains, same day. The list is a random sample (seed 42)
of Y Combinator companies pulled from their public API — picked before either
Actor saw it, and deliberately unglamorous: modern startup sites, mostly
Framer/Next.js, many with a contact form instead of a published address.

This measures **yield**, not accuracy: how many domains each Actor turns into a
usable contact, and what that costs. For accuracy against hand-verified labels
see `vdrmota_comparison.md` and `golden_set.json`. The same comparison on
German domains is in `head_to_head_de150.md`.

## September 2026 re-run

Both Actors in the Apify cloud on September 24, 2026, same configuration as in
July (below): ours build 0.2.23 at `maxContactPages: 3`, theirs at
`maxRequestsPerStartUrl: 4` through Apify Proxy, no browser for either. We read
391 pages, they were charged for 516.

| Metric | This Actor | Incumbent |
|---|---|---|
| Domains with an email | **114 (76.0%)** | 80 (53.3%) |
| Domains with a phone | **11 (7.3%)** | 4 (2.7%) confident, plus 36 unnormalized |
| Domains with a social profile | 103 (68.7%) | 102 (68.0%) |
| Unique emails found | **204** | 123 |
| Domains where only this Actor found an email | **36** | 2 |
| Charged for the run | **$0.945** | $1.036 |
| **Per email found** | **$0.0046** | $0.0084 |

Between the runs the engine learned to leave out contacts that are not the
site's: the California consumer-complaint line on US terms pages, sample
customers on demo pages, authorities named on legal pages. That is why phones
are now counted per domain with a usable number, and why one number in July's
table below needs a footnote.

## July 2026 (first run)

### Configuration

| | This Actor | Incumbent (`vdrmota/contact-info-scraper`) |
|---|---|---|
| Depth | `maxContactPages: 3` (homepage + up to 3 subpages) | `maxRequestsPerStartUrl: 4` |
| Browser | off | `useBrowser: false` |
| Proxy | none | Apify Proxy (its input requires one) |
| Pages actually fetched | 370 | 484 |

The incumbent fetched *more* pages than we did, so the comparison does not
favour us on depth.

### Results

| Metric | This Actor | Incumbent |
|---|---|---|
| Domains with an email | **110 (73.3%)** | 81 (54.0%) |
| Domains with a phone | **12 (8.0%)**¹ | 4 (2.7%) confident, plus 38 unnormalized |
| Domains with a social profile | 98 (65.3%) | 99 (66.0%) |
| Unique emails found | **192** | 117 |
| Domains where only one Actor found an email | **30 (ours)** | 1 (theirs) |

### Cost, measured not estimated

| | Cost for these 150 domains |
|---|---|
| This Actor (pay per result) | **$0.886** |
| Incumbent (pay per page, actual run charge) | $0.972 |
| Per domain | **$0.0059** vs $0.0065 |
| **Per email actually found** | **$0.0046** vs $0.0083 |

We are cheaper *and* find more, which is the opposite of what a contact-page
benchmark predicts. The reason is structural: a per-page model bills for every
page it opens, including the 46% of domains where it finds no email, while we
bill only for results. Deep crawling is free to the buyer here and expensive
there.

### Honest caveats

- One sample, 150 domains, one industry slice (YC startups). Yield on lawyers,
  restaurants or German Mittelstand will differ for both Actors.
- The incumbent was run without its paid extras (browser rendering, email
  verification, lead enrichment). Those add capability we do not have — and
  cost extra on top of the figures above.
- Social profiles are a tie; the gap is in emails and in usable phone numbers.
- Our figures come from build 0.2.13, which crawls privacy/terms pages. That
  single change is worth roughly twelve percentage points of email coverage.

### Reproducing

```bash
python benchmark/head_to_head_yield.py --ours ours.json --theirs theirs.json
```

The domain list is `field_sample_yc300.json` (first 150 entries).

¹ Re-running the July engine over the same pages in September showed the
California consumer-complaint line - printed on many US terms pages - on 3 of
its 15 phone domains, 2 of them with no other number: roughly 10 of the 12 were
the startups' own. The engine has not counted that line since September.
