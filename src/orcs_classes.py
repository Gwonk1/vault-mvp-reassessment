"""Assign BioGRID ORCS screens to condition classes using index fields only. No gene data is read."""
import re
import pandas as pd

INDEX = 'data/raw/orcs/screens/BIOGRID-ORCS-SCREEN_INDEX-2.0.18.index.tab.txt'
GENOTOX = r'cisplatin|oxaliplatin|carboplatin|etoposide|camptothecin|irinotecan|topotecan|doxorubicin|daunorubicin|epirubicin|mitoxantrone|gemcitabine|hydroxyurea|temozolomide|fluorouracil|5-fu|olaparib|niraparib|talazoparib|rucaparib|veliparib|parp|azd6738|ceralasertib|berzosertib|ve-?82[12]|m3541|m6620|mms|methyl methane|mitomycin|bleomycin|cytarabine|ara-?c|formaldehyde|azd1390|ku-?\d+|atr inhib|atm inhib|wee1|adavosertib|azd1775|prexasertib|aphidicolin|melphalan|chlorambucil|busulfan|\buv\b|ultraviolet|radiation|irradiat|illudin|trabectedin|calicheamicin|duocarmycin|mnng|kbro3|benzo\[a\]pyrene|bpde|rabusertib|azd0156|thioparib|cpd.391|pyridostatin|phen-dc3|dexrazoxane'
OXID = r'hydrogen peroxide|h2o2|antimycin|oligomycin|rsl3|erastin|ml-?162|ml-?210|ferroptosis|paraquat|rotenone|piericidin|menadione|hypoxia|tert-butyl|selenocystine'
PROTEO = r'bortezomib|carfilzomib|ixazomib|mg-?132|thapsigargin|tunicamycin|brefeldin|cb-?5083|heat shock|proteotoxic|hsp90'
IFN = r'interferon|\bifn'
KILL = r'\btil\b|t cell|nk \(|natural killer|checkpoint|pd-?1|pd-?l1'
TRAFFIC = r'protein transport|lysosome homeostasis|vesicle distribution|protein/peptide distribution'
AUTO = r'autophag|mitophag'


def classify(r):
    cond = str(r.CONDITION_NAME).lower()
    setup = str(r.EXPERIMENTAL_SETUP).lower()
    pheno = str(r.PHENOTYPE).lower()
    why = str(r.SCREEN_RATIONALE).lower()
    if 'virus' in setup or pheno == 'response to virus' or cond.startswith('virus'):
        return 'virus'
    if 'bacteria' in setup or pheno == 'response to bacteria':
        return 'bacteria'
    if 'toxin' in setup or pheno == 'response to toxin':
        return 'toxin'
    if re.search(IFN, cond):
        return 'interferon'
    if 't cell' in setup or 'nk cell' in setup or re.search(KILL, cond) or re.search(KILL, why):
        return 'immune_killing'
    if 'implantation' in setup or pheno == 'tumorigenicity':
        return 'in_vivo'
    if 'radiation' in setup or re.search(GENOTOX, cond):
        return 'genotoxic'
    if 'oxygen' in setup or pheno == 'response to oxygen concentration' or re.search(OXID, cond) or re.search(OXID, why):
        return 'oxidative_mito'
    if re.search(PROTEO, cond):
        return 'proteotoxic'
    if 'cytokine' in setup or 'ligand' in setup:
        return 'other_cytokine_ligand'
    if re.search(AUTO, why) or re.search(TRAFFIC, pheno):
        return 'autophagy_traffic'
    if 'drug' in setup or pheno == 'response to chemicals':
        return 'other_drug'
    if setup == 'timecourse' and cond == '-':
        return 'baseline_fitness'
    return 'other'


def load_index():
    I = pd.read_csv(INDEX, sep='\t', dtype=str, quoting=3).rename(columns={'#SCREEN_ID': 'id'})
    for c in ['SCORES_SIZE', 'FULL_SIZE', 'NUMBER_OF_HITS']:
        I[c] = pd.to_numeric(I[c], errors='coerce')
    I['universe'] = (I.LIBRARY_METHODOLOGY.isin(['Knockout', 'Inhibition'])) & (I.SCORES_SIZE >= 10000) & (I.THROUGHPUT == 'High Throughput') & (I.NUMBER_OF_HITS > 0)
    I['cls'] = I.apply(classify, axis=1)
    return I


if __name__ == '__main__':
    I = load_index()
    U = I[I.universe]
    print('all', len(I), 'universe screens', len(U), 'papers', U.SOURCE_ID.nunique(), 'cell lines', U.CELL_LINE.nunique())
    t = U.groupby('cls').agg(screens=('id', 'size'), papers=('SOURCE_ID', 'nunique'), lines=('CELL_LINE', 'nunique'), med_hits=('NUMBER_OF_HITS', 'median')).sort_values('papers', ascending=False)
    print(t.to_string())
    for c in t.index:
        v = U[U.cls == c].CONDITION_NAME.value_counts()
        print('\n', c, dict(list(v.items())[:22]))
    print('\nother rationale', U[U.cls == 'other'].SCREEN_RATIONALE.value_counts().head(14).to_dict())
    print('\nother_drug top', U[U.cls == 'other_drug'].CONDITION_NAME.value_counts().head(60).index.tolist())
