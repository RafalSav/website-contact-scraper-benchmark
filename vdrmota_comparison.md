# Website Contact & Email Scraper vs vdrmota/contact-info-scraper

Both Actors scraped the **same 28 start URLs, one page each** (our `maxContactPages=0`; vdrmota `maxRequestsPerStartUrl=1`, `useBrowser=false`) and are scored against the same independently hand-verified golden set. vdrmota is the category incumbent (12.6M+ total runs).

## Accuracy vs verified ground truth (micro-averaged)

| Field | Engine | Precision | Recall | F1 | TP | FP | FN |
|---|---|---|---|---|---|---|---|
| Emails | Website Contact & Email Scraper | 100.0% | 100.0% | 100.0% | 78 | 0 | 0 |
| Emails | vdrmota | 98.6% | 93.6% | 96.1% | 73 | 1 | 5 |
| Phones | Website Contact & Email Scraper | 100.0% | 100.0% | 100.0% | 13 | 0 | 0 |
| Phones | vdrmota | 100.0% | 0.0% | 0.0% | 0 | 0 | 13 |
| Socials | Website Contact & Email Scraper | 100.0% | 100.0% | 100.0% | 92 | 0 | 0 |
| Socials | vdrmota | 98.9% | 97.8% | 98.4% | 90 | 1 | 2 |

## Where the gap is widest: phone numbers

Our engine returns **clean E.164 numbers** (recall 100%, precision 100%). vdrmota returned **0 confident phone numbers total** across all 28 sites — it instead dropped 53 raw, unnormalized strings into a separate `phonesUncertain` bucket, mixing genuine numbers with garbage (e.g. `888 888 88888`, `3363 72867`) and leaving the user to sort E.164 formatting out by hand.

## Per-site detail

| Site | Emails (exp / ours / vdrmota) | Phones (exp / ours / vdrmota) | Socials (exp / ours / vdrmota) |
|---|---|---|---|
| www.fsf.org/about/contact | 2 / 2 / 2 | 0 / 0 / 0 | 0 / 0 / 0 |
| www.heise.de/impressum.html | 7 / 7 / 7 | 2 / 2 / 0 | 0 / 0 / 0 |
| www.python.org | 0 / 0 / 0 | 0 / 0 / 0 | 2 / 2 / 2 |
| apify.com | 0 / 0 / 0 | 0 / 0 / 0 | 4 / 4 / 4 |
| www.blender.org/about | 2 / 2 / 0 | 0 / 0 / 0 | 6 / 6 / 6 |
| www.eff.org/about/contact | 6 / 6 / 6 | 3 / 3 / 0 | 5 / 5 / 4 |
| www.gnu.org/contact | 8 / 8 / 8 | 0 / 0 / 0 | 0 / 0 / 0 |
| about.gitlab.com | 0 / 0 / 0 | 0 / 0 / 0 | 5 / 5 / 5 |
| www.mozilla.org/en-US/contact | 1 / 1 / 1 | 0 / 0 / 0 | 7 / 7 / 7 |
| www.torproject.org/contact | 3 / 3 / 3 | 0 / 0 / 0 | 5 / 5 / 5 |
| creativecommons.org/about/contac | 3 / 3 / 3 | 0 / 0 / 0 | 2 / 2 / 2 |
| www.debian.org/contact | 14 / 14 / 13 | 0 / 0 / 0 | 0 / 0 / 0 |
| signal.org | 1 / 1 / 0 | 0 / 0 / 0 | 2 / 2 / 2 |
| www.kernel.org/category/contact- | 1 / 1 / 1 | 1 / 1 / 0 | 0 / 0 / 0 |
| www.livechat.com/contact | 2 / 2 / 2 | 0 / 0 / 0 | 9 / 9 / 9 |
| www.cloudflare.com | 0 / 0 / 0 | 0 / 0 / 0 | 2 / 2 / 2 |
| www.docker.com | 0 / 0 / 1 | 0 / 0 / 0 | 6 / 6 / 7 |
| brand24.com/contact | 1 / 1 / 1 | 0 / 0 / 0 | 6 / 6 / 6 |
| nazwa.pl/kontakt | 2 / 2 / 2 | 2 / 2 / 0 | 3 / 3 / 3 |
| www.postgresql.org/about/contact | 5 / 5 / 5 | 0 / 0 / 0 | 0 / 0 / 0 |
| www.ietf.org/contact | 6 / 6 / 6 | 0 / 0 / 0 | 3 / 3 / 2 |
| www.mysql.com/about/contact | 0 / 0 / 0 | 5 / 5 / 0 | 4 / 4 / 4 |
| www.apache.org/foundation/contac | 3 / 3 / 3 | 0 / 0 / 0 | 3 / 3 / 3 |
| automattic.com/contact | 2 / 2 / 2 | 0 / 0 / 0 | 5 / 5 / 5 |
| www.php.net/contact | 3 / 3 / 3 | 0 / 0 / 0 | 0 / 0 / 0 |
| survicate.com/contact | 5 / 5 / 4 | 0 / 0 / 0 | 2 / 2 / 2 |
| callpage.io | 0 / 0 / 0 | 0 / 0 / 0 | 5 / 5 / 5 |
| tidio.com/contact | 1 / 1 / 1 | 0 / 0 / 0 | 6 / 6 / 6 |

_Ground truth built by reading each page's raw HTML by hand; both engines judged identically. Single-page scope keeps it apples-to-apples — neither engine was allowed to deep-crawl._
