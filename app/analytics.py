import os
import pandas as pd

def load_smart_meter_data(csv_path: str) -> pd.DataFrame:
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Database error: File '{csv_path}' not found.")
        
    df = pd.read_csv(csv_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

def calculate_periodic_consumption(df: pd.DataFrame) -> tuple:
    daily_totals = df.groupby(df["timestamp"].dt.to_period("D"))["consumption_kw"].sum()
    weekly_totals = df.groupby(df["timestamp"].dt.to_period("W"))["consumption_kw"].sum()
    monthly_totals = df.groupby(df["timestamp"].dt.to_period("M"))["consumption_kw"].sum()
    return daily_totals, weekly_totals, monthly_totals

def detect_meter_peak_loads(df: pd.DataFrame) -> pd.DataFrame:
    peak_indices = df.groupby("meter_id")["consumption_kw"].idxmax()
    peak_loads_df = df.loc[peak_indices]
    return peak_loads_df

def generate_formatted_reports(csv_path: str) -> None:
    print("=" * 60)
    print("          SMART GRID LOAD ANALYTICS - DAY 2 REPORT          ")
    print("=" * 60)

    try:
        df = load_smart_meter_data(csv_path)
        print(f"Dataset successfully loaded from: {csv_path}\n")
        
        daily_totals, weekly_totals, monthly_totals = calculate_periodic_consumption(df)
        
        print("-" * 60)
        print("PERIODIC CONSUMPTION REPORTS")
        print("-" * 60)
        
        print("\n--- Daily Consumption Report ---")
        for period, total in daily_totals.items():
            print(f"Date: {period} | Total Consumption: {total:.2f} kWh")

        print("\n--- Weekly Consumption Report ---")
        for period, total in weekly_totals.items():
            print(f"Week Range: {period} | Total Consumption: {total:.2f} kWh")

        print("\n--- Monthly Consumption Report ---")
        for period, total in monthly_totals.items():
            print(f"Month: {period} | Total Consumption: {total:.2f} kWh")

        peak_loads = detect_meter_peak_loads(df)
        
        print("\n" + "-" * 60)
        print("PEAK LOAD DETECTION PER METER")
        print("-" * 60)
        for index, row in peak_loads.iterrows():
            print(f"Meter ID: {row['meter_id']} | Peak Load: {row['consumption_kw']:.2f} kW | Recorded At: {row['timestamp']}")

    except FileNotFoundError as fnf_error:
        print(f"IO Error: {fnf_error}")
    except Exception as general_error:
        print(f"Runtime Error occurred during analytics: {general_error}")

    print("=" * 60)

if __name__ == "__main__":
    data_file_path = os.path.join("data", "sample_meter_data.csv")
    generate_formatted_reports(data_file_path)
