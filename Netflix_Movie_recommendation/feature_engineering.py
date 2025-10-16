import pandas as pd
from sklearn.decomposition import PCA
import numpy as np


def feature_selection_drop_corr(X, threshold=0.85):
    corr_matrix = X.corr().abs()
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    to_drop = [col for col in upper.columns if any(upper[col] > threshold)]
    X = X.drop(columns=to_drop)
    return X, to_drop


def add_interaction_features(X):
    X['budget_popularity_interaction'] = X['budget'] * X['popularity']
    return X


def apply_pca_on_counts(X, count_cols, n_components=2):
    pca = PCA(n_components=n_components, random_state=42)
    pca_components = pca.fit_transform(X[count_cols])

    # Drop original count cols
    X = X.drop(columns=count_cols)

    for i in range(n_components):
        X[f'pca_{i + 1}'] = pca_components[:, i]

    return X, pca
