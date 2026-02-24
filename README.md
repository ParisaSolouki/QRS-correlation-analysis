# QRS Correlation Analysis – Template-Based Similarity in Time-Series Data

## Overview

This project analyzes ECG time-series data by segmenting QRS complexes and measuring their similarity to a reference template using Pearson correlation.

Although the dataset is biomedical (MIT-BIH Arrhythmia Database), the main focus of this project is **time-series preprocessing, feature extraction, and similarity analysis**, which are transferable skills in data analytics.

---

## Objectives

- Segment time-series signals around annotated events
- Apply signal filtering (Butterworth high-pass & low-pass)
- Construct a representative template from normal patterns
- Measure similarity using correlation coefficients
- Compare behavior across different event classes

---

## Workflow

1. Load ECG records and annotations  
2. Apply filtering to remove noise  
3. Segment QRS windows around R-peaks  
4. Categorize beats into N, S, F, V, U classes  
5. Build a template from normal beats (mean signal)  
6. Compute correlation between individual beats and template  
7. Visualize similarity differences  

---

## Key Techniques Used

- Time-series segmentation
- Signal preprocessing
- Feature construction (mean template)
- Correlation analysis
- Data visualization (matplotlib)

---

## Project Structure
QRS-correlation-analysis/
│
├── notebooks/
│ └── qrs_correlation.ipynb
│
├── src/
│ └── qrs_correlation.py
│
├── .gitignore
└── README.md


---

## How to Run

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Open the notebook:
notebooks/qrs_correlation.ipynb


3.run
%run ../src/qrs_correlation.py

