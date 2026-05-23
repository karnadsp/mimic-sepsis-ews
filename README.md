# MIMIC-IV Pre-Treatment Sepsis Early Warning System

## Overview
An independent Random Forest classifier for early sepsis prediction, built exclusively on pre-treatment physiological data from the MIMIC-IV database. This project directly addresses the critical flaw identified by Wiens et al. (2024, NEJM AI), which demonstrated that the Epic Sepsis Model collapses to an AUROC of 0.47 when restricted to pre-treatment data — worse than random chance.

This system predicts sepsis risk using only biological signals available before any clinician-initiated treatment markers (antibiotics, blood cultures, IV fluids), and outputs standardized FHIR R4 RiskAssessment resources for clinical deployment.

## The Problem
The Epic Sepsis Model (ESM) is deployed at hundreds of US hospitals. Research conducted at University of Michigan Health on 77,000 adult inpatients found that the ESM's AUROC drops from 0.62 to 0.47 once predictions are restricted to pre-treatment data — meaning the model performs worse than a coin toss precisely when clinicians need it most: before they have already suspected sepsis.

## What This Project Builds

### Layer 1 — Machine Learning
- Random Forest classifier trained exclusively on pre-treatment data
- Features: vital sign trends, early lab results, age, chronic conditions — all captured within the first 6 hours of admission
- Strict treatment trigger timestamp cutoff: earliest of first antibiotic order, blood culture order, or IV fluid bolus
- SHAP-based feature importance audit to mathematically demonstrate zero contamination from treatment markers
- AUROC benchmarked against the Wiens et al. 0.47 baseline and traditional scores (SIRS, qSOFA)

### Layer 2 — Interoperability
- Deterministic Python pipeline transforming model risk scores into FHIR R4 RiskAssessment JSON payloads
- Each payload includes: risk probability, top SHAP features in plain language, pre-treatment timestamp certification, and Patient resource reference

## Repository Structure
```
mimic-sepsis-ews/
├── data/
│   ├── raw/          # Raw MIMIC-IV extracts (not committed — covered by DUA)
│   └── processed/    # Cleaned cohort and feature matrices
├── notebooks/
│   ├── 01_cohort_definition.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_model_training.ipynb
│   └── 04_fhir_output.ipynb
├── src/
│   ├── cohort.py
│   ├── features.py
│   ├── model.py
│   ├── fhir_generator.py
│   └── contamination_audit.py
└── README.md
```
## Dataset
MIMIC-IV v3.1 (Medical Information Mart for Intensive Care)  
Access: PhysioNet Credentialed Health Data License  
Note: Raw data files are not included in this repository in compliance with the PhysioNet Data Use Agreement.

## Key References
- Wiens et al. (2024). Evaluation of Sepsis Prediction Models before Onset of Treatment. *NEJM AI*. DOI: 10.1056/AIoa2300032
- Wong et al. (2021). External Validation of a Widely Implemented Proprietary Sepsis Prediction Model. *JAMA Internal Medicine*.
- Johnson et al. MIMIC-IV (version 3.1). PhysioNet. DOI: 10.13026/07hj-2a80

## Author
Shreyas Karnad  
Master of Health Informatics, University of Michigan  
[LinkedIn](https://linkedin.com/in/shreyas-karnad) | [Portfolio](https://karnadsp.github.io)

## Status
🟡 In Progress — awaiting MIMIC-IV data access approval
