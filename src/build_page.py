"""Build the review page from results/figdata.json. Output: results/page/index.html"""
import json,html,os,math,re
D=json.load(open('results/figdata.json'))
def esc(x): return html.escape(str(x),quote=True)
def scale(a,b,x0,x1): return lambda v: x0+(v-a)/(b-a)*(x1-x0)
def ticks(a,b,n=5):
    s=(b-a)/n; m=10**math.floor(math.log10(s)); st=min((m*k for k in (1,2,2.5,5,10) if m*k>=s),default=s)
    t=math.ceil(a/st)*st; o=[]
    while t<=b+1e-9: o.append(round(t,6)); t+=st
    return o
def tf(v): return ('%g'%v).replace('-','−')
def xaxis(sx,y0,y1,a,b,label):
    o=''
    for t in ticks(a,b):
        x=sx(t); o+=f'<line class="grid" x1="{x:.1f}" x2="{x:.1f}" y1="{y0}" y2="{y1}"/><text class="tick" x="{x:.1f}" y="{y1+16}" text-anchor="middle">{tf(t)}</text>'
    return o+f'<text class="axl" x="{(sx(a)+sx(b))/2:.1f}" y="{y1+34}" text-anchor="middle">{esc(label)}</text>'
def yaxis(sy,x0,x1,a,b,label):
    o=''
    for t in ticks(a,b):
        y=sy(t); o+=f'<line class="grid" y1="{y:.1f}" y2="{y:.1f}" x1="{x0}" x2="{x1}"/><text class="tick" x="{x0-6}" y="{y+4:.1f}" text-anchor="end">{tf(t)}</text>'
    return o+f'<text class="axl" transform="translate(12,{(sy(a)+sy(b))/2:.1f}) rotate(-90)" text-anchor="middle">{esc(label)}</text>'
def scatter(xs,ys,title,xl,cls,w=340,h=270):
    L,R,T,B=48,10,28,48; a=-2.6;b=2.6
    fin=[(x,y) for x,y in zip(xs,ys)]
    m=sum(x for x,_ in fin)/len(fin); sd=(sum((x-m)**2 for x,_ in fin)/(len(fin)-1))**.5
    Z=[(x-m)/sd for x,_ in fin]; ya=max(abs(y) for _,y in fin); cy=min(4,math.ceil(ya))
    sx=scale(-3.2,3.2,L,w-R); sy=scale(-cy,cy,h-B,T)
    my=sum(y for _,y in fin)/len(fin); sxy=sum((z)*(y-my) for z,(_,y) in zip(Z,fin))/(len(fin)-1); sdy=(sum((y-my)**2 for _,y in fin)/(len(fin)-1))**.5; r=sxy/sdy
    o=f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}, r {r:.2f}"><text class="pt" x="{L}" y="16">{esc(title)}</text><text class="pv" x="{w-R}" y="16" text-anchor="end">r = {r:.2f}</text>'
    o+=xaxis(sx,T,h-B,-3.2,3.2,xl)+yaxis(sy,L,w-R,-cy,cy,'MVP (z)')
    for z,(_,y) in zip(Z,fin):
        if abs(z)<=3.2 and abs(y)<=cy: o+=f'<circle class="{cls}" cx="{sx(z):.1f}" cy="{sy(y):.1f}" r="3" fill-opacity=".55"/>'
    return o+'</svg>'
def fig1():
    o='<div class="grid2">'
    for k,n in (('imvigor','IMvigor210'),('liu','Liu 2019')):
        s=D['scatter'][k]
        o+=scatter(s['a'],s['mvp'],f'{n}: vs ISG.RS','ISG.RS score (z)','s1')+scatter(s['c'],s['mvp'],f'{n}: vs IFNG.GS','IFNG.GS score (z)','s2')
    return o+'</div>'
def fig2():
    F=D['forest']; names={'riaz':'Riaz','hugo':'Hugo','liu':'Liu','gide':'Gide','vanallen':'Van Allen','imvigor':'IMvigor210','jung':'Jung'}
    w,h=720,60+34*(len(F)+1)+40; L,R,T=120,16,20; a,b=-2.0,3.0; sx=scale(a,b,L,w-R); y1=h-46
    o=f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="Forest plot of adjusted coefficients per cohort">'+xaxis(sx,T,y1,a,b,'Standardized adjusted coefficient for MVP, 95% CI')
    o+=f'<line class="zero" x1="{sx(0):.1f}" x2="{sx(0):.1f}" y1="{T}" y2="{y1}"/>'
    def row(y,lab,ba,la,ha,bc,lc,hc,bold=False):
        s=f'<text class="{"rb" if bold else "rl"}" x="{L-10}" y="{y+4}" text-anchor="end">{esc(lab)}</text>'
        for cls,e,lo,hi,dy,nm in (('s1',ba,la,ha,-6,'ISG.RS'),('s2',bc,lc,hc,6,'IFNG.GS')):
            yy=y+dy; lo2,hi2=max(a,lo),min(b,hi)
            s+=f'<g class="hov" data-tip="{esc(lab)}, {nm}: β {e:+.2f} (CI {lo:+.2f} to {hi:+.2f})"><rect x="{sx(lo2):.1f}" y="{yy-8}" width="{sx(hi2)-sx(lo2):.1f}" height="16" fill="transparent"/><line class="{cls}l" x1="{sx(lo2):.1f}" x2="{sx(hi2):.1f}" y1="{yy}" y2="{yy}"/>'
            s+=(f'<rect class="{cls}" x="{sx(e)-6:.1f}" y="{yy-6}" width="12" height="12" transform="rotate(45 {sx(e):.1f} {yy})"/>' if bold else f'<circle class="{cls} ring" cx="{sx(e):.1f}" cy="{yy}" r="5"/>')+'</g>'
        return s
    y=T+24
    for f in F:
        o+=row(y,f"{names[f['name']]} (n={f['n']})",f['ba'],f['ba']-1.96*f['sa'],f['ba']+1.96*f['sa'],f['bc'],f['bc']-1.96*f['sc'],f['bc']+1.96*f['sc']); y+=34
    p=D['pool']; o+=f'<line class="sep" x1="10" x2="{w-R}" y1="{y-14}" y2="{y-14}"/>'
    o+=row(y+4,'Pooled',p['ba'][0],p['ba'][1],p['ba'][2],p['bc'][0],p['bc'][1],p['bc'][2],True)
    return o+'</svg>'
def fig3():
    o='<div class="grid3">'
    for n in D['nulls']:
        w,h=340,172; L,R,T=78,14,34; v=n['bg']+n['isg']+n['ifng']+n['d'][:3]; a=min(v);b=max(v);pad=(b-a)*.07;a-=pad;b+=pad; sx=scale(a,b,L,w-R); y1=h-46
        s=f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{esc(n["name"])}: MVP Delta versus null"><text class="pt" x="4" y="16">{esc(n["name"])}</text><text class="pv" x="{w-R}" y="16" text-anchor="end">{n["pct"]:.0f}th percentile</text>'+xaxis(sx,T,y1,a,b,'Δ = β(ISG.RS) − β(IFNG.GS)')
        s+=f'<line class="zero" x1="{sx(0):.1f}" x2="{sx(0):.1f}" y1="{T}" y2="{y1}"/>'
        y=T+12
        for lab,q,c in (('All genes',n['bg'],'s0'),('ISG.RS genes',n['isg'],'s1'),('IFNG.GS genes',n['ifng'],'s2')):
            s+=f'<g class="hov" data-tip="{lab}: 10th {q[0]:+.2f}, median {q[1]:+.2f}, 90th {q[2]:+.2f}"><text class="rl" x="{L-6}" y="{y+4}" text-anchor="end">{lab}</text><line class="{c}b" x1="{sx(q[0]):.1f}" x2="{sx(q[2]):.1f}" y1="{y}" y2="{y}"/><rect class="surf" x="{sx(q[1])-3:.1f}" y="{y-7}" width="6" height="14"/><rect class="{c}" x="{sx(q[1])-2:.1f}" y="{y-6}" width="4" height="12" rx="1"/></g>'
            y+=20
        xd=sx(n['d'][0]); s+=f'<line class="mvpl" x1="{xd:.1f}" x2="{xd:.1f}" y1="{T}" y2="{y1}"/><g class="hov" data-tip="MVP: Δ {n["d"][0]:+.2f} (CI {n["d"][1]:+.2f} to {n["d"][2]:+.2f})"><rect class="mvp" x="{xd-5:.1f}" y="{T-6}" width="10" height="10" transform="rotate(45 {xd:.1f} {T-1})"/></g>'
        o+=s+'</svg>'
    return o+'</div>'
def fig4():
    o='<div class="grid2 two">'
    for k,t in (('lung','Lung malignant, 21 patients'),('mel','Melanoma malignant, 14 patients')):
        P=D['patients'][k]; w,h=360,330; L,R,T,B=48,14,28,48; a,b=-.1,.6; sx=scale(a,b,L,w-R); sy=scale(a,b,h-B,T)
        s=f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{esc(t)}"><text class="pt" x="{L}" y="16">{esc(t)}</text>'+xaxis(sx,T,h-B,a,b,'Within-patient ρ, MVP vs ISG.RS')+yaxis(sy,L,w-R,a,b,'ρ, MVP vs IFNG.GS')
        s+=f'<line class="zero" x1="{sx(a):.1f}" y1="{sy(a):.1f}" x2="{sx(b):.1f}" y2="{sy(b):.1f}"/><text class="note" x="{sx(.5):.1f}" y="{sy(.5)+18:.1f}" text-anchor="end">equal</text>'
        for p in P:
            s+=f'<g class="hov" data-tip="{esc(p["patient"])}, {p["n"]} cells: ρ ISG.RS {p["rho_a"]:+.2f}, ρ IFNG.GS {p["rho_c"]:+.2f}"><circle cx="{sx(p["rho_a"]):.1f}" cy="{sy(p["rho_c"]):.1f}" r="11" fill="transparent"/><circle class="s0 ring" cx="{sx(p["rho_a"]):.1f}" cy="{sy(p["rho_c"]):.1f}" r="5"/></g>'
        o+=s+'</svg>'
    return o+'</div>'
def table(hdr,rows,cap=None,strong=()):
    o='<div class="tw"><table>'+(f'<caption>{cap}</caption>' if cap else '')+'<thead><tr>'+''.join(f'<th>{h}</th>' for h in hdr)+'</tr></thead><tbody>'
    for i,r in enumerate(rows):
        o+=f'<tr{" class=hl" if i in strong else ""}>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>'
    return o+'</tbody></table></div>'
M='−'
verdict=table(['Test','Label','β ISG.RS','β IFNG.GS','Δ (95% CI)','Genome percentile'],[
 ['Bulk screen: 7 ICB cohorts, 686 patients','ACUTE (unstable)',M+'0.06','+1.05',M+'1.09 ('+M+'1.64, '+M+'0.54)','7.6'],
 ['<b>Verdict: lung malignant cells, 21 patients</b>','<b>ACUTE, not specific</b>','+0.035','+0.17',M+'0.11 ('+M+'0.18, '+M+'0.05)','29'],
 ['Replication: melanoma malignant cells, 14 patients','BOTH/UNRESOLVED','+0.11','+0.20',M+'0.09 ('+M+'0.22, +0.04)','64'],
 ['Mouse chromatin lookup (context only)','Negative','','','','']],strong=(1,))
spec=table(['Bulk specification','Label','Δ (95% CI)'],[['Primary','ACUTE',M+'1.09 ('+M+'1.64, '+M+'0.54)'],['TMB added (5 cohorts)','ACUTE',M+'0.97 ('+M+'1.43, '+M+'0.51)'],['ISG.RS, 24 Hallmark genes only','ACUTE',M+'1.00 ('+M+'1.49, '+M+'0.52)'],['No covariates','BOTH/UNRESOLVED',M+'0.30 ('+M+'0.63, +0.04)'],['ssGSEA scoring','BOTH/UNRESOLVED',M+'0.46 ('+M+'1.02, +0.11)'],['Hallmark IFN-α vs IFN-γ','NEITHER','+0.01 ('+M+'1.20, +1.22)'],['ISG.RS minus IFNG.GS as one predictor','no association','β +0.09 ('+M+'0.08, +0.25)']])
sc=table(['Compartment','Patients','Label','Δ (95% CI)','Genome percentile'],[['Lung malignant','21','ACUTE',M+'0.11 ('+M+'0.18, '+M+'0.05)','29'],['Lung malignant, depth adjusted','21','ACUTE',M+'0.09 ('+M+'0.14, '+M+'0.03)','9.7'],['Lung primary tumor, tS labels included','13','ACUTE',M+'0.10 ('+M+'0.18, '+M+'0.02)','25'],['Lung brain metastases','10','BOTH/UNRESOLVED',M+'0.06 ('+M+'0.13, 0.00)','54'],['Lung lymph node metastases','7','ACUTE',M+'0.21 ('+M+'0.38, '+M+'0.05)','17'],['Lung myeloid','57','ACUTE',M+'0.10 ('+M+'0.14, '+M+'0.06)','16'],['Melanoma malignant','14','BOTH/UNRESOLVED',M+'0.09 ('+M+'0.22, +0.04)','64'],['Melanoma macrophage','1','UNUSABLE','','']])
epi=table(['Check (mouse B16/Res499)','Mvp','Program genes'],[['Strict memory-domain list','Absent','Oas1a, Oas1g, Ifit1, Ifit3, Usp18 present'],['Nearest memory domain to TSS','730 kb','not measured'],['Promoter accessibility gain, percentile','39th','Oas1a 94th, Irf7 97th'],['Promoter accessibility, STAT1 dependence','63rd','Oas1a 100th, Ifit1 99th'],['RNA drop with STAT1 knockout','about 13%','3- to 5-fold'],['Accessibility-to-RNA coupling rank','18,993 of 21,069','Oas1g 1st, Oas1a 17th'],['H3K4me1 gain at promoter, percentile','79th, small, STAT1 independent','Oas1g 82nd, Irf7 94th']])
tcga=table(['TCGA tumor','n','Δ','SE','Genome percentile'],[['THCA ("immune-hot" literature)','497',M+'1.57','0.17','8'],['PAAD ("immune-evasive" literature)','177',M+'0.82','0.33','18'],['LIHC ("immune-evasive" literature)','366',M+'0.65','0.23','18'],['LUSC','484',M+'0.83','0.22','3'],['LUAD','510',M+'0.24','0.22','23'],['SKCM, primary tumors only','76','+0.65','0.66','72']])
CSS=''':root{color-scheme:light;--bg:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--ink3:#73726c;--rule:#e4e3dd;--grid:#ecebe6;--panel:#f4f3ef;--s1:#2a78d6;--s2:#eb6834;--s0:#8a8983;--mark:#0b0b0b}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){color-scheme:dark;--bg:#1a1a19;--ink:#f0efec;--ink2:#c3c2b7;--ink3:#9d9c92;--rule:#3a3a37;--grid:#2c2c2a;--panel:#242422;--s1:#3987e5;--s2:#d95926;--s0:#8f8e87;--mark:#f0efec}}
:root[data-theme="dark"]{color-scheme:dark;--bg:#1a1a19;--ink:#f0efec;--ink2:#c3c2b7;--ink3:#9d9c92;--rule:#3a3a37;--grid:#2c2c2a;--panel:#242422;--s1:#3987e5;--s2:#d95926;--s0:#8f8e87;--mark:#f0efec}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
main{max-width:860px;margin:0 auto;padding:32px 16px 72px}h1{font-size:30px;line-height:1.2;margin:0 0 10px;letter-spacing:-.01em}h2{font-size:20px;margin:42px 0 8px;padding-top:18px;border-top:1px solid var(--rule)}
.sub{color:var(--ink2);margin:0 0 22px}p{margin:10px 0}ul{padding-left:20px;margin:8px 0}li{margin:6px 0}.answer{background:var(--panel);border-radius:8px;padding:14px 18px;margin:18px 0}.answer p:first-child{margin-top:0}.answer p:last-child{margin-bottom:0}
figure{margin:18px 0}figcaption{color:var(--ink2);font-size:14px;margin-top:6px}svg{width:100%;height:auto;display:block;overflow:visible}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:18px}.grid3{display:grid;grid-template-columns:1fr;gap:14px;max-width:620px}@media(max-width:560px){.grid2{grid-template-columns:1fr}}
.tw{overflow-x:auto;margin:14px 0}table{border-collapse:collapse;width:100%;font-size:14px;font-variant-numeric:tabular-nums}th{text-align:left;color:var(--ink2);font-weight:600;border-bottom:1px solid var(--rule);padding:7px 10px 7px 0;white-space:nowrap}td{padding:7px 10px 7px 0;border-bottom:1px solid var(--grid);vertical-align:top}tr.hl td{background:var(--panel)}tr.hl td:first-child{padding-left:8px}
.legend{display:flex;gap:18px;flex-wrap:wrap;font-size:14px;color:var(--ink2);margin:10px 0 2px}.key{display:inline-block;width:11px;height:11px;border-radius:50%;margin-right:6px;vertical-align:-1px}
.grid{stroke:var(--grid);stroke-width:1}.zero{stroke:var(--ink3);stroke-width:1;stroke-dasharray:3 3}.sep{stroke:var(--rule)}.tick{fill:var(--ink3);font-size:11px}.axl{fill:var(--ink2);font-size:11.5px}.pt{fill:var(--ink);font-size:13px;font-weight:600}.pv{fill:var(--ink2);font-size:12px}.rl{fill:var(--ink2);font-size:12px}.rb{fill:var(--ink);font-size:12.5px;font-weight:600}.note{fill:var(--ink3);font-size:11px}
.s1{fill:var(--s1)}.s2{fill:var(--s2)}.s0{fill:var(--s0)}.s1l{stroke:var(--s1);stroke-width:2}.s2l{stroke:var(--s2);stroke-width:2}.s0b{stroke:var(--s0);stroke-width:8;stroke-opacity:.45;stroke-linecap:round}.s1b{stroke:var(--s1);stroke-width:8;stroke-opacity:.45;stroke-linecap:round}.s2b{stroke:var(--s2);stroke-width:8;stroke-opacity:.45;stroke-linecap:round}.ring{stroke:var(--bg);stroke-width:2}.surf{fill:var(--bg)}.mvp{fill:var(--mark)}.mvpl{stroke:var(--mark);stroke-width:2}
.hov{cursor:default}#tip{position:fixed;pointer-events:none;background:var(--ink);color:var(--bg);font-size:13px;padding:5px 8px;border-radius:4px;max-width:280px;display:none;z-index:9}code{font-size:.92em}'''
BODY=f'''<main>
<h1>MVP did not partition with the chronic interferon program</h1>
<p class="sub">Partition analysis on public data, run 2026-11-06. Predictions were committed to git before any expression value was read.</p>
<div class="answer"><p><b>The prediction failed.</b> It said MVP would track the chronic set (ISG.RS) more than the acute set (IFNG.GS) inside malignant cells. No dataset, model, or compartment came out chronic.</p>
<p><b>What the data shows instead:</b> MVP rises with interferon state in malignant cells, more than most genes do, but does not choose between the two programs. It also shows no anti-correlation, which was the containment prediction.</p></div>
{verdict}
<p><b>How to read it.</b> Δ below zero leans acute, above zero leans chronic. A label counts as specific only at the 90th genome percentile or higher for chronic, or the 10th or lower for acute, since an average gene has a negative Δ here too.</p>
<h2>What this does to the hypothesis</h2>
<ul><li><b>Signaling-brake layer:</b> the committed abandonment condition is met for "MVP is a member of the chronic program." This test can only speak to that claim.</li>
<li><b>Containment layer:</b> its only testable prediction here, anti-correlation with both sets, failed. Containment as a physical function is untouched, because this test cannot reach it.</li>
<li><b>Published contradictions:</b> the hoped-for resolution did not appear. Thyroid, pancreas, and liver all sit on the same side of the axis (section 5).</li></ul>
<div class="answer"><p><b>Watch for a third absorption.</b> Transcript co-variation cannot see a protein-level action, so MVP's reported STAT1 inhibition is neither supported nor refuted. That is true, and it is also the sentence a dying hypothesis would say. If the chronic-program idea continues, it needs a new prediction that can fail, ideally MVP knockout with an interferon-output readout.</p></div>
<h2>1. Chromatin: no memory signature in the mouse model</h2>
<p>Qiu 2023 deposited chromatin data (GSE219179). This is one mouse melanoma line, so it is context. It agrees with the human result.</p>{epi}
<h2>2. Bulk screen: acute under the primary model, but unstable</h2>
<figure><div class="legend"><span><i class="key" style="background:var(--s1)"></i>ISG.RS (chronic)</span><span><i class="key" style="background:var(--s2)"></i>IFNG.GS (acute)</span><span>Diamond: pooled estimate</span></div>{fig2()}<figcaption>Adjusted coefficients with both signatures and purity, myeloid, and lymphoid covariates in one model. Hover for values. IFNG.GS has a VIF of 11 to 23, so coefficients above 1 reflect collinearity and should not be read as magnitudes.</figcaption></figure>
{spec}
<p>The plan requires saying so if the ratio and the adjusted model disagree. <b>They disagree</b>, so the bulk ACUTE magnitude should not be believed. What holds throughout is that β(ISG.RS) spans zero in every model that estimates it, and no Δ is significantly above zero.</p>
<figure><div class="legend"><span><i class="key" style="background:var(--s1)"></i>ISG.RS panels</span><span><i class="key" style="background:var(--s2)"></i>IFNG.GS panels</span></div>{fig1()}<figcaption>Unadjusted MVP against each signature in the two largest cohorts. MVP is removed from IFNG.GS before scoring, and an assertion aborts the run otherwise.</figcaption></figure>
<h2>3. Single cell: the test that decides</h2>
<figure>{fig4()}<figcaption>Each dot is one patient. Dots above the dashed line track IFNG.GS more than ISG.RS. Nearly all are positive on both axes, which is the "interferon-linked, not selective" pattern. Unadjusted within-patient correlations; the verdict uses the adjusted model.</figcaption></figure>
{sc}
<h2>4. Could this test have found a chronic gene?</h2>
<p>Yes. Δ separates held-out ISG.RS members from IFNG.GS members with AUC 0.78 to 0.79 in malignant cells. MVP's Δ falls at the 11th percentile of ISG.RS members in lung and the 30th in melanoma, well below most genes the test identifies as chronic.</p>
<figure><div class="legend"><span>Bars: 10th to 90th percentile, tick at median</span><span>Black diamond and line: MVP</span></div>{fig3()}<figcaption>MVP's Δ against all genes and held-out signature members. Scales differ per panel. One sensitivity note: adjusting for sequencing depth moves lung to the 9.7th percentile, across the 10th-percentile line for "specific."</figcaption></figure>
<p><b>The one real positive:</b> in lung malignant cells MVP's coefficient is at the 95th genome percentile for ISG.RS and 88th for IFNG.GS. In melanoma, 97th and 78th. Absolute effects are small.</p>
<h2>5. Exploratory results</h2>
<p><b>Do the published contradictions resolve on this axis? No.</b> The "immune-evasive" and "immune-hot" tumor types land on the same side, with thyroid furthest from chronic.</p>{tcga}
<p><b>ICB response:</b> no pooled association, log odds ratio per SD +0.04 ({M}0.30, +0.38). Liu and IMvigor210 reached nominal significance in opposite directions and neither survives multiple-testing correction.</p>
<h2>6. Corrections to the plan, and limits</h2>
<ul><li><b>MVP is in Benci's IFNG.GS</b>, contrary to plan §6. That set is exactly Hallmark IFN-γ minus ISG.RS, so MVP landed there by construction and nobody tested it.</li>
<li><b>The two planned single-cell datasets are controlled access</b> (dbGaP phs002371, EGA EGAS00001005021). I used GSE131907 for lung and GSE115978 for melanoma. Lung malignant labels are mostly stage IV, and it is not an ICB cohort.</li>
<li><b>IFNG.GS came from patent claim text</b> (US12662705), since Benci's Table S1 was blocked. ISG.RS matched Qiu's source data at 38 of 38.</li>
<li><b>Correlative throughout.</b> MVP detected in about 54% of lung malignant cells. Melanoma has 14 usable patients; melanoma macrophages were unusable.</li>
<li><b>I drafted the pre-registered predictions</b> from the plan, and they are not your independent statement. You can add a dated dissent, which will not change what was frozen.</li></ul>
<h2>What is yours to decide</h2>
<ul><li><b>Accept the verdict, or apply for the controlled-access lung data?</b> Those datasets are the plan's original test and include earlier-stage lesions. Access takes an application, and I would expect the same answer.</li>
<li><b>Anything for you to check by eye:</b> Benci Table S1 in a browser, against the IFNG.GS list.</li></ul>
<p class="sub" style="margin-top:24px">Source: <code>~/projects/Vault</code> on xeric. Read <code>RESULTS.md</code>, then <code>PREREGISTRATION.md</code> and <code>DEVIATIONS.md</code>.</p>
</main><div id="tip"></div>
<script>(function(){{var t=document.getElementById('tip');document.addEventListener('mousemove',function(e){{var g=e.target.closest&&e.target.closest('[data-tip]');if(!g){{t.style.display='none';return}}t.textContent=g.getAttribute('data-tip');t.style.display='block';var x=Math.min(e.clientX+14,innerWidth-t.offsetWidth-8);t.style.left=x+'px';t.style.top=(e.clientY+14)+'px'}})}})();</script>'''
os.makedirs('results/page',exist_ok=True)
open('results/page/index.html','w').write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>MVP Partition Results</title><style>{CSS}</style></head><body>{BODY}</body></html>')
print(os.path.getsize('results/page/index.html'))
