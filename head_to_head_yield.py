#!/usr/bin/env python
"""Head-to-head *yield* on an uncurated list — both Actors, identical domains.

`run_vdrmota.py` scores both engines against hand-verified labels; that measures
accuracy on pages we already know the answer for. This measures the other half:
run both over a list nobody curated and count how many domains each one turns
into a usable contact. No ground truth is needed — a domain either yielded an
address or it did not.

Usage:
    python benchmark/head_to_head_yield.py --ours ours.json --theirs theirs.json
"""

from __future__ import annotations

import argparse
import json
import re
from urllib.parse import urlsplit

# Their dataset spreads socials across one key per platform.
THEIR_SOCIAL_KEYS = ('linkedIns', 'twitters', 'instagrams', 'facebooks', 'youtubes', 'tiktoks')
# …and phone numbers across a confident and an uncertain bucket.
THEIR_PHONE_KEYS = ('phones', 'phonesUncertain')

_E164 = re.compile(r'^\+\d{7,15}$')


def host(url: str) -> str:
    netloc = urlsplit(url if '://' in url else f'//{url}').netloc.lower()
    return netloc.removeprefix('www.').split(':')[0]


def load(path: str) -> list[dict]:
    text = open(path, encoding='utf-8').read().strip()
    text = text[text.index('['):] if text.lstrip().startswith(('{"data"', 'application/json')) else text
    if text.startswith('['):
        return json.loads(text)
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def ours_by_host(items: list[dict]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for r in items:
        h = host(r.get('domain', ''))
        emails = {e['email'].lower() for e in (r.get('emails') or [])}
        phones = set(r.get('phones') or [])
        socials = {u for v in (r.get('socials') or {}).values() for u in v}
        cur = out.setdefault(h, {'emails': set(), 'phones': set(), 'socials': set()})
        cur['emails'] |= emails
        cur['phones'] |= phones
        cur['socials'] |= socials
    return out


def theirs_by_host(items: list[dict]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for r in items:
        url = r.get('url') or r.get('originalUrl') or r.get('domain') or ''
        h = host(url)
        if not h:
            continue
        cur = out.setdefault(h, {'emails': set(), 'phones': set(), 'socials': set(),
                                 'phones_uncertain': set()})
        cur['emails'] |= {e.lower() for e in (r.get('emails') or []) if '@' in e}
        cur['phones'] |= set(r.get('phones') or [])
        cur['phones_uncertain'] |= set(r.get('phonesUncertain') or [])
        for k in THEIR_SOCIAL_KEYS:
            cur['socials'] |= set(r.get(k) or [])
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--ours', required=True)
    ap.add_argument('--theirs', required=True)
    args = ap.parse_args()

    ours, theirs = ours_by_host(load(args.ours)), theirs_by_host(load(args.theirs))
    domains = sorted(set(ours) | set(theirs))
    n = len(domains)

    def count(src: dict, field: str) -> int:
        return sum(1 for d in domains if src.get(d, {}).get(field))

    o_mail, t_mail = count(ours, 'emails'), count(theirs, 'emails')
    o_phone, t_phone = count(ours, 'phones'), count(theirs, 'phones')
    o_soc, t_soc = count(ours, 'socials'), count(theirs, 'socials')
    t_phone_unc = sum(1 for d in domains if theirs.get(d, {}).get('phones_uncertain'))

    o_only = [d for d in domains if ours.get(d, {}).get('emails') and not theirs.get(d, {}).get('emails')]
    t_only = [d for d in domains if theirs.get(d, {}).get('emails') and not ours.get(d, {}).get('emails')]

    def p(k: int) -> str:
        return f'{k} ({k / n * 100:.1f}%)' if n else '—'

    print(f'\n# Yield head-to-head — {n} identical domains\n')
    print('| Metric | This Actor | Incumbent |')
    print('|---|---|---|')
    print(f'| Domains with an email | **{p(o_mail)}** | {p(t_mail)} |')
    print(f'| Domains with a phone | **{p(o_phone)}** | {p(t_phone)} confident'
          f' (+{t_phone_unc} unnormalized) |')
    print(f'| Domains with a social profile | {p(o_soc)} | {p(t_soc)} |')
    print(f'| Unique emails found | {sum(len(v["emails"]) for v in ours.values())} | '
          f'{sum(len(v["emails"]) for v in theirs.values())} |')
    print()
    print(f'- Domains where **only we** found an email: **{len(o_only)}**')
    print(f'- Domains where **only they** found an email: **{len(t_only)}**')
    if o_only:
        print(f'\nOnly ours (first 10): {", ".join(o_only[:10])}')
    if t_only:
        print(f'Only theirs (first 10): {", ".join(t_only[:10])}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
