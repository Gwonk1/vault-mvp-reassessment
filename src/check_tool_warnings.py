#!/usr/bin/env python3
"""Check 4: did we READ what our own tools printed?

Exists because codeml printed 'This is a rooted tree. Please check!' and 'ntime: 24'
in a file we never opened, and an external auditor found the fault from arithmetic
alone (RESULTS.md 101a). Every other gate in this repo checks a claim against data.
None checked whether the tool had already told us we were wrong.
"""
import re, sys, pathlib

# Strings that mean a tool is telling you something. Deliberately broad: a false
# alarm costs an annotation, a miss costs a published result.
PATTERNS = [
    r'[Pp]lease check',
    r'\bWARNING\b', r'\bwarning:',
    r'\bERROR\b', r'\berror:',
    r'\bFAIL(?:ED|URE)?\b',
    r'rooted tree',
    r'not converged|convergence (?:problem|failed)',
    r'singular|unidentifiab\w+',
    r'[Tt]raceback',
    r'NaN|[-+]?nan\b',
    r'deprecat\w+',
    r'truncat\w+',
    r'\bskipp?(?:ed|ing)\b',
]
RX = re.compile('|'.join(PATTERNS))
# An annotation anywhere in the same file that shows the line was read and judged.
SEEN = re.compile(r'READ:|ACKNOWLEDGED|EXPECTED|benign|harmless|see RESULTS|SUPERSEDED|'
                  r'by design|not a fault|VOID|accounted for', re.I)

ROOTS = [pathlib.Path('results'),
         pathlib.Path('/tmp/claude-1000/-home-graham-projects/'
                      '46738ac0-1f6d-4b80-81fe-caa9aa37b1a5/scratchpad/t0')]
EXTS = {'.log', '.txt', '.out'}

# Ledger #468: six codeml output files sat in the repository ROOT for a day without
# this check ever seeing them, for two independent reasons - the root was not a scan
# root, and PAML writes its defaults with NO EXTENSION, so the EXTS filter would have
# skipped them anyway. Both are fixed here. A tool-output filter that assumes an
# extension is a filter that misses every tool whose convention is a bare name.
BARE = {'mlc', 'rst', 'rst1', 'rub', 'lnf', '2NG.dN', '2NG.dS', '2NG.t', 'rates'}
ROOT_TOP = pathlib.Path('.')   # top level only: results/ is already a root above

def candidates():
    """Every file this check should read, from the recursive roots plus the
    repository top level (where a tool run in the wrong directory lands)."""
    for root in ROOTS:
        if not root.exists(): continue
        for f in sorted(root.rglob('*')):
            if f.is_file() and f.suffix in EXTS: yield f
    for f in sorted(ROOT_TOP.iterdir()):
        if f.is_file() and (f.suffix in EXTS or f.name in BARE): yield f

def main():
    hits=[]; scanned=0
    for f in candidates():
        if f.stat().st_size > 4_000_000: continue
        try: txt=f.read_text(errors='replace')
        except Exception: continue
        scanned+=1
        acked = bool(SEEN.search(txt))
        for i,line in enumerate(txt.splitlines(),1):
            m=RX.search(line)
            if m and not acked:
                hits.append((f, i, m.group(0), line.strip()[:96]))
    print(f'  scanned {scanned} tool-output files under {len(ROOTS)} roots + the repository top level')
    if not hits:
        print(f'  OK: no unacknowledged tool warnings.')
        return 0
    byfile={}
    for f,i,k,l in hits: byfile.setdefault(f,[]).append((i,k,l))
    print(f'  {len(hits)} unacknowledged warning line(s) in {len(byfile)} file(s):\n')
    for f,rows in list(byfile.items())[:14]:
        print(f'  {f}')
        for i,k,l in rows[:4]: print(f'    {i:>5}: [{k}] {l}')
        if len(rows)>4: print(f'          ... {len(rows)-4} more')
    if len(byfile)>14: print(f'  ... {len(byfile)-14} more files')
    print('\n  Annotate each file with READ: <what it means> once judged, or fix the cause.')
    return 1

if __name__=='__main__':
    sys.exit(main())
