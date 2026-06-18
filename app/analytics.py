import os
import pandas as pd

# Import Day 3 Alerting modules with safety fallback paths
try:
    from app.alerts import detect_overloads, generate_alert_messages, log_alerts_to_file
except ImportError:
    from alerts import detect_overloads, generate_alert_messages, log_alerts_to_file

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
    print("          SMART GRID LOAD ANALYTICS - DAY 3 REPORT          ")
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

        # --- DAY 3: OVERLOAD DETECTION AND ALERTS INTEGRATION ---
        # Set a load threshold of 5.0 kW (this can be dynamically configured)
        threshold_value = 5.0
        
        print("\n" + "-" * 60)
        print("DAY 3: REAL-TIME OVERLOAD DETECTION")
        print("-" * 60)
        print(f"Active Threshold Monitor: {threshold_value:.2f} kW")
        
        # Step 1: Detect overloads from dataset
        overloads_df = detect_overloads(df, threshold=threshold_value)
        
        # Step 2: Generate user-friendly alerts with severity ratings
        alerts = generate_alert_messages(overloads_df, threshold=threshold_value)
        
        print(f"Total Overload Incidents Flagged: {len(alerts)}")
        
        if alerts:
            print("\n--- Triggered Overload Alerts ---")
            for alert in alerts:
                # Add status indicators depending on severity level for rich visuals
                indicator = "🚨 [CRITICAL]" if alert["severity"] == "CRITICAL" else "⚠️ [WARNING]"
                print(f"{indicator} Time: {alert['timestamp']} | Meter: {alert['meter_id']} | "
                      f"Load: {alert['consumption_kw']:.2f} kW | Exceeded By: {alert['consumption_kw'] - threshold_value:.2f} kW")
            
            # Step 3: Log all generated alerts to disk/persistence layer
            log_file_path = os.path.join("data", "alerts.log")
            log_alerts_to_file(alerts, log_path=log_file_path)
        else:
            print("\n✅ Normal Operations: No overload events detected.")

    except FileNotFoundError as fnf_error:
        print(f"IO Error: {fnf_error}")
    except Exception as general_error:
        print(f"Runtime Error occurred during analytics: {general_error}")

    print("=" * 60)

if __name__ == "__main__":
    data_file_path = os.path.join("data", "sample_meter_data.csv")
    generate_formatted_reports(data_file_path)
