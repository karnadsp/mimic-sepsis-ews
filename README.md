# MIMIC-IV Pre-Treatment Sepsis Early Warning System

## Overview
An independent Random Forest classifier for early sepsis prediction, built exclusively on pre-treatment physiological data from the MIMIC-IV clinical database. This project directly addresses the critical flaw identified by Wiens et al. (2024, NEJM AI), which demonstrated that the Epic Sepsis Model collapses to an AUROC of 0.47 when restricted to pre-treatment data, which is worse than random chance.

This system predicts sepsis risk using only biological signals available before any clinician-initiated treatment markers (antibiotics, blood cultures, IV fluids), and outputs standardized FHIR R4 RiskAssessment resources for clinical deployment.

---

## The Problem

The Epic Sepsis Model (ESM) is deployed at hundreds of US hospitals including Michigan Medicine. Research conducted at the University of Michigan on 77,000+ adult inpatients found that the ESM's AUROC drops from 0.62 to **0.47**, worse than a coin toss, once predictions are restricted to pre-treatment data. This means the model performs worst precisely when clinicians need it most: before they have already suspected sepsis.

---

## Results

| Model | AUROC | Notes |
|---|---|---|
| Random classifier | 0.50 | Theoretical baseline |
| Epic ESM: pre-treatment (Wiens et al. 2024) | 0.47 | Worse than random |
| Epic ESM: with treatment contamination | 0.62 | Standard ESM deployment |
| **This model: pre-treatment RF (Google Colab)** | **0.7766** | ✅ Primary result |
| **This model: pre-treatment RF (Local VSCode)** | **0.8160** | ✅ Reproduced locally |

**Key finding:** A pre-treatment Random Forest trained on biological signals alone outperforms the Epic ESM even when the ESM is permitted to use post-treatment contaminated data. The model was independently validated on two separate compute environments.

---

## What This Project Builds

### Layer 1: Machine Learning
- Random Forest classifier (scikit-learn) trained exclusively on pre-treatment data
- **Cohort:** 67,286 adult ICU stays from MIMIC-IV v3.1 (Beth Israel Deaconess Medical Center, 2008-2022)
- **Features:** vital sign trends, early lab results, age, chronic conditions. These are all captured within the first 6 hours of ICU admission and strictly before treatment initiation
- **Treatment trigger:** earliest of first antibiotic order or blood culture which defines the contamination cutoff
- **Outcome label:** Sepsis-3 validated labels from MIMIC-IV derived dataset
- **SHAP contamination audit:** mathematically confirms zero treatment markers in top 20 predictive features

### Layer 2: Interoperability
- Deterministic Python pipeline transforming model risk scores into FHIR R4 RiskAssessment JSON payloads
- SNOMED CT terminology bindings for sepsis outcome coding
- Custom extension certifying pre-treatment status. This is a guarantee which no proprietary sepsis model currently provides
- SHAP-derived rationale text embedded in each resource for clinical transparency

---

## SHAP Contamination Audit: PASSED

Top 20 features by mean absolute SHAP value: **zero treatment markers**:

| Rank | Feature | Clinical Meaning |
|---|---|---|
| 1 | vital_measurement_count | Monitoring intensity proxy |
| 2 | min_hr | Minimum heart rate in 6hr window |
| 3 | min_spo2 | Minimum oxygen saturation |
| 4 | avg_rr | Average respiratory rate |
| 5 | avg_bun | Blood urea nitrogen (kidney function) |
| 6 | avg_spo2 | Average oxygen saturation |
| 7 | charlson_comorbidity_index | Chronic disease burden |
| 8 | max_temp | Maximum temperature |
| 9 | avg_hr | Average heart rate |
| 10 | avg_pao2fio2_missing | Blood gas not ordered (lower acuity signal) |

No antibiotics, no blood culture timestamps, no IV fluid markers anywhere in the top 20 features.

---

## Repository Structure

```
mimic-sepsis-ews/
├── data/
│   ├── raw/          # Raw MIMIC-IV extracts (not committed: covered by DUA)
│   └── processed/    # Cleaned cohort, feature matrices, model, FHIR bundle
├── notebooks/
│   ├── 01_cohort_definition.ipynb       # Data loading, imputation, train/test split
│   ├── 02_feature_engineering.ipynb     # Exploratory data analysis
│   ├── 03_model_training.ipynb          # Random Forest, AUROC, SHAP audit
│   └── 04_fhir_output.ipynb             # FHIR R4 RiskAssessment generation
├── src/
│   ├── cohort.py                        # Cohort definition module
│   ├── features.py                      # Feature engineering module
│   ├── model.py                         # Model training and evaluation
│   ├── fhir_generator.py                # FHIR R4 RiskAssessment output
│   └── contamination_audit.py           # Pre-treatment contamination audit
└── README.md
```

---

## Reproducibility

Notebooks are environment-agnostic. They are designed to auto-detect Google Colab vs local VSCode:

```python
if os.path.exists('/content/drive'):
    # Google Colab
    from google.colab import drive
    drive.mount('/content/drive')
    project_path = '/content/drive/MyDrive/mimic-sepsis-ews'
else:
    # Local VSCode
    project_path = os.path.abspath(os.path.join(os.getcwd(), '..'))
```

**Tested environments:**
- Google Colab (Python 3, scikit-learn 1.9.0) gives AUROC 0.7766
- Local VSCode, Windows 11, Intel Core i9-11800H, 32GB RAM (Python 3, scikit-learn) gives AUROC 0.8160

---

## Dataset

MIMIC-IV v3.1 (Medical Information Mart for Intensive Care)
- **Source:** Beth Israel Deaconess Medical Center, Boston MA (2008-2022)
- **Access:** PhysioNet Credentialed Health Data License
- **Size:** 67,286 adult ICU stays used in this project
- **Access via:** Google BigQuery (`physionet-data.mimiciv_3_1_hosp`, `mimiciv_3_1_icu`, `mimiciv_3_1_derived`)

Raw data files are not included in this repository in compliance with the PhysioNet Data Use Agreement.

---

## Requirements

```bash
pip install pandas numpy scikit-learn shap matplotlib seaborn jupyter
```

---

## Key References

- Wiens et al. (2024). Evaluation of Sepsis Prediction Models before Onset of Treatment. *NEJM AI*. DOI: 10.1056/AIoa2300032
- Singer M, et al. The Third International Consensus Definitions for Sepsis and Septic Shock (Sepsis-3). *JAMA*. 2016;315(8):801-810.
- Johnson et al. MIMIC-IV (version 3.1). PhysioNet. DOI: 10.13026/kpb9-mt58
- Johnson AEW, et al. MIMIC-IV, a freely accessible electronic health record dataset. *Sci Data*. 2023. DOI: 10.1038/s41597-022-01899-x
- HL7 International. FHIR R4 RiskAssessment Resource. https://hl7.org/fhir/R4/riskassessment.html

---

## Author

Shreyas Karnad
Master of Health Informatics, University of Michigan (May 2026)
[LinkedIn](https://linkedin.com/in/shreyas-karnad) | [Portfolio](https://karnadsp.github.io) | [GitHub](https://github.com/karnadsp)

## Status
🟢 Complete.  AUROC 0.7766 (Colab) | 0.8160 (Local) | FHIR R4 output | SHAP audit passed
