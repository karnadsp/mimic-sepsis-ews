# Cohort definition module
# Pre-Treatment Sepsis Early Warning System
# Shreyas Karnad — Master of Health Informatics, University of Michigan

"""
Cohort definition for MIMIC-IV pre-treatment sepsis prediction.

Cohort criteria:
- Adult patients (age >= 18) admitted to the ICU
- At least 3 vital sign measurements in the first 6 hours of ICU admission
- Sepsis-3 labels from MIMIC-IV derived dataset (mimiciv_3_1_derived.sepsis3)

Treatment trigger definition:
- Earliest of: first antibiotic order OR first blood culture order
- All features must be extracted BEFORE this timestamp
- This ensures zero treatment contamination per Wiens et al. 2024

BigQuery datasets used:
- physionet-data.mimiciv_3_1_hosp (admissions, prescriptions, microbiology)
- physionet-data.mimiciv_3_1_icu (ICU stays)
- physionet-data.mimiciv_3_1_derived (sepsis3, icustay_detail, vitalsign)

Final cohort: 67,286 adult ICU stays
- Sepsis positive: 7,594 (11.3%)
- Sepsis negative: 59,692 (88.7%)
"""

INCLUSION_CRITERIA = {
    'min_age': 18,
    'min_vital_measurements': 3,
    'pre_treatment_window_hours': 6
}

ANTIBIOTIC_DRUGS = [
    'vancomycin',
    'piperacillin',
    'cefepime',
    'meropenem',
    'ciprofloxacin',
    'levofloxacin',
    'metronidazole',
    'ampicillin',
    'ceftriaxone'
]
