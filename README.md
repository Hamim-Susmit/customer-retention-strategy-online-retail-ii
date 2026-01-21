# Project 5 — Customer Retention & Intervention Strategy (Data → Decisions)

Turn customer analytics into an actionable retention plan. This project builds a complete, reproducible pipeline to segment customers by churn risk and value, recommend interventions, simulate ROI under budget constraints, and export an action list for business teams.

## Why this project matters
Retention programs only work when they focus on the right customers with clear, measurable ROI. This repo moves from raw transaction data to an optimized action plan in one command, giving stakeholders a practical playbook for intervention.

## Dataset
- **Source:** Online Retail II (UCI)
- **Expected location:** `data/raw/online_retail_II.xlsx`
- **Sheets:** handles `Year 2009-2010`, `Year 2010-2011`, or any sheets found

> The dataset is not included in this repo. Place the file at `data/raw/online_retail_II.xlsx` before running the pipeline.

## One-command pipeline
```bash
python scripts/run_pipeline.py --input data/raw/online_retail_II.xlsx --outdir reports
```

The script will:
1. Load and clean transactions
2. Build customer features
3. Score churn risk and value
4. Assign segments and interventions
5. Simulate ROI scenarios (including a budget-optimized plan)
6. Export CSVs and charts to `reports/`

## Outputs
**Exports** (generated in `reports/`):
- `customer_action_list.csv` — customer-level metrics + action recommendations
- `simulation_summary.csv` — scenario-level ROI summary

**Figures** (generated in `reports/figures/`):
- `churn_risk_distribution.png`
- `value_distribution.png`
- `action_matrix.png`
- `roi_by_scenario.png`

> Add screenshots of the figures here after running the pipeline.

## Methods summary
**Cleaning**
- Normalizes column names
- Drops missing customer IDs
- Removes cancellations (invoice prefix `C`)
- Drops non-positive quantities, prices, or line totals

**Feature Engineering**
- Recency, frequency, monetary value, average order value
- Purchase span and dominant country

**Risk & Value Scoring**
- Risk proxy combines recency and inverse frequency (scaled + sigmoid)
- Value score combines monetary total and average order value

**Segmentation** (2x2 matrix)
- **Save:** high risk, high value
- **Protect:** low risk, high value
- **Nurture:** high risk, low value
- **LetGo:** low risk, low value

**Interventions**
- Save → Discount10
- Protect → LoyaltyPerk
- Nurture → FreeShipping
- LetGo → NoAction

**ROI Simulation**
- Computes expected next-period revenue
- Applies action cost rules and lift assumptions
- Simulates multiple scenarios + greedy budget optimization

## Repository layout
```
customer-retention-strategy-online-retail-ii/
├── data/
│   ├── raw/                      # user puts xlsx here (not tracked)
│   └── processed/                # cleaned snapshots (local)
├── notebooks/
│   ├── 01_build_features.ipynb
│   ├── 02_risk_value_segmentation.ipynb
│   ├── 03_intervention_simulation.ipynb
│   └── 04_final_action_list.ipynb
├── reports/
│   ├── figures/
│   ├── customer_action_list.csv
│   └── simulation_summary.csv
├── src/
│   ├── __init__.py
│   ├── io.py
│   ├── cleaning.py
│   ├── features.py
│   ├── segmentation.py
│   ├── simulation.py
│   └── viz.py
├── scripts/
│   ├── run_pipeline.py
│   └── quickcheck.py
├── tests/
│   ├── test_cleaning.py
│   ├── test_features.py
│   ├── test_simulation.py
│   └── test_segmentation.py
├── .gitignore
├── requirements.txt
├── README.md
└── LICENSE
```

## Notebooks
Each notebook mirrors a phase of the pipeline and produces clean outputs:
1. **01_build_features.ipynb** — ingest + clean + feature table
2. **02_risk_value_segmentation.ipynb** — scores + action matrix
3. **03_intervention_simulation.ipynb** — ROI scenario comparison
4. **04_final_action_list.ipynb** — exports + business memo

## How to run tests
```bash
pytest
```

## Limitations & next steps
- The churn risk score is a proxy (no labels); consider fitting a supervised model if labels become available.
- Lift assumptions are deterministic; consider A/B test results or causal models for better estimates.
- Add channel-level segmentation or CLV models to refine targeting.

## Project series
This is **Project 5** in a 6-part series. Placeholder links:
- Project 1: [TBD](#)
- Project 2: [TBD](#)
- Project 3: [TBD](#)
- Project 4: [TBD](#)
- Project 6: [TBD](#)

## License
MIT License. See `LICENSE`.
