import os
import pandas as pd

try:
    from app.alerts import detect_overloads, generate_alert_messages, log_alerts_to_file
except ImportError:
    from alerts import detect_overloads, generate_alert_messages, log_alerts_to_file

try:
    from app.redis_client import (
        cache_analytics_results,
        get_cached_analytics,
        store_latest_meter_reading,
        get_latest_meter_reading
    )
except ImportError:
    from redis_client import (
        cache_analytics_results,
        get_cached_analytics,
        store_latest_meter_reading,
        get_latest_meter_reading
    )

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
    print("          SMART GRID LOAD ANALYTICS - DAY 4 REPORT          ")
    print("=" * 60)

    try:
        cache_key = f"analytics:report:{os.path.basename(csv_path)}"
        cached_report = get_cached_analytics(cache_key)
        
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Database error: File '{csv_path}' not found.")
            
        if cached_report:
            print("💾 [CACHE HIT] Loaded analytics results from Redis Cache!")
            daily_totals = pd.Series(cached_report["daily_totals"])
            daily_totals.index = pd.PeriodIndex(daily_totals.index, freq="D")
            
            weekly_totals = pd.Series(cached_report["weekly_totals"])
            weekly_totals.index = pd.PeriodIndex(weekly_totals.index, freq="W-SUN")
            
            monthly_totals = pd.Series(cached_report["monthly_totals"])
            monthly_totals.index = pd.PeriodIndex(monthly_totals.index, freq="M")
            
            peak_loads = pd.DataFrame(cached_report["peak_loads"])
            peak_loads["timestamp"] = pd.to_datetime(peak_loads["timestamp"])
            df = load_smart_meter_data(csv_path)
        else:
            print("❌ [CACHE MISS] Cache empty or unavailable. Computing analytics...")
            df = load_smart_meter_data(csv_path)
            print(f"Dataset successfully loaded from: {csv_path}\n")
            
            daily_totals, weekly_totals, monthly_totals = calculate_periodic_consumption(df)
            peak_loads = detect_meter_peak_loads(df)
            
            daily_dict = {str(k): float(v) for k, v in daily_totals.items()}
            weekly_dict = {str(k): float(v) for k, v in weekly_totals.items()}
            monthly_dict = {str(k): float(v) for k, v in monthly_totals.items()}
            
            peak_loads_copy = peak_loads.copy()
            peak_loads_copy["timestamp"] = peak_loads_copy["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
            peak_loads_list = peak_loads_copy.to_dict(orient="records")
            
            cache_payload = {
                "daily_totals": daily_dict,
                "weekly_totals": weekly_dict,
                "monthly_totals": monthly_dict,
                "peak_loads": peak_loads_list
            }
            cache_analytics_results(cache_key, cache_payload, ttl=3600)
            print("💾 [CACHE SAVE] Cached analytics results successfully in Redis.")

        print("⚡ Storing latest smart meter readings in Redis...")
        latest_stored_count = 0
        for _, row in df.iterrows():
            meter_id = row["meter_id"]
            timestamp_str = row["timestamp"].strftime("%Y-%m-%d %H:%M:%S") if isinstance(row["timestamp"], pd.Timestamp) else str(row["timestamp"])
            consumption = float(row["consumption_kw"])
            if store_latest_meter_reading(meter_id, timestamp_str, consumption):
                latest_stored_count += 1
        print(f"✅ Processed readings: Updated Redis for latest meter states (operations: {latest_stored_count}).")

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

        print("\n" + "-" * 60)
        print("PEAK LOAD DETECTION PER METER")
        print("-" * 60)
        for index, row in peak_loads.iterrows():
            print(f"Meter ID: {row['meter_id']} | Peak Load: {row['consumption_kw']:.2f} kW | Recorded At: {row['timestamp']}")

        threshold_value = 5.0
        
        print("\n" + "-" * 60)
        print("DAY 3: REAL-TIME OVERLOAD DETECTION")
        print("-" * 60)
        print(f"Active Threshold Monitor: {threshold_value:.2f} kW")
        
        overloads_df = detect_overloads(df, threshold=threshold_value)
        alerts = generate_alert_messages(overloads_df, threshold=threshold_value)
        print(f"Total Overload Incidents Flagged: {len(alerts)}")
        
        if alerts:
            print("\n--- Triggered Overload Alerts ---")
            for alert in alerts:
                indicator = "🚨 [CRITICAL]" if alert["severity"] == "CRITICAL" else "⚠️ [WARNING]"
                print(f"{indicator} Time: {alert['timestamp']} | Meter: {alert['meter_id']} | "
                      f"Load: {alert['consumption_kw']:.2f} kW | Exceeded By: {alert['consumption_kw'] - threshold_value:.2f} kW")
            
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
