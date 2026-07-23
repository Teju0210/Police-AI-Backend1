# KSP Crime Analytics Dashboard — Local Setup (VS Code)

## What's in this build
This build was upgraded to meet the SCRB "Advanced Visualization / Network Analysis / AI-Driven Predictive Dashboard" brief in full:

| Requirement | Where it lives |
|---|---|
| District-level drill-down (district → police station) | Map panel, section **01 · Geo Drill-down** — click any circle marker |
| Spatiotemporal clusters (time-of-day layered hotspots) | Heatmap panel, section **01** — Morning/Afternoon/Evening/Night toggle |
| Emerging trend alerts (red pulsing markers) | Pulsing red rings on the map for any district in the early-warning list |
| Relationship mapping / repeat-offender network | Section **05 · Network & Risk** — force-directed co-accused graph |
| Modus Operandi + cross-jurisdiction association detection | Section **06 · MO & Behaviour** — MO frequency + multi-district repeat-offender table |
| Socio-economic correlation ("why behind the where") | Section **07 · Socio-Economic** — crime rate vs urbanization/literacy/unemployment, with Pearson r |
| AI-driven predictive risk scoring | Section **08 · AI Forecast** — `RandomForestRegressor` forecasts next-period case volume per district, tiered High/Medium/Low |
| Anomaly detection | Section **09 · Anomalies** — `IsolationForest` flags individual incidents that deviate from normal district/crime-type/time patterns |
| Pattern & trend discovery (stats-based hotspots) | Sections 01, 02, 08 combined (heatmap + trend charts + forecast) |

Cinematic/interactive layer: animated boot sequence, count-up KPIs, scroll-reveal sections, pulsing hotspot markers, hover-glow panels, and a sticky in-page nav across all 10 sections.


## Project structure
```
ksp_analytics/
├── 1_generate_data.py       # synthetic data generator (swap for real DB pull later)
├── 2_build_analytics.py     # pandas + NetworkX analysis -> output/dashboard_data.json
├── 3_build_dashboard.py     # injects the JSON into the HTML template
├── dashboard_template.html  # editable dashboard source (charts, layout, styling)
├── requirements.txt
├── data/                    # generated CSVs land here
└── output/                  # dashboard_data.json + final dashboard.html land here
```

## 1. Install prerequisites
- **Python 3.9+** — check with `python3 --version`. Get it from python.org if missing.
- **VS Code** — install the **Python** extension (Microsoft) from the Extensions panel (`Ctrl+Shift+X` / `Cmd+Shift+X`).
- Optional but handy: the **Live Server** extension (Ritwick Dey) for auto-reloading the HTML as you edit it.

## 2. Open the project
```
code ksp_analytics
```
(or File → Open Folder… in VS Code)

## 3. Create a virtual environment
Open a terminal in VS Code (`` Ctrl+` ``) and run:
```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
VS Code should prompt "Select Interpreter" — pick the `.venv` one so it's used for every terminal/run going forward.

## 4. Run the pipeline
```bash
python 1_generate_data.py      # writes data/*.csv
python 2_build_analytics.py    # writes output/dashboard_data.json
python 3_build_dashboard.py    # writes output/dashboard.html
```
Or just click the ▶ Run button at the top-right of each file in VS Code (uses the same interpreter).

## 5. View the dashboard
- Simplest: right-click `output/dashboard.html` in the VS Code file explorer → **Reveal in File Explorer/Finder** → double-click to open in your browser.
- Nicer for iterating: right-click the file → **Open with Live Server**. It'll auto-refresh in the browser every time you re-run step 3.

Requires an internet connection in the *browser* (not in Python) — the dashboard loads Plotly/Leaflet/vis-network from CDNs at view time.

## 6. Connecting real data later
Replace the contents of `1_generate_data.py` with a real DB pull (e.g. `pyodbc`/`sqlalchemy` against SQL Server) that produces the same four CSVs with the same column names:
- `data/CaseMaster.csv`
- `data/Victim.csv`
- `data/Accused.csv`
- `data/ArrestSurrender.csv`

`2_build_analytics.py` and `3_build_dashboard.py` don't need to change — they only care about those column names, not where the CSVs came from.

## 7. Editing the look/layout
All HTML/CSS/JS lives in `dashboard_template.html` (not the generated `output/dashboard.html` — that one gets overwritten every time you run step 3). Edit the template, re-run `3_build_dashboard.py`, refresh the browser.
