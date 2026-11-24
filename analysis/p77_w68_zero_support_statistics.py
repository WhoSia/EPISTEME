"""W68: sensitivity to a zero-positive query in the original published workbook.

Use artifact_tool to read the pinned XLSX, not a spreadsheet reconstructed
from the printed paper. All model identities remain ambiguous: geo-gpt4
sheet rows say Llama3. This is a conditional workbook replay.
"""
import hashlib, json, sys, zipfile
from pathlib import Path
from p77_w68_label_rule_replay import SHA, records
from artifact_tool import Blob, SpreadsheetFile
import numpy as np
from scipy.stats import f, friedmanchisquare

XLSX_SHA = '3c95456d42326dba210c0943489988895ffeba2ac09eb3d0e84124e54fcfb935'
ROW_GROUPS = ((5,6,7),(18,19,20),(26,27,28))

def calculate(matrix):
    x=np.asarray(matrix,dtype=float)
    if x.ndim!=2 or x.shape[0]<2 or x.shape[1]!=3 or not np.isfinite(x).all() or ((x<0)|(x>1)).any():
        raise ValueError('Expected finite recall triples in [0,1]')
    n,k=x.shape
    grand=x.mean()
    ss_m=n*((x.mean(axis=0)-grand)**2).sum()
    residual=x-x.mean(axis=0)-x.mean(axis=1)[:,None]+grand
    ss_e=(residual**2).sum()
    if ss_e<=0: raise ValueError('No estimable residual variance')
    stat=(ss_m/(k-1))/(ss_e/((n-1)*(k-1)))
    fr=friedmanchisquare(*x.T)
    return {'means':x.mean(axis=0).tolist(),'F':float(stat),'df':[k-1,(n-1)*(k-1)],'p':float(f.sf(stat,k-1,(n-1)*(k-1))), 'friedman':float(fr.statistic),'friedman_p':float(fr.pvalue)}

def audit(zip_path,xlsx_path):
    for path,expected in ((zip_path,SHA),(xlsx_path,XLSX_SHA)):
        if hashlib.sha256(Path(path).read_bytes()).hexdigest()!=expected: raise ValueError('Pinned source SHA mismatch')
    with zipfile.ZipFile(zip_path) as z:
        if z.testzip() is not None: raise ValueError('ZIP CRC mismatch')
        labels=z.read('Data/annotated_800_geo_simple_ovary.txt').decode('utf-8-sig').splitlines()
        rows=records(z.read('Data/ovarian_cancer_gpt4_geo_output.json'))
        if len(labels)!=800 or len(rows)!=800: raise ValueError('Expected 800 rows')
        pos=labels.count('blood')
        hits={layer:sum(r[layer].get('tissue')=='blood' for r in rows) for layer in ('BioSample','LLM','LLM+CEDAR')}
    w=SpreadsheetFile.import_xlsx(Blob.load(str(xlsx_path)))
    a=w.worksheets.get_item('geo-gpt4').get_range('A1:H28').values
    matrix=[[a[r-1][c] for r in group] for group in ROW_GROUPS for c in (2,6)]
    if pos!=0 or any(hits.values()) or matrix[1]!=[0,0,0]: raise ValueError('Pinned zero-support witness not reproduced')
    return {'zip_sha256':SHA,'xlsx_sha256':XLSX_SHA,'released_blood_positive_labels':pos,
            'released_blood_exact_retrieval_counts':hits,'workbook_sheet':'geo-gpt4',
            'workbook_method_cell_labels':[a[r-1][0] for r in ROW_GROUPS[0]],
            'workbook_recall_matrix':matrix,'zero_support_recall_cells':'G5:G7',
            'all_six':calculate(matrix),'omit_ovarian_blood':calculate(matrix[:1]+matrix[2:]),
            'warning':'Undefined recall (0/0) for released ovarian GEO blood. Zero-filling can be an explicit convention; no author run/cell linkage established. Omitting this row is a sensitivity analysis, not a correction of the paper. Sheet title and row model labels disagree.'}

if __name__=='__main__': print(json.dumps(audit(sys.argv[1],sys.argv[2]),indent=2))
