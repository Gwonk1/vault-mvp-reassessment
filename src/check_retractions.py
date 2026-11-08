#!/usr/bin/env python3
"""Fail if a retracted claim appears without an inline retraction marker nearby.

Built after repeating the same documentation failure three times (#262, #283): a
retraction gets appended at the end of RESULTS.md while the original number stays
stated as live where a reader actually meets it. A house rule did not prevent the
third occurrence, so this is the mechanism instead. Run before any commit that
touches RESULTS.md, LEDGER.md or papers/.
"""
import re, sys, pathlib

WINDOW = 12         # lines either side that may carry the marker. Widened from 6 after the regex
                    # broadening (#328) showed a VOID banner sitting 8 lines above its own table rows
                    # — a marker immediately above a table must cover that table (#329).
MARKERS = re.compile(
    r'VOID|SUPERSEDED|WITHDRAWN|RETRACTED|STRUCK|\[FIXED\]|~~|corrected to|'
    r'wrong;|not valid|no longer|was wrong|overreach|degenerate|does not support|'
    r'but see|uninformative|by construction|we led with it|invalid|'
    # meta-discussion: text ABOUT the retraction machinery necessarily quotes the patterns
    r'planted|self-test|RETRACTIONS\.tsv|check_retractions|caught at the line|'
    # marking phrases found by the regex broadening itself (ledger #328)
    r'corrected|narrower than|first claimed|we first wrote|no support|overturn',
    re.I)
TARGETS = ['RESULTS.md', 'LEDGER.md', 'README.md',
           'papers/PAPER1_vault_reassessment.md', 'papers/PAPER2_bench_experiments.md']

def load_patterns(path='RETRACTIONS.tsv'):
    """Patterns are regexes. See the header of RETRACTIONS.tsv for why."""
    out = []
    for line in open(path):
        if line.startswith('#') or not line.strip(): continue
        f = line.rstrip('\n').split('\t')
        if len(f) >= 2: out.append((f[0], f[1], f[2] if len(f) > 2 else ''))
    return out



# ---------------------------------------------------------------------------
# Qualification check (added after the same failure was found in four separate
# documents: #262, #283, #319, #320). A retraction must be marked AT the line.
# A qualification is different: it qualifies a whole document, so a standing
# banner anywhere in the file satisfies it. What this catches is the error we
# made four times - a reframe landing in one document while every other document
# that asserts what it changed stays unqualified.
QUAL_TARGETS = TARGETS

def load_qualifications(path='QUALIFICATIONS.tsv'):
    out = []
    try:
        fh = open(path)
    except FileNotFoundError:
        return out
    for line in fh:
        if line.startswith('#') or not line.strip(): continue
        f = line.rstrip('\n').split('\t')
        if len(f) >= 3: out.append((f[0], f[1], f[2], f[3] if len(f) > 3 else ''))
    return out

def check_qualifications():
    quals = load_qualifications()
    if not quals: return 0, 0
    bad = []
    for t in QUAL_TARGETS:
        path = pathlib.Path(t)
        if not path.exists(): continue
        text = path.read_text()
        for pat, ctx, sec, note in quals:
            if pat not in text: continue
            if not re.search(ctx, text, re.I):
                n = text.count(pat)
                bad.append((t, pat, n, ctx, sec, note))
    if bad:
        print(f'\nFAIL: {len(bad)} document(s) assert a qualified claim without its standing context\n')
        for t, pat, n, ctx, sec, note in bad:
            print(f'  {t}')
            print(f'    asserts   : {pat!r} x{n}')
            print(f'    needs     : /{ctx}/  (established in section {sec})')
            print(f'    why       : {note}')
    return len(bad), len(quals)


def main():
    pats = load_patterns()
    violations = []
    for t in TARGETS:
        p = pathlib.Path(t)
        if not p.exists(): continue
        lines = p.read_text().split('\n')
        for i, line in enumerate(lines):
            for pat, by, note in pats:
                # patterns are REGEXES (ledger #327: five literal rewordings escaped the old version)
                try:
                    if not re.search(pat, line, re.I): continue
                except re.error:
                    if pat not in line: continue
                lo, hi = max(0, i - WINDOW), min(len(lines), i + WINDOW + 1)
                if not MARKERS.search('\n'.join(lines[lo:hi])):
                    violations.append((t, i + 1, pat, by, note, line.strip()[:90]))
    nq, qtot = check_qualifications()
    if not violations and not nq:
        print(f'OK: {len(pats)} retracted claims checked across {len(TARGETS)} documents; '
              f'every occurrence carries a retraction marker within {WINDOW} lines.')
        print(f'OK: {qtot} qualified claims checked; every document asserting one carries its '
              f'standing context.')
        return 0
    if nq and not violations:
        return 1
    print(f'FAIL: {len(violations)} occurrence(s) of a retracted claim with no nearby marker\n')
    for t, ln, pat, by, note, txt in violations:
        print(f'  {t}:{ln}')
        print(f'    pattern   : {pat!r}  (retracted by {by}{"; "+note if note else ""})')
        print(f'    line      : {txt}')
    return 1

if __name__ == '__main__':
    sys.exit(main())
