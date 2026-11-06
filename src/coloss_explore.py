"""Exploratory, after the verdict. Sensitivity of MVP's NO MODULE label and how its best partners compare."""
import sys
sys.argv=['coloss','none']
exec(open('src/coloss.py').read().split("mode = sys.argv[1]")[0])
def scoreL(q,L):
    co=((F[:,L]<=.1)&(Sib[:,L]>=.5)).sum(axis=1); go=(Ev[:,F[q]>.5]).sum(axis=1)
    s=co/np.maximum(len(L)+go,1)
    d=pd.DataFrame({'og':OGS,'s':s,'co':co,'g_only':go}).iloc[scored]; d=d[d.og!=OGS[q]]
    return d.sort_values(['s','co','g_only'],ascending=[False,False,True])
q=idx[og_of('MVP')]; L0=np.where(Ev[q])[0]; names_L=[names[nodes[j]] for j in L0]
drop=[j for j in L0 if names[nodes[j]] in('Passeriformes','Alligator')]; L1=np.array([j for j in L0 if j not in drop])
print('events',names_L,'->',[names[nodes[j]] for j in L1])
for lab,L in (('all 9',L0),('without 2 vertebrate gaps',L1)):
    d=scoreL(q,L); e=enrich(d[d.co>=1].og.head(100).tolist()); print('\n',lab,'min q',round(float(e.q.min()),4) if len(e) else None,'terms<.05',int((e.q<.05).sum()) if len(e) else 0,'top',e.head(4)[['term','k','K','q']].round(3).values.tolist(),'max co',int(d.co.max()),'n at max',int((d.co==d.co.max()).sum()),'top s',round(float(d.s.max()),3))
    print('  top',[ (','.join(HS[o][:3]),int(c)) for o,c in zip(d.og.head(14),d.co.head(14))])
for s in ['TEP1','PARP4']:
    for o in [x for x in OGS.tolist() if s in HS[x]]:
        print(s,o,'rank without gaps',list(d.og).index(o)+1 if o in set(d.og) else None,'of',len(d))
# Protostomia: where does MVP remain inside it
J=[j for j in L0 if names[nodes[j]]=='Protostomia'][0]; ins=np.where(NM[J]&M[q])[0]; print('\nProtostomia present',[tax.name[SP[i]] for i in ins],'of',int(sz[J]))
# Is MVP's best partner score ordinary?
rng=np.random.default_rng(20261106); cand=scored[(np.abs(nev[scored]-len(L0))<=1)&(np.abs(frac[scored]-frac[q])<=.1)&(scored!=q)]
tops=[]; minq=[]
for r in cand:
    d=score(r)[0]; tops.append(d.s.iloc[:20].mean()); e=enrich(d[d.co>=1].og.head(100).tolist()); minq.append(float(e.q.min()) if len(e) else 1)
tops=np.array(tops); minq=np.array(minq); dm=scoreL(q,L0)
print('\nmean score of top 20 partners: MVP',round(float(dm.s.iloc[:20].mean()),3),'| matched median',round(float(np.median(tops)),3),'q10-90',np.quantile(tops,[.1,.9]).round(3),'| MVP pct',round(float((tops<dm.s.iloc[:20].mean()).mean()*100),1))
print('min q: matched with <.05',round(float((minq<.05).mean()),3),'median',round(float(np.median(minq)),4))
for s in ['IFT88','NDUFS2']:
    d=score(idx[og_of(s)])[0]; print(s,'top20 mean',round(float(d.s.iloc[:20].mean()),3),'events',int(nev[idx[og_of(s)]]))
