import pandas as pd
from sklearn.model_selection import train_test_split
from preprocess import preprocess_data
from feature_engineering import feature_selection_drop_corr, add_interaction_features, apply_pca_on_counts
from models import get_models, train_and_evaluate
from utils import plot_feature_importance
import numpy as np

# 1. Load and preprocess data
df = preprocess_data('data.csv')

# 2. Create target label (liked or not)
print(df["vote_average"].median())
df['liked'] = (df['vote_average'] >= 0.09).astype(int)
df.drop(columns=['id'], inplace=True)

# 3. Split features and target
X = df.drop(columns=['liked'])
y = df['liked']
# print(y)
# 4. Split train/validation/test sets
X_train, X_temp, y_train, y_temp = train_test_split(X, y, stratify=y, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, stratify=y_temp, test_size=0.5, random_state=42)

# print("Unique classes in y_train:", np.unique(y_train))

# 5. Feature selection
X_train, dropped_features = feature_selection_drop_corr(X_train)
X_val = X_val.drop(columns=dropped_features)
X_test = X_test.drop(columns=dropped_features)

# 6. Feature engineering
X_train = add_interaction_features(X_train)
X_val = add_interaction_features(X_val)
X_test = add_interaction_features(X_test)

count_cols = [col for col in X_train.columns if '_count' in col]
X_train, pca = apply_pca_on_counts(X_train, count_cols)
X_val_pca = pca.transform(X_val[count_cols])
X_test_pca = pca.transform(X_test[count_cols])

X_val = X_val.drop(columns=count_cols)
X_test = X_test.drop(columns=count_cols)

X_val['pca_1'], X_val['pca_2'] = X_val_pca[:, 0], X_val_pca[:, 1]
X_test['pca_1'], X_test['pca_2'] = X_test_pca[:, 0], X_test_pca[:, 1]

# 7. Train models and evaluate
models = get_models()
# print("Unique classes in y_train:", np.unique(y_train))

for name, model in models.items():
    print(f"\nTraining {name}...")
    trained_model = train_and_evaluate(model, X_train, y_train, X_val, y_val)

# 8. Select best model manually here (e.g., XGBoost) and test
best_model = models['XGBoost']
best_model.fit(X_train, y_train)
y_test_pred = best_model.predict(X_test)
y_test_proba = best_model.predict_proba(X_test)[:, 1]

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report
print("\nTest set evaluation:")
print("Accuracy:", accuracy_score(y_test, y_test_pred))
print("Precision:", precision_score(y_test, y_test_pred))
print("Recall:", recall_score(y_test, y_test_pred))
print("F1 Score:", f1_score(y_test, y_test_pred))
print("ROC AUC:", roc_auc_score(y_test, y_test_proba))
print("Classification Report:\n", classification_report(y_test, y_test_pred))

# 9. Plot feature importance for Random Forest as example
from utils import plot_feature_importance
plot_feature_importance(models['RandomForest'], X_train.columns.values)
