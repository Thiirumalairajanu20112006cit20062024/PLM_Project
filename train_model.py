"""
========================================================================================
PROJECT TITLE:
Digital Twin-Enabled AI Framework for Predictive Maintenance and Product Lifecycle 
Optimization of Heavy Equipment Engine Components

COURSE: ME4506 – Product Lifecycle Management
MENTOR: Dhanesh Babu
TEAM: Thirumalairajan U, Tharunkumar RP
========================================================================================
Description:
This script performs complete end-to-end data preprocessing, model training, 
evaluation, visualization, and persistence for both Classification (Engine Health Status) 
and Regression (Remaining Useful Life - RUL).
========================================================================================
"""

import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix,
    mean_absolute_error, mean_squared_error, r2_score
)

def train_and_evaluate_models():
    """
    Main function to execute preprocessing, model training, evaluation, 
    plot generation, and saving serialized model artifacts.
    """
    print("=" * 80)
    print("   ME4V33 PLM PROJECT: HEAVY EQUIPMENT ENGINE PREDICTIVE MAINTENANCE ML PIPELINE")
    print("=" * 80)

    # ----------------------------------------------------------------------------------
    # PART 1: DATA PREPROCESSING
    # ----------------------------------------------------------------------------------
    print("\n[PART 1] Loading and Preprocessing Sensor Dataset...")
    
    csv_file = "sensor_data.csv"
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"Error: '{csv_file}' not found. Please run dataset generator first.")

    # 1. Load Dataset
    df = pd.read_csv(csv_file)
    print(f"-> Dataset successfully loaded with shape: {df.shape}")
    print(f"-> Feature Columns: {list(df.columns)}")

    # 2. Handle Missing Values (Imputation if any missing)
    missing_counts = df.isnull().sum().sum()
    if missing_counts > 0:
        print(f"-> Found {missing_counts} missing values. Performing forward/median imputation...")
        df.fillna(df.median(numeric_only=True), inplace=True)
    else:
        print("-> Data Quality Check Passed: 0 missing values detected.")

    # Define Feature Sets
    feature_cols = ['hours_operated', 'temperature', 'vibration', 'oil_pressure', 'rpm', 'load']
    X = df[feature_cols].copy()
    y_class_raw = df['health_label'].copy()
    y_reg = df['RUL'].copy()

    # 3. Label Encoding for Categorical Target (health_label)
    encoder = LabelEncoder()
    y_class = encoder.fit_transform(y_class_raw)
    print(f"-> Label Encoding mapped classes: {dict(zip(encoder.classes_, encoder.transform(encoder.classes_)))}")

    # 4. Standard Scaling for Numerical Features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled_df = pd.DataFrame(X_scaled, columns=feature_cols)

    # 5. Train-Test Split (80% Train, 20% Test)
    # Stratified split to ensure balanced target class distributions in both sets
    X_train, X_test, y_class_train, y_class_test, y_reg_train, y_reg_test = train_test_split(
        X_scaled_df, y_class, y_reg, test_size=0.20, random_state=42, stratify=y_class
    )

    print(f"-> Train Set Size: {len(X_train)} samples (80%)")
    print(f"-> Test Set Size:  {len(X_test)} samples (20%)")

    # ----------------------------------------------------------------------------------
    # PART 2: CLASSIFICATION MODEL (Health Status Prediction: Healthy, Warning, Failure)
    # ----------------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("[PART 2] Training & Evaluating Classification Model (Random Forest Classifier)")
    print("=" * 80)

    clf = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=None
    )
    clf.fit(X_train, y_class_train)
    y_class_pred = clf.predict(X_test)

    # Evaluation Metrics
    acc = accuracy_score(y_class_test, y_class_pred)
    prec = precision_score(y_class_test, y_class_pred, average='weighted')
    rec = recall_score(y_class_test, y_class_pred, average='weighted')
    f1 = f1_score(y_class_test, y_class_pred, average='weighted')

    print(f"\nClassification Metrics Summary:")
    print(f"   - Accuracy:  {acc * 100:.2f}%")
    print(f"   - Precision: {prec * 100:.2f}%")
    print(f"   - Recall:    {rec * 100:.2f}%")
    print(f"   - F1 Score:  {f1 * 100:.2f}%")

    print("\nDetailed Classification Report:")
    target_names = [str(c) for c in encoder.classes_]
    print(classification_report(y_class_test, y_class_pred, target_names=target_names))

    print("Confusion Matrix:")
    cm = confusion_matrix(y_class_test, y_class_pred)
    cm_df = pd.DataFrame(cm, index=target_names, columns=target_names)
    print(cm_df)

    # ----------------------------------------------------------------------------------
    # PART 3: REGRESSION MODEL (Remaining Useful Life - RUL Prediction)
    # ----------------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("[PART 3] Training & Evaluating Regression Model (Random Forest Regressor)")
    print("=" * 80)

    reg = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=None
    )
    reg.fit(X_train, y_reg_train)
    y_reg_pred = reg.predict(X_test)

    # Evaluation Metrics
    mae = mean_absolute_error(y_reg_test, y_reg_pred)
    mse = mean_squared_error(y_reg_test, y_reg_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_reg_test, y_reg_pred)

    print(f"\nRegression Metrics Summary:")
    print(f"   - Mean Absolute Error (MAE):  {mae:.2f} hours")
    print(f"   - Mean Squared Error (MSE):   {mse:.2f}")
    print(f"   - Root Mean Sq. Error (RMSE): {rmse:.2f} hours")
    print(f"   - R² Score:                   {r2:.4f} ({r2*100:.2f}% variance explained)")

    # Plot Actual vs Predicted RUL
    plt.figure(figsize=(9, 6))
    plt.scatter(y_reg_test, y_reg_pred, alpha=0.7, color='#00a8ff', edgecolors='k', s=50, label='Test Samples')
    ideal_min = min(y_reg_test.min(), y_reg_pred.min())
    ideal_max = max(y_reg_test.max(), y_reg_pred.max())
    plt.plot([ideal_min, ideal_max], [ideal_min, ideal_max], 'r--', linewidth=2, label='Ideal 1:1 Line')
    plt.title("Random Forest Regressor: Actual vs Predicted Remaining Useful Life (RUL)", fontsize=13, fontweight='bold')
    plt.xlabel("Actual RUL (Hours)", fontsize=11)
    plt.ylabel("Predicted RUL (Hours)", fontsize=11)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='upper left')
    plt.tight_layout()
    plot_path = "actual_vs_predicted_rul.png"
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"-> Actual vs Predicted RUL plot saved to: {plot_path}")

    # ----------------------------------------------------------------------------------
    # PART 4: SAVE MODELS
    # ----------------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("[PART 4] Saving Trained Models & Transformers using Joblib")
    print("=" * 80)

    models_dir = "saved_models"
    os.makedirs(models_dir, exist_ok=True)

    classifier_path = os.path.join(models_dir, "classifier.pkl")
    regressor_path  = os.path.join(models_dir, "regressor.pkl")
    scaler_path     = os.path.join(models_dir, "scaler.pkl")
    encoder_path    = os.path.join(models_dir, "encoder.pkl")

    joblib.dump(clf, classifier_path)
    joblib.dump(reg, regressor_path)
    joblib.dump(scaler, scaler_path)
    joblib.dump(encoder, encoder_path)

    print(f" Successfully saved Classification Model -> {classifier_path}")
    print(f" Successfully saved Regression Model     -> {regressor_path}")
    print(f" Successfully saved StandardScaler       -> {scaler_path}")
    print(f" Successfully saved LabelEncoder          -> {encoder_path}")

    print("\n" + "=" * 80)
    print(" PIPELINE EXECUTION COMPLETE: ALL MODELS READY FOR STREAMLIT DASHBOARD")
    print("=" * 80)

if __name__ == "__main__":
    train_and_evaluate_models()
