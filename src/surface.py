"""Surface conservation per SURFACE_PREREGISTRATION.md + SURFACE_AMENDMENT.md."""
import gzip,json,warnings,sys
import numpy as np, pandas as pd
warnings.filterwarnings('ignore')
from Bio.PDB import MMCIFParser, ShrakeRupley
from Bio.PDB.Polypeptide import protein_letters_3to1 as _T31
T31={k.upper():v for k,v in dict(_T31).items()}
MAXASA={'A':129,'R':274,'N':195,'D':193,'C':167,'E':223,'Q':225,'G':104,'H':224,'I':197,'L':201,
        'K':236,'M':224,'F':240,'P':159,'S':155,'T':172,'W':285,'Y':263,'V':174}
CIF='data/raw/struct/4V60-assembly1.cif.gz'
rng=np.random.default_rng(20261106)

print('parsing assembly...',flush=True)
with gzip.open(CIF,'rt') as fh:
    st=MMCIFParser(QUIET=True).get_structure('v',fh)
model=next(st.get_models())
chains=[c for c in model if sum(1 for r in c if r.id[0]==' ')>100]
print('protein chains:',len(chains),flush=True)
GATE_CHAINS=len(chains)>=70

def com(ch): 
    a=np.array([at.coord for r in ch for at in r if r.id[0]==' ']); return a.mean(0),a
allc=np.vstack([com(c)[1] for c in chains])
center=allc.mean(0)
X=allc-center
# principal axis = eigenvector of smallest spread? For a barrel, symmetry axis is the one with
# largest extent if elongated; 4V60 vault is elongated along its axis.
w,V=np.linalg.eigh(np.cov(X.T))
axis=V[:,np.argmax(w)]
proj=lambda P:( (P-center)@axis, np.linalg.norm((P-center)-np.outer((P-center)@axis,axis),axis=1) )
z_all,r_all=proj(allc)
print(f'assembly {len(allc)} atoms | z range {z_all.min():.0f}..{z_all.max():.0f} | r range {r_all.min():.0f}..{r_all.max():.0f}',flush=True)

ref=chains[0]
rc,ra=com(ref)
near=[c for c in chains if c is not ref and np.linalg.norm(com(c)[0]-rc)<180]
print('reference chain',ref.id,'| neighbour chains kept:',len(near),flush=True)

class Sel:
    def __init__(self,cl): self.cl=cl
sr=ShrakeRupley()
import copy
def sasa_of(chlist):
    import Bio.PDB
    s=Bio.PDB.Structure.Structure('x'); m=Bio.PDB.Model.Model(0); s.add(m)
    for c in chlist: m.add(copy.deepcopy(c))
    sr.compute(m,level='R')
    return {(c.id,r.id[1]):r.sasa for c in m for r in c if r.id[0]==' '}
print('SASA in context...',flush=True)
ctx=sasa_of([ref]+near)
print('SASA isolated...',flush=True)
iso=sasa_of([ref])

rows=[]; _seen=set()
for r in ref:
    if r.id[0]!=' ': continue
    k=(ref.id,r.id[1])
    if k not in ctx or k not in iso: continue
    aa=T31.get(r.get_resname().strip().upper(),'X')
    if aa not in MAXASA: continue
    P=np.array([at.coord for at in r])
    zz,rr=proj(P)
    rows.append(dict(resi=r.id[1],aa=aa,sasa_ctx=ctx[k],sasa_iso=iso[k],
                     rsa=ctx[k]/MAXASA[aa],rsa_iso=iso[k]/MAXASA[aa],
                     z=float(zz.mean()),r=float(rr.mean())))
assert rows, 'no residues scored - check residue-name mapping'
D=pd.DataFrame(rows).sort_values('resi').reset_index(drop=True)
print('reference chain residues scored:',len(D),flush=True)
D['interface']=(D.sasa_iso-D.sasa_ctx)>20
D['buried']=(D.rsa<.15)&(~D.interface)
D['exposed']=(D.rsa>=.15)&(~D.interface)
# local midsurface radius at each residue's |z|
az=np.abs(D.z.values); A=np.abs(z_all)
mid=np.array([np.median(r_all[(A>=z-5)&(A<=z+5)]) if ((A>=z-5)&(A<=z+5)).sum()>50 else np.nan for z in az])
D['R_local']=mid; D['dr']=D.r-D.R_local
# conservation from eggNOG alignment, anchored on the rat sequence
import tarfile
T=tarfile.open('data/raw/divergence/2759_trimmed_algs.tar')
m=[x for x in T.getmembers() if x.name.endswith('/2QPP0.trimmed_alg.faa.gz')][0]
fa=gzip.decompress(T.extractfile(m).read()).decode()
seqs={};cur=None
for ln in fa.splitlines():
    if ln.startswith('>'): cur=ln[1:].split()[0]; seqs[cur]=[]
    else: seqs[cur].append(ln.strip())
seqs={k:''.join(v) for k,v in seqs.items()}
rat=[k for k in seqs if k.startswith('10116.')]
print('rat sequences in alignment:',rat,flush=True)
key=rat[0]; S=np.array(list(seqs[key])); M=np.array([list(v) for v in seqs.values()])
ung=np.where(S!='-')[0]
cons=[]
for col in ung:
    c=M[:,col]; ok=c!='-'
    cons.append((c[ok]==S[col]).mean() if ok.sum()>=len(c)/2 else np.nan)
ratseq=''.join(S[ung]); cons=np.array(cons)
# align structure sequence to rat alignment sequence by offset search
struct_seq=''.join(D.aa)
best=(None,-1)
for off in range(-50,len(ratseq)-len(struct_seq)+51):
    idx=D.resi.values-D.resi.values[0]+off
    ok=(idx>=0)&(idx<len(ratseq))
    if ok.sum()<100: continue
    match=np.mean([ratseq[i]==a for i,a in zip(idx[ok],np.array(list(struct_seq))[ok])])
    if match>best[1]: best=(off,match)
off,match=best
print(f'sequence mapping offset {off}, identity {match:.3f}',flush=True)
idx=D.resi.values-D.resi.values[0]+off
D['cons']=[cons[i] if 0<=i<len(cons) else np.nan for i in idx]
D=D.dropna(subset=['cons','dr'])
D.to_csv('results/surface_residues.csv',index=False)

ex=D[D.exposed]; lum=ex[ex.dr<0]; out=ex[ex.dr>0]
gate_burial=D[D.buried].cons.mean()>ex.cons.mean()
print(f"\nGATE chains>=70: {GATE_CHAINS} | buried cons {D[D.buried].cons.mean():.3f} > exposed {ex.cons.mean():.3f}: {gate_burial}",flush=True)
print(f"counts: buried {D.buried.sum()}, interface {D.interface.sum()}, exposed {len(ex)} (lumen {len(lum)}, outward {len(out)})",flush=True)
diff=out.cons.mean()-lum.cons.mean()
# block bootstrap over 20-residue windows
blocks=[g for _,g in ex.groupby(ex.resi//20)]
bs=[]
for _ in range(2000):
    s=pd.concat([blocks[i] for i in rng.integers(0,len(blocks),len(blocks))])
    l=s[s.dr<0]; o=s[s.dr>0]
    if len(l)>5 and len(o)>5: bs.append(o.cons.mean()-l.cons.mean())
lo,hi=np.percentile(bs,[2.5,97.5])
lab=('NO DIFFERENCE' if lo<=0<=hi else ('OUTWARD-FACING CONSERVED' if diff>0 else 'LUMEN-FACING CONSERVED'))
if not (GATE_CHAINS and gate_burial): lab='UNINFORMATIVE'
from scipy.stats import spearmanr
rho=spearmanr(ex.dr,ex.cons)
print(f"\nmean conservation: lumen {lum.cons.mean():.3f} | outward {out.cons.mean():.3f} | interface {D[D.interface].cons.mean():.3f} | buried {D[D.buried].cons.mean():.3f}",flush=True)
print(f"difference outward-lumen {diff:+.4f} (95% CI {lo:+.4f},{hi:+.4f}) -> {lab}",flush=True)
print(f"secondary: Spearman cons vs dr among exposed = {rho.statistic:+.3f} (p={rho.pvalue:.2g})",flush=True)
json.dump(dict(label=lab,chains=len(chains),gate_chains=bool(GATE_CHAINS),gate_burial=bool(gate_burial),
   n_buried=int(D.buried.sum()),n_interface=int(D.interface.sum()),n_lumen=len(lum),n_outward=len(out),
   cons_lumen=float(lum.cons.mean()),cons_outward=float(out.cons.mean()),
   cons_interface=float(D[D.interface].cons.mean()),cons_buried=float(D[D.buried].cons.mean()),
   diff=float(diff),ci=[float(lo),float(hi)],spearman_dr=float(rho.statistic),map_identity=float(match)),
   open('results/surface.json','w'),indent=1)
