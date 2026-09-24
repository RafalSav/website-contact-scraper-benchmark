# Google Maps field sample — 128 local businesses

`field_sample_maps128.json` is the list a lead-generation buyer actually brings:
the websites of local businesses found on Google Maps. It is where the regulated
professions are — lawyers, dentists, tax advisers, estate agents — and with them
the chambers and licensing authorities their legal pages must name, which the two
other samples barely contain. It is used to measure what the engine returns on
small-business sites and to compare engine versions.

## How it was drawn

On 2026-09-24, `compass/crawler-google-places` took up to the first 8 Google Maps
results for five lead-generation categories in four cities — dentist, plumber,
lawyer, estate agent and accountant, searched in the local language, around
Chicago, Manchester, Köln and Kraków. 136 places came back, 130 with a website;
with tracking parameters stripped and duplicates merged, the 128 websites the
engine was then run on form the sample. Each entry carries the search term and
city it came from, and the `phoneRegion` of its country, so that local-format
numbers are read as that country's.

## What it is and is not

The top of Google Maps, not a random draw of businesses: chains and firms that
invest in their listing are over-represented (reedsrains.co.uk publishes 101
addresses). A fair test of precision on small-business sites and of what a Maps
lead list costs; not a yield estimate for any other kind of list.
