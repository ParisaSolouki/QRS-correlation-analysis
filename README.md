# QRS Template Matching with Correlation Analysis (MIT-BIH)

This project builds an end-to-end workflow to transform raw ECG time-series into structured beat-level data and quantify similarity between beats using correlation-based template matching.

Although the source data is biomedical, the core skills demonstrated are transferable to general analytics:
**time-series preprocessing, feature engineering, data structuring, and relationship analysis.**

---

## Objective
Create a **normal-beat template** and measure how similar other beats are to it using **Pearson correlation**.
This helps quantify pattern similarity across categories (N, S, F, V, U).

---

## Dataset
- **MIT-BIH Arrhythmia Database**
- Sampling rate: **360 Hz**
- Beat types used: **N, S, F, V, U**

> Note: This repository does not include the dataset files. See *How to Run* to download/access the data.

---

## Workflow
1. **Load raw signals** (`.dat`) and annotations
2. **Preprocess** (bandpass filtering using Butterworth filters)
3. **Segment beats** around annotated R-peaks
4. **Structure data** into beat-level arrays / tables by class
5. **Build template** from normal beats (N) using averaging
6. **Correlation analysis**: compare each beat (or selected beats) with the template
7. **Summarize results** by beat type

---

## Methods
### Filtering
Butterworth high-pass + low-pass filters applied to reduce baseline wander and high-frequency noise.

### Template Creation
A template is created by averaging segmented beats labeled as **Normal (N)**.

### Similarity Metric
Pearson correlation coefficient is used to quantify similarity between a beat and the template.

---

## Outputs
- Segmented beats grouped by type: **N, S, F, V, U**
- Correlation scores per beat (or per selected beats)
- Summary statistics (e.g., mean/median correlation per beat type)

Suggested saved outputs:
- `results/correlation_scores.csv`
- `results/summary_by_type.csv`

---

## Example Insights (to be completed)
Replace these with your actual results:
- Beats of type **N** show the highest similarity to the template (mean r ≈ __).
- Certain non-normal types (e.g., **V**) show noticeably lower correlation (mean r ≈ __), indicating distinct morphology.
- Correlation distributions differ by type, making correlation a useful proxy feature for classification or anomaly detection.

---

## Tech Stack
- Python
- NumPy, pandas
- SciPy (signal processing / correlation)
- wfdb (MIT-BIH data reader)
- Matplotlib (optional, for plots)

---

