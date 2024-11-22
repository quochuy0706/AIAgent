import pandas as pd
import numpy as np
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os 
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split, cross_validate, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import warnings

# Suppress all warnings
warnings.filterwarnings('ignore')
# Set display all columns
pd.set_option('display.max_columns', None)


def load_hydraulic_data(file_path, agg='mean'):
    try:
        # Load data from the file
        arr_data = np.genfromtxt(file_path)
        
        # Check if data was loaded successfully
        if arr_data.size == 0:
            raise ValueError("File is empty or not properly formatted.")

        # Aggregate data based on the specified aggregation function
        if agg == 'mean':
            agg_data = np.mean(arr_data, axis=1)
        elif agg == 'median':
            agg_data = np.median(arr_data, axis=1)
        else:
            raise ValueError("Invalid aggregation function. Choose 'mean' or 'median'.")

        return agg_data

    except IOError:
        print(f"Error: Could not read file {file_path}. Please check if the file exists and is accessible.")
        return None
    except ValueError as e:
        print(f"Error: {e}")
        return None

def export_parquet(target_path, file_name,df):
    df.to_parquet(f"{target_path}/{file_name}.parquet", engine='pyarrow')


def cross_validate_for_each_model(models, X_train, y_train):
    cv_results = {}
    for model_name, model in models.items():
        print(f"Performing cross-validation for {model_name}...")
        results = cross_validate(model, X_train, y_train, cv=10, scoring='accuracy', return_train_score=True)
        cv_results[model_name] = {
            'mean_train_score': np.mean(results['train_score']),
            'mean_test_score': np.mean(results['test_score']),
            'std_test_score': np.std(results['test_score']),
            'fit_time': np.mean(results['fit_time']),
            'score_time': np.mean(results['score_time'])
        }

    # Print the cross-validation results
    for model_name, scores in cv_results.items():
        print(f"{model_name}:")
        print(f"  Mean train score: {scores['mean_train_score']:.4f}")
        print(f"  Mean test score: {scores['mean_test_score']:.4f}")
        print(f"  Standard deviation of test score: {scores['std_test_score']:.4f}")
        print(f"  Mean fit time: {scores['fit_time']:.4f} seconds")
        print(f"  Mean score time: {scores['score_time']:.4f} seconds")
    return cv_results

def plot_confusion_matrix(models, X_train, y_train, X_test, y_test):
    fig, axes = plt.subplots(3, 2, figsize=(15, 15))
    fig.delaxes(axes[2, 1])  # Remove the last empty subplot if we have an odd number of models

    for ax, (model_name, model) in zip(axes.flatten(), models.items()):
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)
        ax.set_title(f'{model_name} Confusion Matrix')
        ax.set_xlabel('Predicted')
        ax.set_ylabel('Actual')

    plt.tight_layout()
    plt.show()

def best_model_selection(cv_results, mean_test_score_weight, fit_time_weight, std_test_score_weight):
    best_model_name = max(
        cv_results, 
        key=lambda k: cv_results[k]['mean_test_score']* mean_test_score_weight + (1/cv_results[k]['fit_time'])* fit_time_weight + cv_results[k]['std_test_score'] * std_test_score_weight)
    return best_model_name


def best_estimator_selection(models, best_model_name, param_grids, X_train, y_train, n_iter=50, cv=5, scoring='accuracy', random_state=42, n_jobs=-1):
    param_grid_best_model = param_grids.get(best_model_name, {})

    # Perform Randomized Search CV for the best model
    random_search = RandomizedSearchCV(models[best_model_name], param_grid_best_model, n_iter=n_iter, cv=cv, scoring=scoring, random_state=random_state, n_jobs=n_jobs)
    random_search.fit(X_train, y_train)
    best_estimator = random_search.best_estimator_
    
    print(f"Best parameters for {best_model_name}: {random_search.best_estimator_}")
    print(f"Best cross-validation score for {best_model_name}: {random_search.best_score_}")

    return best_estimator

def save_ML_model(model, model_name):
    joblib.dump(model, model_name)

def load_ML_model(model_name):
    model = joblib.load(model_name)
    return model