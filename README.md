# Applied Data Science Capstone — SpaceX Falcon 9 Landing Prediction

Capstone project for the IBM **Applied Data Science** Professional Certificate (Coursera).
**Author:** Igor Grybek

## Business problem
SpaceX advertises a Falcon 9 launch at ~USD 62M versus ~USD 165M+ for competitors,
largely because SpaceX reuses the first stage. This project predicts whether the
Falcon 9 **first stage will land successfully**, so launch cost can be estimated.

## Data
- **90 Falcon 9 launches** (Falcon 1 excluded), collected via the SpaceX REST API v4
  and the Wikipedia *List of Falcon 9 and Falcon Heavy launches* table.
- Launch sites: CCAFS LC-40 (23), CCAFS SLC-40 (30), KSC LC-39A (22), VAFB SLC-4E (15).
- First-stage landing success rate: **67%**.
- Feature engineering: one-hot encoding of categorical attributes →
  **90 × 83** feature matrix (80 one-hot + 3 numeric columns).

## Repository structure
```
notebooks/
  1-data-collection-api.ipynb   SpaceX API v4 + Wikipedia scraping pipeline
  2-data-wrangling.ipynb        EDA, launch counts, landing outcomes, target Class
  3-eda-sql.ipynb               SQL analysis on SPACEXTBL (SQLite)
  4-eda-visualization.ipynb     matplotlib/seaborn charts
  5-folium-maps.ipynb           interactive Folium launch-site maps
  6-dash-dashboard.ipynb        Plotly Dash dashboard (+ runnable spacex_dash_app.py)
  7-ml-prediction.ipynb         classification with GridSearchCV
data/
  dataset_spacex.csv            90 curated Falcon 9 launch records
  dataset_features.csv          90 × 84 one-hot encoded features + Class
assets/                         charts and the Folium map HTML
Data Science Capstone Project Report.pdf
```

## Methodology
1. **Data collection** — SpaceX API v4 (`/launches/query`) joined with Wikipedia
   landing-outcome data.
2. **Data wrangling** — cleaning, `Class` target engineering, EDA.
3. **EDA** — SQL queries, visual analytics (payload/orbit/site vs. success),
   Folium geospatial analysis, Plotly Dash dashboard.
4. **Predictive analysis** — `train_test_split(test_size=0.2, random_state=2)`
   → 72 train / 18 test records; GridSearchCV (10-fold) over Logistic Regression,
   SVM, Decision Tree and KNN.

## Results
| Model | Test accuracy |
|---|---|
| **Decision Tree** | **83.33%** |
| SVM (best kernel: **sigmoid**) | 77.78% |
| Logistic Regression | 66.67% |
| KNN | 72.22% |

The Decision Tree generalises best (15 of 18 test launches correct): landing
success is driven by nonlinear interactions between payload mass, orbit energy
requirement and booster block — a linear boundary is insufficient.

## Reproducing
```bash
pip install pandas numpy matplotlib seaborn scikit-learn plotly dash folium jupyter
jupyter nbconvert --to notebook --execute notebooks/7-ml-prediction.ipynb --output /tmp/ml.ipynb
```
