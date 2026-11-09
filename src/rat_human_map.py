#!/usr/bin/env python3
"""Does rat 42-47 correspond to human 36-42? Align the sequences AS MODELLED in the
two structures, then map the contact sets through the alignment. §96e flagged this
as needing an alignment rather than an eyeballed offset (house rule 3)."""
import gzip, subprocess, pathlib
T={'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLN':'Q','GLU':'E','GLY':'G','HIS':'H',
   'ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S','THR':'T','TRP':'W',
   'TYR':'Y','VAL':'V','MSE':'M'}
S=pathlib.Path('/tmp/claude-1000/-home-graham-projects/46738ac0-1f6d-4b80-81fe-caa9aa37b1a5/scratchpad/t0')

def chain_seq(path):
    """Sequence of ONE chain, with the author residue numbers it carries."""
    cols=[]; seen={}; first=None
    with gzip.open(path,'rt') as fh:
        inloop=False
        for line in fh:
            if line.startswith('_atom_site.'): cols.append(line.strip().split('.')[1]); inloop=True; continue
            if inloop and line.startswith('ATOM'):
                f=line.split()
                if len(f)<len(cols): continue
                ix={c:i for i,c in enumerate(cols)}
                c=f[ix['auth_asym_id']]
                if first is None: first=c
                if c!=first: break
                if f[ix['label_atom_id']].strip('"')!='CA': continue
                aa=T.get(f[ix['label_comp_id']].upper())
                if not aa: continue
                n=f[ix['auth_seq_id']]
                if n.lstrip('-').isdigit(): seen[int(n)]=aa
            elif inloop and seen and not line.startswith(('ATOM','HETATM')): break
    nums=sorted(seen)
    return nums, ''.join(seen[n] for n in nums)

rn, rs = chain_seq('data/raw/struct/4V60-assembly1.cif.gz')
hn, hs = chain_seq('data/raw/struct/9BW5-assembly1.cif.gz')
print(f"  4V60 (rat)  chain modelled: {len(rn)} residues, {rn[0]}..{rn[-1]}")
print(f"  9BW5 (human) chain modelled: {len(hn)} residues, {hn[0]}..{hn[-1]}")

(S/'rh.faa').write_text(f">rat\n{rs}\n>human\n{hs}\n")
subprocess.run(['mafft','--quiet','--auto',str(S/'rh.faa')],
               stdout=open(S/'rh.afa','w'), stderr=subprocess.DEVNULL, check=True)
al={}
for blk in (S/'rh.afa').read_text().split('>')[1:]:
    l=blk.split('\n'); al[l[0].strip()]=''.join(l[1:]).strip()
ra, ha = al['rat'], al['human']
print(f"  aligned length {len(ra)}")

# column -> author residue number, per species
def colmap(aln, nums):
    m={}; k=0
    for i,ch in enumerate(aln):
        if ch!='-': m[i]=nums[k]; k+=1
    return m
rc, hc = colmap(ra, rn), colmap(ha, hn)
rat2col={v:k for k,v in rc.items()}; col2hum=hc

RAT=[1,2,3,4,6,21,42,43,44,45,46,47]
HUM_CORE=[21,22,38,39,40]; HUM_ALL=[6,7,9,21,22,36,38,39,40,41]
print(f"\n  rat contact residue -> aligned column -> human residue at that column:")
mapped=[]
for r in RAT:
    c=rat2col.get(r)
    h=col2hum.get(c) if c is not None else None
    hit='' if h is None else ('  <-- in the human contact set' if h in HUM_ALL else '')
    print(f"    rat {r:3d} -> col {c if c is not None else '--':>4} -> human {h if h is not None else 'gap':>4}{hit}")
    if h is not None: mapped.append((r,h))
print(f"\n  rat contacts that map onto a human contact residue: "
      f"{[(r,h) for r,h in mapped if h in HUM_ALL]}")
print(f"  rat contacts mapping into the human CORE (21,22,38-40): "
      f"{[(r,h) for r,h in mapped if h in HUM_CORE]}")
print(f"\n  and the reverse - human core -> rat:")
hum2col={v:k for k,v in hc.items()}
for h in HUM_CORE:
    c=hum2col.get(h); r=rc.get(c) if c is not None else None
    print(f"    human {h:3d} -> col {c if c is not None else '--':>4} -> rat {r if r is not None else 'gap':>4}"
          f"{'  <-- in the rat contact set' if r in RAT else ''}")
