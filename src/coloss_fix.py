"""Check 0.2: do not call a clade lost when a well-retained sister subclade sits inside it."""
import numpy as np,pandas as pd,json,sys
sys.argv=['x','none']
exec(open('src/coloss.py').read().split("mode = sys.argv[1]")[0])
def events2(g):
    v=F[g]; tot=M[g].sum(); n=ROOT
    while True:
        nx=[c for c in ch[n] if (M[g]&NM[ni[c]]).sum()>=.9*tot]
        if not nx: break
        n=nx[0]
    out=[]
    def go(x):
        for c in ch[x]:
            j=ni[c]
            if sz[j]<2: continue
            if v[j]<=.1:
                kids=[k for k in ch[c] if sz[ni[k]]>=2 and F[g][ni[k]]>=.5]
                if kids: go(c)          # a retained subclade lives inside: descend instead
                else: out.append(j)
            else: go(c)
    go(n)
    return out
q=idx[og_of('MVP')]
old=np.where(Ev[q])[0]; new=events2(q)
f=lambda L:[(names[nodes[j]],int(sz[j])) for j in L]
print('OLD events:',f(old)); print('NEW events:',f(new))
Ev2=Ev.copy(); Ev2[q]=False; Ev2[q,new]=True
def score2(q,L):
    co=((F[:,L]<=.1)&(Sib[:,L]>=.5)).sum(axis=1); go=(Ev[:,F[q]>.5]).sum(axis=1)
    s=co/np.maximum(len(L)+go,1)
    d=pd.DataFrame({'og':OGS,'s':s,'co':co}).iloc[scored]; d=d[d.og!=OGS[q]]
    return d.sort_values(['s','co'],ascending=[False,False])
d=score2(q,np.array(new)); e=enrich(d[d.co>=1].og.head(100).tolist())
print('after fix: min q',round(float(e.q.min()),4) if len(e) else None,'| terms<.05',int((e.q<.05).sum()) if len(e) else 0)
print('top partners:',[(','.join(HS[o][:3]),int(c)) for o,c in zip(d.og.head(12),d.co.head(12))])
json.dump({'old_events':f(old),'new_events':f(new),'min_q':float(e.q.min()) if len(e) else None,
  'n_sig':int((e.q<.05).sum()) if len(e) else 0,
  'top':[ (','.join(HS[o][:3]),int(c)) for o,c in zip(d.og.head(20),d.co.head(20))]},
  open('results/coloss_fixed.json','w'),indent=1)
