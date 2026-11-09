#!/usr/bin/env python3
"""Extended codon model: 11 vertebrates + Ciona + Branchiostoma, plus the
two-ratio branch test registered in TIER0_PREREGISTRATION.md as the CORRECTED
version of the ill-posed 'branches leading to clades that lost MVP' test."""
import pathlib, subprocess, re, statistics as st
S=pathlib.Path('/tmp/claude-1000/-home-graham-projects/46738ac0-1f6d-4b80-81fe-caa9aa37b1a5/scratchpad/t0')
bases='TCAG'; aas='FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG'
CODON={b1+b2+b3:aas[i] for i,(b1,b2,b3) in enumerate((a,b,c) for a in bases for b in bases for c in bases)}
tr=lambda s: ''.join(CODON.get(s[i:i+3].upper(),'X') for i in range(0,len(s)-2,3))
def rd(p):
    d={}
    for blk in pathlib.Path(p).read_text().split('>')[1:]:
        l=blk.split('\n'); d[l[0].strip()]=''.join(l[1:]).strip().upper()
    return d

cds=rd(S/'mvp_cds_ok.fna')
for extra in ('ciona','branchiostoma'):
    f=S/f'{extra}_cds.fna'
    if f.exists(): cds.update(rd(f))
print(f"  taxa: {sorted(cds)}")
prot={}
for k,v in cds.items():
    p=tr(v); p=p[:-1] if p.endswith('*') else p
    if '*' in p: print(f"    {k}: internal stop, DROPPED"); continue
    prot[k]=p; cds[k]=v[:len(p)*3]
(S/'deep.faa').write_text(''.join(f'>{k}\n{v}\n' for k,v in prot.items()))
subprocess.run(['mafft','--quiet','--auto',str(S/'deep.faa')],
               stdout=open(S/'deep.afa','w'), stderr=subprocess.DEVNULL, check=True)
pal=rd(S/'deep.afa'); names=list(pal)
cal={}
for n in names:
    out=[];k=0;c=cds[n]
    for aa in pal[n]:
        if aa=='-': out.append('---')
        else: out.append(c[k*3:k*3+3] if len(c)>=k*3+3 else '---'); k+=1
    cal[n]=''.join(out)
L=len(cal[names[0]])
keep=[i for i in range(0,L,3) if all('-' not in cal[n][i:i+3] and len(cal[n][i:i+3])==3 for n in names)]
clean={n:''.join(cal[n][i:i+3] for i in keep) for n in names}
nc=len(keep)
print(f"  alignment {L//3} columns -> {nc} gap-free codons across {len(names)} taxa")
print(f"  (mammal-only run had 786 codons across 11 taxa)")
with (S/'deep.phy').open('w') as fh:
    fh.write(f" {len(names)} {nc*3}\n")
    for n in names: fh.write(f"{n}  {clean[n]}\n")  # PAML needs >=2 spaces after the name; {n:<14} left exactly one for "branchiostoma" and codeml ate a base

VERT="(((((human,(rat,rabbit)),(dog,horse)),(cow,sheep)),opossum),(chicken,(xenopus,zebrafish)))"
has=lambda x: x in names
inv=[x for x in ('branchiostoma','ciona') if has(x)]
if len(inv)==2: T0=f"(branchiostoma,(ciona,{VERT}))"; T1=f"(branchiostoma #1,(ciona #1,{VERT}))"
elif inv:      T0=f"({inv[0]},{VERT})";               T1=f"({inv[0]} #1,{VERT})"
else:          T0=VERT; T1=None
(S/'deep0.tree').write_text(f"  {len(names)}  1\n{T0};\n")
if T1: (S/'deep1.tree').write_text(f"  {len(names)}  1\n{T1};\n")
print(f"  tree: {T0}")

def run(tag, tree, model, w):
    d=S/f'cmd_{tag}_{w}'; d.mkdir(exist_ok=True)
    (d/'codeml.ctl').write_text(f"""      seqfile = {S}/deep.phy
     treefile = {tree}
      outfile = out.txt
        noisy = 0
      verbose = 0
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
    lnl=re.search(r'lnL\(.*?\):\s*(-?[0-9.]+)', t)
    oms=re.findall(r'omega \(dN/dS\) =\s*([0-9.]+)', t)
    w0=re.search(r'w \(dN/dS\) for branches:\s*([0-9. ]+)', t)
    return (float(lnl.group(1)) if lnl else None,
            [float(x) for x in oms] or ([float(x) for x in w0.group(1).split()] if w0 else []))

print("\n  --- M0, one omega for the whole tree ---")
r=[run('m0', S/'deep0.tree', 0, w) for w in ('0.05','0.5')]
for w,(l,o) in zip(('0.05','0.5'), r): print(f"    start {w}: lnL={l}  omega={o}")
gate = r[0][1] and r[1][1] and abs(r[0][1][0]-r[1][1][0])<=0.02
print(f"    GATE reproducibility (<=0.02): {'PASS' if gate else 'FAIL'}")
if T1:
    print("\n  --- two-ratio: invertebrate branches as foreground (the registered branch test) ---")
    r2=[run('m2', S/'deep1.tree', 2, w) for w in ('0.05','0.5')]
    for w,(l,o) in zip(('0.05','0.5'), r2): print(f"    start {w}: lnL={l}  omegas={o}")
    if r[0][0] and r2[0][0]:
        lr=2*(r2[0][0]-r[0][0])
        from scipy.stats import chi2
        p=1-chi2.cdf(lr,1) if lr>0 else 1.0
        print(f"\n    LRT 2*dlnL = {lr:.4f} on 1 df  ->  p = {p:.4g}")
        print(f"    {'constraint is NOT uniform across the retained tree' if p<0.05 else 'no evidence that constraint differs between vertebrate and invertebrate branches'}")
