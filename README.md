# Website contact scraper benchmark

Reproducible measurements for the boring question nobody in this category
answers with numbers: **on a list of company websites you did not curate, how
many domains actually give you a contact, and what does that cost?**

Contact and email scrapers are sold on adjectives. This repository holds the
data behind three measurements, so anyone can check or repeat them:

| File | Question it answers |
|---|---|
| [`golden_set.json`](golden_set.json) | **Accuracy.** 32 real pages whose emails, phones and social profiles were read out of the raw HTML by hand. Ground truth, not a sample of somebody's output. |
| [`field_report_yc300.md`](field_report_yc300.md) | **Yield.** 300 random Y Combinator companies, sampled before anything was run against them. |
| [`head_to_head_yc150.md`](head_to_head_yc150.md) | **Comparison.** The same 150 domains through two scrapers on the same day, at comparable crawl depth, with the cost each one billed. |
| [`field_sample_de150.json`](field_sample_de150.json) · [`head_to_head_de150.md`](head_to_head_de150.md) | **The same comparison on German domains** — 150 random `.de` names from the Tranco list, where the result is less flattering and published anyway. |
| [`vdrmota_comparison.md`](vdrmota_comparison.md) | Per-field accuracy of the same two scrapers against the golden set. |

## What the numbers say

On 150 identical, uncurated startup domains, both scrapers in the Apify cloud
on September 24, 2026:

| Metric | This engine | Category incumbent |
|---|---|---|
| Domains with an email | **76.0%** | 53.3% |
| Emails found | **204** | 123 |
| Domains with a usable phone | **11** | 4 confident, 36 unnormalized |
| Cost of the run | **$0.95** | $1.04 |
| **Cost per email found** | **$0.0046** | $0.0084 |

On 36 domains only this engine returned an address; the reverse happened twice.

On 150 random German domains the same day, this engine found an email on more
of them (64.7% against 56.7%) and a usable phone on far more (91 against 37) —
but cost more per domain ($0.015 against $0.006), because German legal pages
publish many contacts and it bills per contact where the incumbent bills per
page. Both results are here; neither is the whole story alone.

Three findings from the 300-domain field test are worth more than the totals:

1. **A privacy policy is a contact page.** Any site subject to GDPR has to
   publish a reachable data-controller contact, so a startup with nothing but a
   contact form still has an address on `/privacy`. Crawling legal pages as a
   fallback moved email coverage from 60.7% to **73.3%** — the single largest
   gain measured here.
2. **A browser is worth less than it looks, but not nothing.** Re-running only
   the 56 domains that yielded nothing, with JavaScript rendering on, recovered
   **24 of them (43%)** for 7% of the run's cost. The remaining 32 publish no
   contact at all.
3. **Dates parse as phone numbers.** German datelines (`20.2.2026`) are valid
   `+49` numbers once the separators go, so an article archive yields a page of
   invented numbers. Any phone extraction over free text needs a date filter —
   this was found by running the engine against `heise.de` and reading every
   number it returned.
4. **A legal page names contacts that are not the site's.** German privacy
   policies must name the data protection authority a visitor can complain to,
   with its address, email and phone; on 150 random German domains 12 records
   carried a supervisory authority's inbox, and on 4 it was the "best" email.
   US terms pages print a California consumer-complaint line the same way.

## Method

- **Golden set.** Each page was fetched as raw HTML and read by hand; whatever a
  human could prove was there became the label. Labels include contacts hidden
  behind Cloudflare's `data-cfemail`, HTML entities, `name [at] domain`
  obfuscation and JSON-LD, because those are on the page whether or not a
  scraper can see them. Notes on every entry record what makes it interesting
  and when it was verified.
- **Field sample.** 300 companies drawn with `random.seed(42)` from the public
  Y Combinator API, before any run. The full list is in
  [`field_sample_yc300.json`](field_sample_yc300.json) so the sample can be
  re-drawn and the result checked.
- **German sample.** 150 `.de` names drawn with `random.seed(42)` from the
  Tranco top-1M list (`field_sample_de150.md` has the exact recipe) — a
  popularity sample, so it includes names with no website behind them.
- **Head-to-head.** Both scrapers were given the same 150 domains on the same
  day, with the incumbent configured to crawl at least as deep (in September it
  was charged for 516 pages against our 391). Costs are the amounts each run actually billed, not
  list prices. Caveat stated plainly: this is one sample of one population
  (YC startups), and the incumbent was run without its paid add-ons — browser
  rendering, email verification and enrichment are real features that cost extra
  and were not bought.
- **Scoring.** [`head_to_head_yield.py`](head_to_head_yield.py) takes the two
  dataset exports and produces the comparison table. It reads exports, not the
  engine, so it works on any scraper's output. The exports themselves are not
  published: they hold real people's names and addresses.

## Reproducing it

```bash
# export both runs from the Apify Console (Storage -> Export -> JSON), then:
python head_to_head_yield.py --ours ours.json --theirs theirs.json
```

The extraction engine these numbers came from is not in this repository — it is
published as an Apify Actor:
[Website Contact & Email Scraper](https://apify.com/sandy_yclept/website-contact-email-scraper),
and a German-market variant,
[Impressum Email Scraper](https://apify.com/sandy_yclept/impressum-email-scraper).
The data and the scoring scripts are here so the claims can be audited without
taking anyone's word for them.

Corrections are welcome: if a label in `golden_set.json` is wrong, open an issue
with the page and what it should say. Several labels have already been fixed
that way — including a few where the engine was right and the human was not.

## Licence

MIT for the code, CC0 for the labels and the sample list.
