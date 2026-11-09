#!/usr/bin/env python3
"""Tier 0a step 1, take three: MVP CDS from Ensembl FTP static dumps.
The REST homology endpoint failed three distinct ways tonight (HTML pages, HTTP 500
on 36/90 calls, then total failure on all 9 species). Our own Tier 0a instruction
said to use a local dump; this is that. Registered at 06dd589."""
import gzip, io, re, urllib.request, pathlib, sys, time
SP={'homo_sapiens':'human','rattus_norvegicus':'rat','canis_lupus_familiaris':'dog',
    'bos_taurus':'cow','ovis_aries':'sheep','equus_caballus':'horse',
    'oryctolagus_cuniculus':'rabbit','monodelphis_domestica':'opossum',
    'gallus_gallus':'chicken','xenopus_tropicalis':'xenopus'}
BASE='https://ftp.ensembl.org/pub/current_fasta'
UA={'User-Agent':'vault-reassessment/1.0 (research script)'}
OUT=pathlib.Path('/tmp/claude-1000/-home-graham-projects/46738ac0-1f6d-4b80-81fe-caa9aa37b1a5/scratchpad/t0')
FA=OUT/'mvp_cds.fna'; FA.write_text('')

def fetch(url, to=300):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=to)

for sp, short in SP.items():
    t0=time.time()
    try:
        idx=fetch(f'{BASE}/{sp}/cds/', 60).read().decode('utf8','replace')
        m=re.search(r'href="([^"]*cds\.all\.fa\.gz)"', idx)
        if not m: print(f'  {short:9s} no cds.all file listed', flush=True); continue
        url=f'{BASE}/{sp}/cds/{m.group(1)}'
        # stream-decompress and stop as soon as MVP's records are past
        best=('',0); name=None; buf=[]; seen=False
        with fetch(url, 600) as r, gzip.GzipFile(fileobj=r) as gz:
            for raw in io.TextIOWrapper(gz, encoding='utf8', errors='replace'):
                if raw.startswith('>'):
                    if name and buf:
                        s=''.join(buf)
                        if len(s)>best[1] and len(s)%3==0: best=(s,len(s))
                    hit = re.search(r'gene_symbol:MVP\b', raw, re.I) is not None
                    if hit: seen=True
                    elif seen and best[1]: break      # past the MVP block
                    name = raw if hit else None; buf=[]
                elif name: buf.append(raw.strip())
            if name and buf:
                s=''.join(buf)
                if len(s)>best[1] and len(s)%3==0: best=(s,len(s))
        if best[1]:
            with FA.open('a') as fh: fh.write(f'>{short}\n{best[0]}\n')
            print(f'  {short:9s} CDS {best[1]:5d} nt  ({best[1]//3} codons)  {time.time()-t0:5.1f}s', flush=True)
        else:
            print(f'  {short:9s} no gene_symbol:MVP CDS found  {time.time()-t0:5.1f}s', flush=True)
    except Exception as e:
        print(f'  {short:9s} {type(e).__name__}: {str(e)[:50]}  {time.time()-t0:5.1f}s', flush=True)
print(f'\n  {FA.read_text().count(">")} sequences -> {FA}', flush=True)
