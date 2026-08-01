"""
Dataset Generator for Heavy Equipment Engine Predictive Maintenance
Course: ME4V33 – Product Lifecycle Management
Mentor: Dhanesh Babu
Team: Thirumalairajan U & Tharunkumar RP
"""

import numpy as np
import pandas as pd

def generate_engine_sensor_data(n_samples=1200, random_state=42):
    np.random.seed(random_state)
    
    # 1. Primary operational parameters
    hours_operated = np.random.uniform(50, 10000, n_samples)
    rpm = np.random.uniform(900, 2400, n_samples)
    load = np.random.uniform(25, 95, n_samples)
    
    # 2. Physics-based sensor responses with operational degradation
    # Higher hours, load, and RPM lead to higher temperatures and vibration, lower oil pressure
    temperature = (
        70.0 
        + (hours_operated / 1000.0) * 2.8 
        + (load / 100.0) * 22.0 
        + (rpm / 2400.0) * 10.0 
        + np.random.normal(0, 3.5, n_samples)
    )
    
    vibration = (
        0.8 
        + (hours_operated / 1000.0) * 1.1 
        + (load / 100.0) * 2.5 
        + (rpm / 2400.0) * 1.5 
        + np.random.normal(0, 0.4, n_samples)
    )
    # Clip vibration to realistic positive values
    vibration = np.clip(vibration, 0.5, 18.0)
    
    oil_pressure = (
        62.0 
        - (hours_operated / 1000.0) * 3.2 
        - (temperature - 70.0) * 0.18 
        - (load / 100.0) * 5.0 
        + np.random.normal(0, 2.5, n_samples)
    )
    # Clip oil pressure to physical limits
    oil_pressure = np.clip(oil_pressure, 10.0, 75.0)
    
    # 3. Formulate Degradation Index to derive Health Label and RUL
    # Normalized stress indicators
    temp_stress = np.clip((temperature - 65) / 55.0, 0, 1.5)
    vib_stress = np.clip((vibration - 1.0) / 12.0, 0, 1.5)
    press_stress = np.clip((55.0 - oil_pressure) / 45.0, 0, 1.5)
    hours_stress = hours_operated / 10000.0
    
    degradation_score = (
        0.30 * temp_stress + 
        0.35 * vib_stress + 
        0.25 * press_stress + 
        0.10 * hours_stress
    )
    
    # 4. Classify into Healthy, Warning, Failure based on degradation score thresholds
    health_labels = []
    rul_values = []
    
    for idx, d_score in enumerate(degradation_score):
        if d_score < 0.42:
            label = "Healthy"
            base_rul = 1500 - (d_score / 0.42) * 700 + np.random.normal(0, 60)
        elif d_score < 0.75:
            label = "Warning"
            base_rul = 800 - ((d_score - 0.42) / 0.33) * 550 + np.random.normal(0, 45)
        else:
            label = "Failure"
            base_rul = 250 - ((d_score - 0.75) / 0.75) * 230 + np.random.normal(0, 25)
            
        health_labels.append(label)
        rul_values.append(max(0.0, round(float(base_rul), 1)))
        
    df = pd.DataFrame({
        'hours_operated': np.round(hours_operated, 1),
        'temperature': np.round(temperature, 1),
        'vibration': np.round(vibration, 2),
        'oil_pressure': np.round(oil_pressure, 1),
        'rpm': np.round(rpm, 0),
        'load': np.round(load, 1),
        'health_label': health_labels,
        'RUL': rul_values
    })
    
    return df

if __name__ == "__main__":
    df = generate_engine_sensor_data()
    df.to_csv("sensor_data.csv", index=False)
    print(f"Generated sensor_data.csv successfully with {len(df)} records.")
    print("Class distribution:")
    print(df['health_label'].value_counts())
    print("\nDataset summary:")
    print(df.describe())
