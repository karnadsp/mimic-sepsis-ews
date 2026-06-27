# Feature engineering module
# Pre-Treatment Sepsis Early Warning System
# Shreyas Karnad — Master of Health Informatics, University of Michigan

"""
Feature engineering pipeline for MIMIC-IV pre-treatment sepsis prediction.

Key principle: All features must be extracted strictly before the
treatment trigger timestamp (earliest of first antibiotic order or
blood culture order) to ensure zero treatment contamination.

Features:
- Vital signs: HR, SBP, DBP, MAP, RR, Temperature, SpO2
  (avg/max/min aggregates over 6-hour pre-treatment window)
- Laboratory values: WBC, Lactate, pH, PaO2/FiO2, Creatinine,
  BUN, Sodium, Potassium, Bicarbonate, Glucose
- Missingness indicator flags for high-missing lab features
- Demographics: age, gender, insurance, race
- Comorbidity burden: Charlson Comorbidity Index
"""

VITAL_FEATURES = [
    'avg_hr', 'max_hr', 'min_hr',
    'avg_sbp', 'min_sbp',
    'avg_dbp',
    'avg_mbp', 'min_mbp',
    'avg_rr', 'max_rr',
    'avg_temp', 'max_temp', 'min_temp',
    'avg_spo2', 'min_spo2',
    'vital_measurement_count'
]

LAB_FEATURES = [
    'avg_wbc', 'max_wbc', 'min_wbc',
    'avg_lactate', 'max_lactate',
    'avg_ph', 'min_ph',
    'avg_pao2fio2',
    'avg_creatinine', 'max_creatinine',
    'avg_bun',
    'avg_sodium',
    'avg_potassium',
    'avg_bicarbonate', 'min_bicarbonate',
    'avg_glucose'
]

HIGH_MISSING_FEATURES = [
    'avg_pao2fio2',
    'avg_lactate',
    'max_lactate',
    'avg_ph',
    'min_ph'
]

DEMOGRAPHIC_FEATURES = [
    'admission_age',
    'charlson_comorbidity_index'
]

CATEGORICAL_FEATURES = [
    'gender',
    'insurance',
    'race'
]

ID_COLS = ['stay_id', 'hadm_id', 'subject_id']
LABEL_COL = 'sepsis_label'

ALL_FEATURES = VITAL_FEATURES + LAB_FEATURES + DEMOGRAPHIC_FEATURES
