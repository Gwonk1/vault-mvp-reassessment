#!/usr/bin/env python3
"""Fail if a retracted claim appears without an inline retraction marker nearby.

Built after repeating the same documentation failure three times (#262, #283): a
retraction gets appended at the end of RESULTS.md while the original number stays
stated as live where a reader actually meets it. A house rule did not prevent the
third occurrence, so this is the mechanism instead. Run before any commit that
touches RESULTS.md, LEDGER.md or papers/.
"""
import re, sys, pathlib

WINDOW = 6          # lines either side that may carry the marker
MARKERS = re.compile(
    r'VOID|SUPERSEDED|WITHDRAWN|RETRACTED|STRUCK|\[FIXED\]|~~|corrected to|'
    r'wrong;|not valid|no longer|was wrong|overreach|degenerate|does not support|'
    r'but see|uninformative|by construction|we led with it|invalid',
    re.I)
TARGETS = ['RESULTS.md', 'LEDGER.md', 'README.md',
           'papers/PAPER1_vault_reassessment.md', 'papers/PAPER2_bench_experiments.md']

def load_patterns(path='RETRACTIONS.tsv'):
    out = []
    for line in open(path):
        if line.startswith('#') or not line.strip(): continue
        f = line.rstrip('\n').split('\t')
        if len(f) >= 2: out.append((f[0], f[1], f[2] if len(f) > 2 else ''))
    return out

def main():
    pats = load_patterns()
    violations = []
    for t in TARGETS:
        p = pathlib.Path(t)
        if not p.exists(): continue
        lines = p.read_text().split('\n')
        for i, line in enumerate(lines):
            for pat, by, note in pats:
                if pat not in line: continue
                lo, hi = max(0, i - WINDOW), min(len(lines), i + WINDOW + 1)
                if not MARKERS.search('\n'.join(lines[lo:hi])):
                    violations.append((t, i + 1, pat, by, note, line.strip()[:90]))
    if not violations:
        print(f'OK: {len(pats)} retracted claims checked across {len(TARGETS)} documents; '
              f'every occurrence carries a retraction marker within {WINDOW} lines.')
        return 0
    print(f'FAIL: {len(violations)} occurrence(s) of a retracted claim with no nearby marker\n')
    for t, ln, pat, by, note, txt in violations:
        print(f'  {t}:{ln}')
        print(f'    pattern   : {pat!r}  (retracted by {by}{"; "+note if note else ""})')
        print(f'    line      : {txt}')
    return 1

if __name__ == '__main__':
    sys.exit(main())
