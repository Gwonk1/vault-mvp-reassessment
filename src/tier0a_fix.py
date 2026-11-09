#!/usr/bin/env python3
"""Rerun the branch test with an UNROOTED tree, and leave-one-out without Branchiostoma.
codeml printed 'This is a rooted tree. Please check!' on the original run and fit 24 branch
lengths where an unrooted 13-taxon tree has 23 - with the foreground sitting at the
unidentifiable root. Grok audit 010 flagged the arithmetic; the warning was in our own output."""
import pathlib, subprocess, re
from scipy.stats import chi2
S=pathlib.Path('/tmp/claude-1000/-home-graham-projects/46738ac0-1f6d-4b80-81fe-caa9aa37b1a5/scratchpad/t0')
V="(((((human,(rat,rabbit)),(dog,horse)),(cow,sheep)),opossum),(chicken,(xenopus,zebrafish)))"

def phy(names, src=S/'deep.phy'):
    """Rewrite the phylip keeping only `names`."""
    lines=src.read_text().split('\n')
    rows=[l for l in lines[1:] if l.strip()]
    keep=[r for r in rows if r.split()[0] in names]
    ncod=len(keep[0].split()[1])
    out=S/f"sub_{'_'.join(sorted(names))[:40]}.phy"
    out.write_text(f" {len(keep)} {ncod}\n" + '\n'.join(keep) + '\n')
    return out, len(keep), ncod//3

def run(tag, phyf, treef, model, w='0.3'):
    d=S/f'fx_{tag}'; d.mkdir(exist_ok=True)
    (d/'codeml.ctl').write_text(f"""      seqfile = {phyf}
     treefile = {treef}
      outfile = out.txt
        noisy = 0
      verbose = 1
      runmode = 0
      seqtype = 1
    CodonFreq = 2
        model = {model}
      NSsites = 0
        icode = 0
    fix_kappa = 0
        kappa = 2
    fix_omega = 0
        omega = {w}
        clock = 0
    cleandata = 0
""")
    subprocess.run(['codeml','codeml.ctl'], cwd=d, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    t=(d/'out.txt').read_text() if (d/'out.txt').exists() else ''
    lnl=re.search(r'lnL\(ntime:\s*(\d+)\s*np:\s*(\d+)\):\s*(-?[0-9.]+)', t)
    om=re.findall(r'omega \(dN/dS\) =\s*([0-9.]+)', t)
    br=re.search(r'w \(dN/dS\) for branches:\s*([0-9. ]+)', t)
    rooted='This is a rooted tree' in t
    return dict(ntime=int(lnl.group(1)) if lnl else None, np=int(lnl.group(2)) if lnl else None,
                lnL=float(lnl.group(3)) if lnl else None,
                om=[float(x) for x in om], brw=[float(x) for x in br.group(1).split()] if br else [],
                rooted=rooted, txt=t)

ALL={'human','rat','rabbit','dog','horse','cow','sheep','opossum','chicken','xenopus','zebrafish','ciona','branchiostoma'}
print("  === A. UNROOTED, both deep taxa (the fix) ===")
(S/'u0.tree').write_text(f"  13  1\n(branchiostoma,ciona,{V});\n")
(S/'u1.tree').write_text(f"  13  1\n(branchiostoma #1,ciona #1,{V});\n")
p13,_,nc = phy(ALL)
a0=run('u_m0', p13, S/'u0.tree', 0); a1=run('u_m2', p13, S/'u1.tree', 2)
for nm,r in [('M0',a0),('two-ratio',a1)]:
    print(f"    {nm:10s} ntime={r['ntime']} np={r['np']} lnL={r['lnL']} "
          f"omega={r['om'] or r['brw']}  rooted-warning={r['rooted']}")
if a0['lnL'] and a1['lnL']:
    lr=2*(a1['lnL']-a0['lnL']); p=1-chi2.cdf(lr,1) if lr>0 else 1.0
    print(f"    LRT = {lr:.4f}, 1 df, p = {p:.4g}")
    print(f"    (rooted run gave LRT 28.33, p 1.0e-07, foreground omega 0.0025)")

print("\n  === B. LEAVE-ONE-OUT: Branchiostoma removed (grok called this mandatory) ===")
sub=ALL-{'branchiostoma'}
p12,n12,nc12 = phy(sub)
(S/'l0.tree').write_text(f"  12  1\n(ciona,{V});\n".replace('(ciona,','(ciona,') )
# unrooted 12-taxon: ciona as one of three basal lineages requires splitting the vertebrate clade
(S/'l0.tree').write_text(f"  12  1\n(ciona,(((((human,(rat,rabbit)),(dog,horse)),(cow,sheep)),opossum),(chicken,(xenopus,zebrafish))));\n")
(S/'l1.tree').write_text(f"  12  1\n(ciona #1,(((((human,(rat,rabbit)),(dog,horse)),(cow,sheep)),opossum),(chicken,(xenopus,zebrafish))));\n")
b0=run('l_m0', p12, S/'l0.tree', 0); b1=run('l_m2', p12, S/'l1.tree', 2)
print(f"    {n12} taxa, {nc12} codons")
for nm,r in [('M0',b0),('two-ratio',b1)]:
    print(f"    {nm:10s} ntime={r['ntime']} np={r['np']} lnL={r['lnL']} "
          f"omega={r['om'] or r['brw']}  rooted-warning={r['rooted']}")
if b0['lnL'] and b1['lnL']:
    lr=2*(b1['lnL']-b0['lnL']); p=1-chi2.cdf(lr,1) if lr>0 else 1.0
    print(f"    LRT = {lr:.4f}, 1 df, p = {p:.4g}   <- Ciona alone as foreground")
