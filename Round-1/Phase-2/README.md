# Round 1 — Phase 2: Analytical Core

## Objective

Use the validated SQLite Social Engine database for the final selected SQL challenges.

## Authoritative questions

- Easy E2 — Most Engaged Posts
- Medium M1 — Which Locations Generate the Most Engagement?
- Hard H2 — Rank Users Within Their Location

`src/build_phase2_submission.py` is the authoritative source for the exact three read-only SQL queries and generates the final PDFs and output images in `submission/`. It opens `data/data_vortex.db` read-only for the selected analysis.

## Final submission artifacts

- SQL queries: `submission/Data_Vortex_Phase2_SQL_Queries.pdf`
- Executed output: `submission/Easy_Output.jpeg`, `Medium_Output.jpeg`, `Hard_Output.jpeg`
- Logic explanation: `submission/Data_Vortex_Phase2_Logic_Explanation.pdf`
- Insight report: `submission/Data_Vortex_Phase2_Insight_Report.pdf`
- Manifest: `submission/SUBMISSION_MANIFEST.txt`

## Reproduce

```powershell
python -m pip install -r ../Phase-1/requirements.txt
python src/load_sqlite.py
python src/build_phase2_submission.py
```

The loader reads the retained cleaned Phase 1 CSVs at `../Phase-1/data/cleaned/`; no duplicate clean-data copy is kept in Phase 2.
