# Head-to-head on German domains — 150 identical domains

The same comparison as `head_to_head_yc150.md`, on the kind of site the
Impressum listing is sold for. The domains are `field_sample_de150.json`: 150
random `.de` names from the Tranco top-1M list (seed 42, below rank 10,000;
`field_sample_de150.md` says how they were drawn). They were picked before
either Actor saw them and are a popularity sample, not a register of companies:
shops and firms, but also associations, public bodies, publishers and names with
no website at all.

## Configuration

Both Actors in the Apify cloud on September 24, 2026.

| | This Actor | Incumbent (`vdrmota/contact-info-scraper`) |
|---|---|---|
| Build | 0.2.23 | 0.2.237 |
| Depth | `maxContactPages: 3` (homepage + up to 3 subpages) | `maxRequestsPerStartUrl: 4` |
| Phone region | `DE` | — |
| Browser | off | `useBrowser: false` |
| Proxy | none | Apify Proxy (its input requires one) |
| Pages read / charged | 387 read | 466 charged |

## Results

| Metric | This Actor | Incumbent |
|---|---|---|
| Domains with an email | **97 (64.7%)** | 85 (56.7%) |
| Unique emails found | **330** | 239 |
| Domains with a usable phone | **91 (60.7%)** | 37 (24.7%) confident, plus 112 unnormalized |
| Domains with a social profile | 76 (50.7%) | **80 (53.3%)** |
| Domains where only this Actor / only the incumbent found an email | **25** | 13 |
| Charged for the run | $2.182 | **$0.936** |
| Per domain | $0.0145 | **$0.0062** |
| Per email found | $0.0066 | **$0.0039** |

We also return 54 fax numbers apart from the phones, uncharged; the incumbent
has no such distinction, so its phone columns may contain faxes.

## Reading it

- **Coverage and phones favour this Actor; price per domain favours the
  incumbent.** An Impressum publishes many contacts - address, phone, fax,
  several inboxes - and this Actor bills per contact where the incumbent bills
  per page. On lists of German companies it costs more per domain, and it should
  not be sold as cheaper there.
- **The 13 domains only the incumbent answered for** break down as: 4 parked or
  spam pages whose "contact" is a domain broker's or a link seller's address
  (`domain@kv-gmbh.de`, `links@nextbacklinks.com`); 5 whose pages our cloud run
  could not read, where the incumbent's proxy got through; 1 whose robots.txt
  forbids its Impressum, which we respect; and 3 real gaps of ours - two sites
  that redirect to another domain (online-tis.de to iisii.de, arbeitsamt.de to
  arbeitsagentur.de), where we stop before the contact pages, and
  bridge-verband.de, whose address sits on a fourth contact page, past our three.
  The redirects were fixed the same evening: build 0.2.27 follows a site to the
  front page of the domain it moved to, and in the cloud both now return their
  contacts (`zentrale@arbeitsagentur.de`, `info@online-tis.de`). The table above is still
  build 0.2.23's.
- **At the listing's default of 6 subpages** the same 150 domains cost $2.91
  ($0.019 per domain) for 482 emails on the same 97 domains - more contacts per
  site, not more sites.

## A first run the same day

Earlier on September 24 the same comparison ran on build 0.2.22 and came out
level on email coverage, 57.3% against 56.7%. Of the 20 domains only the
incumbent answered for, 14 were ones we never read: bare domain names that only
answer as `www.` or over plain http, and sites that refused our old,
bot-shaped user agent. Build 0.2.23 tries the other spellings of a host and
sends a browser-shaped agent that still names this Actor; unreachable domains
went from 47 to 33, and the table above is that build.

## Honest caveats

- One sample of 150, drawn from a popularity list; results on a list of real
  German companies will be higher for both Actors, since fewer names will be
  dead.
- The incumbent ran through Apify Proxy, we did not. Its proxy got it into two
  sites that block cloud addresses; turning ours on is one setting.
- The incumbent was run without its paid extras (browser, email verification,
  lead enrichment).
- Cost is what each Actor charged a Free-plan account for the run.

## Reproducing

The inputs above plus the domain list reproduce the runs. The exports are not
published: they hold the names and addresses of real people, which is not ours
to redistribute. Score any two exports with:

```bash
python benchmark/head_to_head_yield.py --ours ours.json --theirs theirs.json
```
