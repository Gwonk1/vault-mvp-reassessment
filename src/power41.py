"""What effect size did the section 41 replication test actually have power for?
N=1205 universe, K=88 interactors, M=95 term members. alpha=0.05 one-sided."""
import numpy as np
from scipy.stats import hypergeom
N,K,M = 1205,88,95
exp = M*K/N
# critical value: smallest obs with hypergeom p < 0.05 under the null
crit = next(k for k in range(M+1) if hypergeom.sf(k-1,N,M,K) < 0.05)
print(f'universe N={N}  interactors K={K}  term members M={M}')
print(f'expected under null = {exp:.2f}')
print(f'critical value (smallest significant obs at alpha=0.05) = {crit}  -> fold = {crit/exp:.2f}x')
print(f'observed in section 41 = 9  -> fold = {9/exp:.2f}x,  p = {hypergeom.sf(8,N,M,K):.3f}\n')
# power: if the TRUE enrichment is f-fold, what fraction of experiments reach crit?
# model: term members have elevated probability of being interactors; simulate by
# drawing the number of term-member interactors from a non-central hypergeometric
# approximated by a binomial with p = f*K/N capped at 1
print('power curve (binomial approximation, p_hit = f * K/N):')
rng=np.random.default_rng(0)
for f in [1.0,1.5,2.0,2.5,3.0,3.5,4.0,5.0]:
    p = min(f*K/N, 1.0)
    draws = rng.binomial(M, p, 40000)
    pw = (draws >= crit).mean()
    print(f'  {f:>4.1f}x  expected obs {M*p:5.1f}   power = {pw:.3f}' + ('   <-- 80% power threshold' if 0.78<=pw<=0.86 else ''))
# solve for 80% power
lo,hi=1.0,6.0
for _ in range(40):
    mid=(lo+hi)/2; p=min(mid*K/N,1.0)
    pw=(rng.binomial(M,p,40000)>=crit).mean()
    if pw<0.80: lo=mid
    else: hi=mid
print(f'\n=> 80% power requires about {hi:.2f}x enrichment ({M*min(hi*K/N,1):.1f} of {M} term members as interactors)')
print(f'=> section 40 reported an 18x enrichment in the co-elution tail; this test could see ~{hi:.1f}x')
# and what would section 40's effect look like here?
print(f'\nIf the true effect here were the 2x that an association might plausibly give:')
p=min(2.0*K/N,1); print(f'   expected {M*p:.1f} of 95, power {(rng.binomial(M,p,40000)>=crit).mean():.2f}')
