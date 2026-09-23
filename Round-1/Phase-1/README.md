# Round 1 — Phase 1: Data Recovery and EDA

## Objective

Restore the supplied Social Engine data while preserving provenance, then perform exploratory data analysis.

## Data and methodology

`data/raw/` contains the original supplied CSVs. `src/clean_data.py` deterministically writes the cleaned CSVs in `data/cleaned/`: it removes exact duplicate post records, corrects confirmed negative-like sign inversions, standardizes timestamps and text, and preserves genuine missing values.

The forensic notebooks and reports record the inspection, corruption analysis, cleaning validation, reconciliation, data dictionary, and EDA. `notebooks/06_final_eda.ipynb` generates the final figures in `outputs/figures/`.

## Final deliverables

- Cleaned datasets: `data/cleaned/`
- Reproducible cleaning code: `src/clean_data.py`
- EDA report: `reports/EDA_Report.md`
- Final EDA notebook, summaries, and figures: `notebooks/06_final_eda.ipynb`, `outputs/summaries/`, `outputs/figures/`
- QA and reconciliation evidence: `reports/FINAL_PHASE1_QA.md` and related forensic reports

## Reproduce

```powershell
python -m pip install pandas numpy matplotlib
python src/clean_data.py
```

The raw files are retained as provenance evidence and are not modified by the pipeline.
