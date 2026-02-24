"""Model training for V1.

V1 trains two simple baselines:
- Logistic Regression (interpretable)
- Gradient Boosting (non-linear baseline)

V2 handles model registry, drift monitoring, CI checks, and API packaging.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, Tuple

import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier


@dataclass
class ModelBundle:
    name: str
    pipeline: Pipeline


def build_preprocessor(cat_cols, num_cols) -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
            ("num", "passthrough", num_cols),
        ]
    )


def logistic_regression_model(cat_cols, num_cols) -> ModelBundle:
    prep = build_preprocessor(cat_cols, num_cols)
    pipe = Pipeline(
        steps=[
            ("prep", prep),
            ("clf", LogisticRegression(max_iter=400, solver="saga", n_jobs=-1)),
        ]
    )
    return ModelBundle(name="LogisticRegression", pipeline=pipe)


def gradient_boosting_model(cat_cols, num_cols) -> ModelBundle:
    prep = build_preprocessor(cat_cols, num_cols)
    pipe = Pipeline(
        steps=[
            ("prep", prep),
            ("clf", GradientBoostingClassifier(random_state=42)),
        ]
    )
    return ModelBundle(name="GradientBoosting", pipeline=pipe)


def predict_proba(bundle: ModelBundle, X) -> np.ndarray:
    return bundle.pipeline.predict_proba(X)[:, 1]
