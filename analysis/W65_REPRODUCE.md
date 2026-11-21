# W65 reproducibility — source-hash and local test instructions

This is a **bounded conditional source-artifact audit**. It does **not** recreate original LLM calls, accession-keyed author labels, the manuscript's six run IDs, or the paper's published recall/precision/F1 statistics.

## Already-held primary data

Original Sundaram et al. Zenodo v2/v3 Data.zip: [Drive primary byte custody](https://drive.google.com/file/d/1aEtrveLusvUspkPJF-1t0UYrx5ZWYOBK/view), 3,992,768 bytes, SHA-256:

    bebd5b8771bd8e572f5efe7fe9c9f0177dcca98e874021b5fefbdd240f81595c

Avoid re-downloading from Zenodo if an exact SHA-matching local copy is already available. The ZIP contains original released model/source records plus the 800-line heuristic labels. No model response text or participant identifiers should be committed to GitHub.

## Python 3.10+ (stdlib)

From the repository root, with the original ZIP downloaded by the human owner from their Drive:

    python -m unittest discover -s analysis -p 'test_p77_w65_*.py' -v
    python analysis/p77_w65_query_parser_sensitivity.py "/path/to/Data.zip" > /tmp/w65-parser-receipt.json
    python analysis/p77_w65_rank_reversal_court.py /tmp/w65-parser-receipt.json > /tmp/w65-rank-receipt.json

On Windows PowerShell, quote the test glob with double quotes and choose any writable path rather than /tmp. All scripts must reject a ZIP not matching the pinned checksum.

Expected source-level invariants:
- 3 source cohorts, 800 heuristic labels in each.
- Original BioSample ovarian blood exact parser: 38 TP among 38 retrieved out of 154 relevant.
- Normalized BioSample ovarian blood: 153 TP among 153 retrieved.
- Original GPT4 CEDAR ovarian blood exact: 78 TP among 87 retrieved.
- Normalized GPT4 CEDAR ovarian blood: 103 TP among 112 retrieved.
- Strict sign reversal of raw-vs-CEDAR relative recall and F1: **2 of 108 pairwise metric comparisons**.
- Do not use these as the author's manuscript results.

The strict parser mirrors one public code example, not a verified production evaluator. It exact-matches dictionary field 'tissue' to the lowercased input query. The alternative parser only trims/case-folds strings and falls back to 'tissue_type'; it does **not** infer ontology terms or correct labels.

## A08 verification gate

    python analysis/p77_w65_provenance_gate.py reviewed_claims.json

A reviewed claims file must contain records for source→input, input→model invocation, invocation→output, output→query, query→confusion, confusion→workbook and workbook→publication. Execution-linked claims require independently verified run IDs and evidence links; the gate merely checks attestation *shape*. Passing the gate is not sufficient to establish scientific provenance. Never backfill missing claims with synthetic records as if they were authentic.

## State

Notion: [W65 evidence/missing-source procurement register](https://app.notion.com/p/41eef561cf92813caa0de210e2c49385). Scientific status: P77 identity REVIEW ACTIVE; S-BIAD602 independent AI/adoption case PAUSED; P78 and PAPER HOLD; **19 active evidence categories F7/A7/B5**. GitHub G-001 applies: no github-actions[bot] commits or contributor history.
