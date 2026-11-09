#!/usr/bin/env python3
"""Run codeml M0 on one gene's CDS set, same tree and pipeline as MVP.
Apples-to-apples: grok audit 009 warned a codeml omega cannot be placed against
NG86 pairwise control values. Registered at 06dd589."""
import pathlib, subprocess, sys, re, os
S=pathlib.Path('/tmp/claude-1000/-home-graham-projects/46738ac0-1f6d-4b80-81fe-caa9aa37b1a5/scratchpad/t0')
FULL="(((((human,(rat,rabbit)),(dog,horse)),(cow,sheep)),opossum),(chicken,(xenopus,zebrafish)))"
bases='TCAG'; aas='FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG'
CODON={b1+b2+b3:aas[i] for i,(b1,b2,b3) in enumerate((a,b,c) for a in bases for b in bases for c in bases)}
def tr(s): return ''.join(CODON.get(s[i:i+3].upper(),'X') for i in range(0,len(s)-2,3))
def rd(p):
    d={}
    for blk in p.read_text().split('>')[1:]:
        l=blk.split('\n'); d[l[0].strip()]=''.join(l[1:]).strip().upper()
    return d
def prune(tree, keep):
    """Parse, drop absent leaves, COLLAPSE single-child nodes, re-serialise.
    The first version used regex substitution and produced nodes with one child,
    which codeml silently rejects (GAPDH returned no omega)."""
    def parse(s, i=0):
        if s[i] != '(':
            j = i
            while j < len(s) and s[j] not in ',)': j += 1
            return s[i:j], j
        kids = []; i += 1
        while True:
            node, i = parse(s, i)
            kids.append(node)
            if s[i] == ',': i += 1
            elif s[i] == ')': return kids, i + 1
    def drop(n):
        if isinstance(n, str): return n if n in keep else None
        kids = [k for k in (drop(c) for c in n) if k is not None]
        if not kids: return None
        if len(kids) == 1: return kids[0]          # collapse
        return kids
    def ser(n): return n if isinstance(n, str) else '(' + ','.join(ser(c) for c in n) + ')'
    t, _ = parse(tree)
    d = drop(t)
    return ser(d)

def run(gene, fna):
    cds=rd(fna); prot={}
    for k,v in cds.items():
        p=tr(v); p=p[:-1] if p.endswith('*') else p
        if '*' in p or len(p)<60: continue
        prot[k]=p; cds[k]=v[:len(p)*3]
    if prot:
        import statistics as _st
        med=_st.median([len(v) for v in prot.values()])
        short=[k for k,v in prot.items() if len(v) < 0.70*med]
        for k in short:
            print(f"    {gene}: dropping {k} as fragmentary ({len(prot[k])} aa vs median {med:.0f})")
            prot.pop(k); cds.pop(k, None)
    if len(prot)<5: print(f"  {gene}: only {len(prot)} usable - SKIP"); return None
    (S/f'{gene}.faa').write_text(''.join(f'>{k}\n{v}\n' for k,v in prot.items()))
    subprocess.run(['mafft','--quiet','--auto',str(S/f'{gene}.faa')],
                   stdout=open(S/f'{gene}.afa','w'), stderr=subprocess.DEVNULL, check=True)
    pal=rd(S/f'{gene}.afa'); names=list(pal)
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
    if nc<100: print(f"  {gene}: only {nc} gap-free codons - SKIP"); return None
    with (S/f'{gene}.phy').open('w') as fh:
        fh.write(f" {len(names)} {nc*3}\n")
        for n in names: fh.write(f"{n:<12}{clean[n]}\n")
    tree=prune(FULL, set(names))
    (S/f'{gene}.tree').write_text(f"  {len(names)}  1\n{tree};\n")
    res=[]
    for w in ('0.05','0.5'):
        d=S/f'cm_{gene}_{w}'; d.mkdir(exist_ok=True)
        (d/'codeml.ctl').write_text(f"""      seqfile = {S}/{gene}.phy
     treefile = {S}/{gene}.tree
      outfile = out.txt
        noisy = 0
      verbose = 0
      runmode = 0
      seqtype = 1
    CodonFreq = 2
        model = 0
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
        txt=(d/'out.txt').read_text() if (d/'out.txt').exists() else ''
        m=re.search(r'omega \(dN/dS\) =\s*([0-9.]+)', txt); l=re.search(r'lnL\(.*?\):\s*(-?[0-9.]+)', txt)
        k=re.search(r'kappa \(ts/tv\) =\s*([0-9.]+)', txt)
        res.append((float(m.group(1)) if m else None, float(l.group(1)) if l else None,
                    float(k.group(1)) if k else None))
    print(f"  {gene:7s} n={len(names):2d} taxa, {nc:4d} codons | omega(start 0.05)={res[0][0]} "
          f"omega(start 0.5)={res[1][0]} | lnL={res[0][1]} kappa={res[0][2]}")
    print(f"          tree: {tree}")
    return res

import sys
_only=sys.argv[1:] or ['MVP','GAPDH','CD4']
for gene, f in [('MVP', S/'mvp_cds_ok.fna'), ('GAPDH', S/'GAPDH_cds.fna'), ('CD4', S/'CD4_cds.fna')]:
    if gene not in _only: continue
    if f.exists(): run(gene, f)
