# Model training and evaluation module
# Pre-Treatment Sepsis Early Warning System
# Shreyas Karnad — Master of Health Informatics, University of Michigan

"""
Random Forest classifier for pre-treatment sepsis prediction.

Model configuration:
- Algorithm: Random Forest (scikit-learn RandomForestClassifier)
- n_estimators: 200
- max_depth: 20
- min_samples_leaf: 10
- class_weight: balanced (handles 11.3% sepsis prevalence)
- random_state: 42

Performance (MIMIC-IV v3.1 test set, n=13,458):
- AUROC: 0.7766 (Google Colab, scikit-learn 1.9.0)
- AUROC: 0.8160 (Local VSCode, Windows 11)
- Baseline (Wiens et al. 2024 ESM pre-treatment): 0.47
- Improvement over baseline: +0.31 (Colab) / +0.35 (Local)

SHAP contamination audit: PASSED
- Zero treatment markers in top 20 predictive features
- All features are pure biological/physiological signals
"""

MODEL_PARAMS = {
    'n_estimators': 200,
    'max_depth': 20,
    'min_samples_leaf': 10,
    'class_weight': 'balanced',
    'random_state': 42,
    'n_jobs': -1
}

AUROC_BENCHMARKS = {
    'random_classifier': 0.50,
    'esm_pre_treatment': 0.47,
    'esm_contaminated': 0.62,
    'this_model_colab': 0.7766,
    'this_model_local': 0.8160
}
