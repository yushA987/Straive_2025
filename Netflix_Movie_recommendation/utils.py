import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plot_feature_importance(model, feature_names):
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]

    plt.figure(figsize=(10,6))
    sns.barplot(x=importances[indices], y=feature_names[indices])
    plt.title(f"Feature Importances - {model.__class__.__name__}")
    plt.show()
