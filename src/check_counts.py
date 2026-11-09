#!/usr/bin/env python3
"""CHECK 5: every count stated in prose must match the thing it counts.

Ledger #482: README claimed 264 ledger entries, 63 RESULTS sections, 44
preregistrations, "the ten house rules" and "Fourteen" experiments, against
actual 478 / 103 / 49 / 19 / 15. PAPER1 claimed "452 entries, ids 1-454" and
"RESULTS.md (24 sections)". #358 had ALREADY corrected a count that was being
"incremented instead of counted" - and it recurred anyway, because a number
maintained by hand next to a file that grows is a number that drifts.

The fix is not care. It is this file. Run it before every commit; it recomputes
each count and fails on any prose figure that no longer matches.
"""
import re, sys, pathlib

def counts():
    led = pathlib.Path('LEDGER.md').read_text()
    # Three rows carry LETTER-SUFFIXED ids (13a, 26b, 34b), so "number of rows" and
    # "number of numeric ids" are two different counts and were being conflated.
    rows = re.findall(r'^\| (\d+) \|', led, re.M)
    suffixed = re.findall(r'^\| (\d+[a-z]) \|', led, re.M)
    ids = sorted(int(x) for x in rows)
    res = pathlib.Path('RESULTS.md').read_text()
    con = pathlib.Path('CONTRIBUTING.md').read_text()
    p2  = pathlib.Path('papers/PAPER2_bench_experiments.md').read_text()
    retr = [l for l in pathlib.Path('RETRACTIONS.tsv').read_text().splitlines()
            if l.strip() and not l.startswith('#')]
    qual = [l for l in pathlib.Path('QUALIFICATIONS.tsv').read_text().splitlines()
            if l.strip() and not l.startswith('#')]
    return {
        'ledger_rows':      len(ids) + len(suffixed),
        'ledger_numeric':   len(ids),
        'ledger_suffixed':  len(suffixed),
        'ledger_max':       max(ids),
        'ledger_struck': sum(1 for l in led.splitlines()
                             if re.match(r'^\| \d+[a-z]? \|', l) and '~~' in l),
        'results_sections': len(re.findall(r'^## \d+\.', res, re.M)),
        'house_rules':   max(int(m) for m in re.findall(r'^#+ (\d+)\.', con, re.M)),
        'preregs':       len(list(pathlib.Path('.').glob('*PREREGISTRATION*.md'))),
        'experiments':   len(re.findall(r'^### \d+\. ', p2, re.M)),
        'retractions':   len(retr),
        'qualifications':len(qual),
        'audits':        len(list(pathlib.Path('grok/from-grok').glob('*.md'))),
    }

# (file, regex capturing ONE number, which count it must equal)
CLAIMS = [
    ('RESULTS.md',  r'\*\*(\d+) ledger rows\*\*',                        'ledger_rows'),
    ('RESULTS.md',  r'\*\*(\d+) with numeric ids 1-\d+\*\*',             'ledger_numeric'),
    ('RESULTS.md',  r'numeric ids 1-(\d+)\*\*',                          'ledger_max'),
    ('RESULTS.md',  r'\*\*(\d+) letter-suffixed\*\*',                    'ledger_suffixed'),
    ('RESULTS.md',  r'\*\*(\d+) carrying a strikethrough\*\*',           'ledger_struck'),
    ('RESULTS.md',  r'\*\*(\d+) numbered sections\*\* here',             'results_sections'),
    ('RESULTS.md',  r'\*\*(\d+) pre-registrations\.\*\*',                'preregs'),
    ('RESULTS.md',  r'\*\*(\d+) house rules\*\*',                        'house_rules'),
    ('RESULTS.md',  r'\*\*(\d+) registered retraction patterns\*\*',     'retractions'),
    ('RESULTS.md',  r'\*\*(\d+) standing qualifications\*\*',            'qualifications'),
    ('README.md',   r'Of \*\*(\d+)\*\* ledger',                          'ledger_rows'),
    ('README.md',   r'\*\*(\d+) rows\*\* \(\d+ numeric',                  'ledger_rows'),
    ('README.md',   r'\*\*(\d+) carry a strikethrough\*\*',              'ledger_struck'),

    ('README.md',   r'\*\*(\d+) numbered sections\*\*',                  'results_sections'),
    ('README.md',   r'\*\*(\d+) house rules\*\*',                        'house_rules'),
    ('README.md',   r'The (\d+) house rules in',                         'house_rules'),
    ('README.md',   r'\*\*(\d+) files\*\*: the predictions',             'preregs'),
    ('papers/PAPER1_vault_reassessment.md',
                    r'\*\*(\d+) rows\*\*: \d+ numeric',                  'ledger_rows'),
    ('papers/PAPER1_vault_reassessment.md',
                    r'\*\*(\d+) numbered sections\*\*',                  'results_sections'),
]

def main():
    c = counts()
    bad = []
    checked = 0
    for f, rx, key in CLAIMS:
        txt = pathlib.Path(f).read_text()
        for m in re.finditer(rx, txt):
            checked += 1
            stated = int(m.group(1))
            if stated != c[key]:
                line = txt[:m.start()].count('\n') + 1
                bad.append((f, line, key, stated, c[key], m.group(0)))
    print('  computed: ' + ', '.join(f'{k}={v}' for k, v in sorted(c.items())))
    if not bad:
        print(f'  OK: {checked} stated counts match what they count.')
        return 0
    print(f'FAIL: {len(bad)} stated count(s) no longer match:\n')
    for f, line, key, stated, actual, frag in bad:
        print(f'  {f}:{line}\n    {key}: prose says {stated}, actual {actual}\n'
              f'    matched: {frag!r}\n')
    print('  Update the prose, or add the new claim site to CLAIMS in this file.')
    return 1

if __name__ == '__main__':
    sys.exit(main())
