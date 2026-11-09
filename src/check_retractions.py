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
# Ledger #472: the +-WINDOW proximity test had a false-negative path. Two live instances of
# "99.99th percentile" in PAPER1 were cleared by the word "uninformative" twelve lines away,
# written about a DIFFERENT claim. A generic marker in the neighbourhood is not a retraction of
# the sentence in front of you. So markers are now split: STRONG ones clear by proximity (a VOID
# banner above a table must cover its rows, #329); everything else must sit in the SAME
# PARAGRAPH as the hit.
STRONG = re.compile(r'VOID|SUPERSEDED|WITHDRAWN|RETRACTED|STRUCK|\[FIXED\]|~~|'
                    r'RETRACTIONS\.tsv|check_retractions|planted|self-test', re.I)
MARKERS = re.compile(
    r'VOID|SUPERSEDED|WITHDRAWN|RETRACTED|STRUCK|\[FIXED\]|~~|corrected to|'
    r'wrong;|not valid|no longer|was wrong|overreach|degenerate|does not support|'
    r'but see|uninformative|by construction|we led with it|invalid|'
    # meta-discussion: text ABOUT the retraction machinery necessarily quotes the patterns
    r'planted|self-test|RETRACTIONS\.tsv|check_retractions|caught at the line|'
    # marking phrases found by the regex broadening itself (ledger #328)
    r'corrected|narrower than|first claimed|we first wrote|no support|overturn',
    re.I)
# Ledger #483: CALIBRATION.md - the ONE file written for strangers, and the only one a reuser is
# told to read first - was not in this list for the whole project. Neither were USEFULNESS.md or
# HYPOTHESES_AND_NOVELTY.md, both of which carry live claims. A gate pointed at the internal
# record and not at the exported document is pointed the wrong way.
TARGETS = ['RESULTS.md', 'LEDGER.md', 'README.md',
           'CALIBRATION.md', 'USEFULNESS.md', 'HYPOTHESES_AND_NOVELTY.md',
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



# ---------------------------------------------------------------------------
# Check 3: superseded result logs must carry a banner.
#
# We do NOT run the retraction patterns over results/*.log. Those patterns are
# bare decimals (0.184, 0.0526, 0.174) and logs are dense with unrelated floats,
# so they cannot discriminate: of six hits in results/, three were genuine void
# values and three were coincidences (a null_sd that happens to equal 0.174, a
# model CI bound of 0.0526, a Spearman rho of 0.1842505...).
#
# And the obvious fix INVERTS the outcome. Adding (?!\d) so a pattern stops
# matching the prefix of a longer float would suppress the two GENUINE hits
# (p=0.18352908..., p=0.05261473...) while keeping both coincidental short
# floats. A prose instrument does not become a numeric one by tightening it.
#
# So logs are gated on a tractable property instead: a log known to be
# superseded must say so at the top. Add to SUPERSEDED_LOGS when a rerun
# invalidates a stored log, and stamp the file.
# ---------------------------------------------------------------------------
SUPERSEDED_LOGS = {
    'results/donor_and_k.log': '#243 frame-order index bug; TEST 2 also superseded by §64c',
    'results/export_test.log': '§63 degenerate three-way matcher voids every matched p-value',
    # JSON twins of the two logs above. JSON takes no comment, so the banner lives
    # in a '_superseded' key whose value opens with the same marker text. Found only
    # because the logs' fix prompted a sweep of every tracked non-document file (§78).
    'results/donor_and_k.json': 'machine-readable twin: ratio 2.4813 / 65 cells / 189 donors, all pre-fix',
    'results/export_test.json': 'machine-readable twin: p=0.18352908 and gate1=true from the degenerate matcher',
}
BANNER = 'SUPERSEDED OUTPUT'

def check_superseded_logs():
    missing = []
    for path, why in sorted(SUPERSEDED_LOGS.items()):
        fp = pathlib.Path(path)
        if not fp.exists():
            missing.append((path, why, 'FILE MISSING'))
        elif BANNER not in fp.read_text(errors='replace'):
            missing.append((path, why, f'no {BANNER!r} banner'))
    if missing:
        print(f'FAIL: {len(missing)} superseded result log(s) not stamped\n')
        for path, why, problem in missing:
            print(f'  {path}')
            print(f'    reason   : {why}')
            print(f'    problem  : {problem}')
    return len(missing), len(SUPERSEDED_LOGS)

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
                if STRONG.search('\n'.join(lines[lo:hi])): continue
                # weak marker: must be in the same blank-line-delimited paragraph
                pstart = i
                while pstart > 0 and lines[pstart - 1].strip(): pstart -= 1
                pend = i
                while pend < len(lines) - 1 and lines[pend + 1].strip(): pend += 1
                if not MARKERS.search('\n'.join(lines[pstart:pend + 1])):
                    violations.append((t, i + 1, pat, by, note, line.strip()[:90]))
    nq, qtot = check_qualifications()
    ns, stot = check_superseded_logs()
    if not violations and not nq and not ns:
        print(f'OK: {len(pats)} retracted claims checked across {len(TARGETS)} documents; '
              f'every occurrence carries a STRONG marker within {WINDOW} lines or a weaker one '
              f'in the same paragraph.')
        print(f'OK: {qtot} qualified claims checked; every document asserting one carries its '
              f'standing context.')
        print(f'OK: {stot} superseded result log(s) checked; each carries its '
              f'{BANNER!r} banner.')
        return 0
    if (nq or ns) and not violations:
        return 1
    print(f'FAIL: {len(violations)} occurrence(s) of a retracted claim with no nearby marker\n')
    for t, ln, pat, by, note, txt in violations:
        print(f'  {t}:{ln}')
        print(f'    pattern   : {pat!r}  (retracted by {by}{"; "+note if note else ""})')
        print(f'    line      : {txt}')
    return 1

if __name__ == '__main__':
    sys.exit(main())
