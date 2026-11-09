#!/usr/bin/env python3
"""Find a species' MVP CDS by PROTEIN MATCH rather than gene symbol, because
invertebrate genomes do not annotate MVP by symbol (Ciona: 0 hits for gene_symbol:MVP
against 205 symbols present). Uses the orthogroup protein we already hold as the query."""
import gzip, io, json, re, urllib.request, pathlib, sys, time
UA={'User-Agent':'vault-reassessment/1.0 (research script)'}
S=pathlib.Path('/tmp/claude-1000/-home-graham-projects/46738ac0-1f6d-4b80-81fe-caa9aa37b1a5/scratchpad/t0')
bases='TCAG'; aas='FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG'
CODON={b1+b2+b3:aas[i] for i,(b1,b2,b3) in enumerate((a,b,c) for a in bases for b in bases for c in bases)}
def tr(s): return ''.join(CODON.get(s[i:i+3].upper(),'X') for i in range(0,len(s)-2,3))

def kmers(s,k=5): return {s[i:i+k] for i in range(len(s)-k+1)}

TARGETS=[('7719','ciona','https://ftp.ensembl.org/pub/current_fasta/ciona_intestinalis/cds/'),
         ('7739','branchiostoma','https://ftp.ensemblgenomes.ebi.ac.uk/pub/current/metazoa/fasta/branchiostoma_lanceolatum/cds/')]

og=json.load(open('argon/raw/eggnog_raw_alg_2QPP0.json'))['raw_alg']
prot={}
for p in og.split('>')[1:]:
    l=p.split('\n'); prot[l[0].strip()]=''.join(l[1:]).replace('-','').replace('.','')

for taxid, short, url in TARGETS:
    q=[v for k,v in prot.items() if k.startswith(taxid+'.')]
    if not q: print(f"  {short}: taxid {taxid} not in the orthogroup"); continue
    q=max(q, key=len); qk=kmers(q)
    print(f"  {short}: query is the orthogroup protein, {len(q)} aa", flush=True)
    t0=time.time()
    try:
        idx=urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read().decode('utf8','replace')
        f=re.search(r'href="([^"]*cds\.all\.fa\.gz)"', idx)
        if not f: print(f"    no cds.all listed"); continue
        best=(0.0,None,None)
        with urllib.request.urlopen(urllib.request.Request(url+f.group(1), headers=UA), timeout=900) as r, \
             gzip.GzipFile(fileobj=r) as gz:
            name=None; buf=[]
            for raw in io.TextIOWrapper(gz, encoding='utf8', errors='replace'):
                if raw.startswith('>'):
                    if name and buf:
                        c=''.join(buf)
                        if len(c)%3==0 and 0.6*len(q)*3 <= len(c) <= 1.6*len(q)*3:
                            p2=tr(c).rstrip('*')
                            if '*' not in p2:
                                j=len(qk & kmers(p2))/max(1,len(qk | kmers(p2)))
                                if j>best[0]: best=(j,name.split()[0][1:],c)
                    name=raw.strip(); buf=[]
                else: buf.append(raw.strip())
            if name and buf:
                c=''.join(buf)
                if len(c)%3==0:
                    p2=tr(c).rstrip('*')
                    if '*' not in p2:
                        j=len(qk & kmers(p2))/max(1,len(qk | kmers(p2)))
                        if j>best[0]: best=(j,name.split()[0][1:],c)
        if best[1]:
            print(f"    best match: {best[1]}  5-mer Jaccard {best[0]:.3f}  CDS {len(best[2])} nt "
                  f"({len(best[2])//3} codons)  {time.time()-t0:.0f}s", flush=True)
            (S/f'{short}_cds.fna').write_text(f">{short}\n{best[2]}\n")
        else: print(f"    no usable CDS found  {time.time()-t0:.0f}s", flush=True)
    except Exception as e:
        print(f"    {type(e).__name__}: {str(e)[:60]}  {time.time()-t0:.0f}s", flush=True)
