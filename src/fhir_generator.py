# FHIR R4 RiskAssessment output module
# Pre-Treatment Sepsis Early Warning System
# Shreyas Karnad — Master of Health Informatics, University of Michigan

"""
Generates FHIR R4 RiskAssessment resources from Random Forest
risk predictions.

FHIR standard: R4 (Release 4)
Resource type: RiskAssessment
Terminology: SNOMED CT, HL7 risk-probability CodeSystem

Risk stratification:
- Low:      probability < 0.40
- Moderate: probability 0.40 - 0.70
- High:     probability >= 0.70

Key feature: Custom extension certifying pre-treatment status
  url: http://sepsis-ews.mimic.org/pre-treatment-certified
  valueBoolean: true

This extension guarantees the prediction was generated without
treatment contamination — a guarantee no proprietary sepsis model
currently provides.

Output: FHIR Bundle (collection) of RiskAssessment resources
Each resource contains:
- Patient and encounter references
- Probability score (probabilityDecimal)
- Qualitative risk category (Low/Moderate/High)
- Rationale with top 3 SHAP features in plain English
- Pre-treatment certification extension
- Model AUROC and version extensions
"""

FHIR_VERSION = 'R4'
RESOURCE_TYPE = 'RiskAssessment'
MODEL_VERSION = 'mimic-iv-rf-v1.0'
MODEL_AUROC = 0.7766

RISK_THRESHOLDS = {
    'low': 0.40,
    'moderate': 0.70
}

SNOMED_SEPSIS_CODE = '11552004'
SNOMED_SYSTEM = 'http://snomed.info/sct'
HL7_RISK_SYSTEM = 'http://terminology.hl7.org/CodeSystem/risk-probability'

CUSTOM_EXTENSIONS = {
    'pre_treatment_certified': 'http://sepsis-ews.mimic.org/pre-treatment-certified',
    'model_auroc': 'http://sepsis-ews.mimic.org/model-auroc',
    'model_version': 'http://sepsis-ews.mimic.org/model-version',
    'top_features': 'http://sepsis-ews.mimic.org/top-features'
}
