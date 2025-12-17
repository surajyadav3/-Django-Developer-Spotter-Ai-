import os
import pandas as pd

# ✅ define path FIRST (global scope)
csv_path = r"C:\Users\SURAJ YADAV\OneDrive\Desktop\spotter\fuel_route\fuel-prices-for-be-assessment.csv"

print("CSV exists:", os.path.exists(csv_path))

def get_fuel_data():
    if not os.path.exists(csv_path):
        return None

    df = pd.read_csv(csv_path)

    if df.empty:
        return None

    return df
