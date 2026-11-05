# EPISTEME-P77 W26 — Original ZIP Upstream Survey Export Court: Byte Drift or Epistemic Difference?

**Date:** 2026-11-05 KST. **Authority:** [P77 strategy](../STRATEGY_P77_CURRENT.md). **Status:** genuine source comparison PASS; actual semantic/test loss NOT ESTABLISHED; P77 ACTIVE / P78 & PAPER HOLD.
**Parent original:** [CRI-master.zip in actual EPISTEME Drive](https://drive.google.com/file/d/1qRL9_P6mV4nJaBMgxq3p60ShDa5p-NJY/view), SHA256 `64756bfe62b25cdd7dbea57d2b063cb0f564225751d1f0251b4879f426894098`. Source was locally unpacked in W23 with all ZIP CRC checks passed.
**Code:** [analysis/p77_w26_za2900_original_exports_precision_null.py](../analysis/p77_w26_za2900_original_exports_precision_null.py). A substantively equivalent local Python script was executed successfully using the original ZIP extraction and Pandas/Stata reader.

## 1. True source records and original byte differences

The same original CRI ZIP contains **two files named `ZA2900.csv`**, at `data/ZA2900.csv` and `data/Provided Materials/ZA2900.csv`, as well as byte-identical source `ZA2900.dta` files in corresponding folders. Previous provenance inspection had not compared the CSV pair.

- Root CSV: **41,208,574 bytes**, full SHA-256 `ea8f539c0fb7debc8c294dbcbfaef89aea466a80bf827b21d3dacd4a35716dcd`.
- Provided CSV: **41,203,230 bytes**, full SHA-256 `1dd010dc2b7f7abc62de583db7df4e5f2b264a883f0571bc2745f5a5444da659`.
- Both have **35,313 data rows × 194 columns**, exact same header and identical text in every column **except `v325`**.
- **7,488 row-cell strings in `v325` differ**, despite all other respondent-field strings being identical; first differing byte offset **6,542,672**.
- Numeric parse within `v325`: **16,218 numeric rows** in both files; **19,095 labeled nonnumeric rows** (e.g. `No weighting`) not compared against a numeric Stata column in this check.
- On numeric rows, the maximum absolute two-CSV discrepancy is **7.771561172376096×10^-16**. In raw Python floating-point comparisons some numeric floats are unequal bitwise (preliminary audit flagged 781), but **NONE exceed 10^-12 absolute tolerance**.
- The unmodified original `ZA2900.dta` (35,313×194) supplies the independent third encoding. For all **16,218 directly numeric-comparable v325 rows**, both CSV representations agree with Stata values within absolute tolerance `1e-12` (rtol=0).
- Root and Provided copies of all five `ZA*.dta` inspected are byte-identical; root and Provided `ZA4700.csv`, `ZA6900_v2-0-0.csv`, `cri_macro.csv` inspected are also byte-identical. `ZA2900.csv` is an exception in byte encoding.

## 2. Important correction of provisional diagnosis

The first string-level check initially said **781 numerical differences** based on `float(x) != float(y)`. That statement **MUST NOT** be treated as evidence of 781 changes in scientific values. On inspecting absolute differences against the original Stata representation, all numeric mismatches are within `8×10^-16` and therefore far below even `10^-12`. The strongest supported reading is **CSV float serialization/precision changes**, not a changed respondent measurement. The 19,095 nonnumeric labels were not matched semantically to the raw Stata values or version-specific codebook; do not claim full categorical equivalence.

No respondent rows or identifying survey records were printed or copied to open GitHub. The code reports only aggregate counts, hashes, and permissible source metadata. Survey upstream distribution remains subject to original GESIS/ISSP terms.

## 3. EPISTEME novelty/causal risk

The two source CSVs have different SHA256 despite numerical comparability. This is an authentic science-workflow encoding incident: **byte identity is stronger than needed for numeric equivalence, and numeric equivalence is weaker than proving equivalence of inferential claims**. These are well-known distinctions in numerical computing, data lineage and scientific reproducibility, not independent EPISTEME theory or evidence of AI caused loss of scientific tests. The converter used to create the two CSVs is **not identified**, and one cannot infer AI involvement.

A future controlled study must inspect the *intended inferential object* and actual formal source equivalence, not reject every byte change or blindly accept every matching number. The user-provided artifact is now a useful **negative control** for an eventual field-real converter benchmark and nothing more.

## 4. Distinct official source needs

The original ZIP already contains candidate original GESIS waves `ZA1490.dta, ZA1950.dta, ZA2900.dta, ZA4700.dta, ZA6900_v2-0-0.dta`, some CSV counterparts, and the original `issp1985_2016.dta`. It is **not necessary to demand another copy of the entire CRI ZIP or all five surveys** for model-table postprocessing. Official GESIS source-version byte hashes and third-party rights are still unverified if an exact independent *survey-source* replay is attempted. The present CRI ZIP contains **no assigned AI adapter treatment and no longitudinal scientific-community standard-adoption outcome**.

### Three new directly relevant PNAS critiques not verified as Drive originals

- [Mathur, Covington & VanderWeele (2023)](https://doi.org/10.1073/pnas.2218957120)
- [Engzell (2023)](https://doi.org/10.1073/pnas.2218530120)
- [Auspurg & Brüderl (2024)](https://doi.org/10.1073/pnas.2404035121)

They have official publicly readable full text but were not found by DOI/title in Drive. Their original PDF holdings are **pending**, not blockers for the actual completed numeric equivalence tests.

**W26 verdict:** Genuine CSV-byte discrepancy FOUND; substantive numeric difference FALSIFIED at 1e-12 in 16,218 comparable rows; scientific test admissibility and AI conversion causal link NOT ESTABLISHED. **P77 ACTIVE, P78 HOLD, PAPER HOLD.**
