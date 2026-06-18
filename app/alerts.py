import os
import pandas as pd
from datetime import datetime

def detect_overloads(df: pd.DataFrame, threshold: float = 5.0) -> pd.DataFrame:
    """
    Filters the smart meter DataFrame to find records that exceed the consumption threshold.
    
    Parameters:
    df (pd.DataFrame): The input smart meter data containing 'timestamp', 'meter_id', and 'consumption_kw'.
    threshold (float): The load threshold (in kW) above which a consumption level is considered an overload.
                       Defaults to 5.0 kW.
                       
    Returns:
    pd.DataFrame: A filtered DataFrame containing only the records where consumption exceeds the threshold.
    """
    # Safety check: ensure required columns are present in the DataFrame
    required_cols = ["timestamp", "meter_id", "consumption_kw"]
    for col in required_cols:
        if col not in df.columns:
            raise KeyError(f"Missing required column '{col}' in smart meter DataFrame.")
            
    # Filter the DataFrame: keep only rows where consumption_kw is strictly greater than the threshold
    overloads_df = df[df["consumption_kw"] > threshold]
    
    # Return the filtered DataFrame (sorted by timestamp for cleaner output)
    return overloads_df.sort_values(by="timestamp")


def generate_alert_messages(overloads_df: pd.DataFrame, threshold: float = 5.0) -> list:
    """
    Converts a DataFrame of overload events into a list of structured alert dictionaries.
    
    Each alert contains details such as the timestamp, meter ID, consumption, threshold,
    severity, and a formatted descriptive alert message.
    
    Parameters:
    overloads_df (pd.DataFrame): DataFrame containing overload events (filtered smart meter data).
    threshold (float): The load threshold used for detection. Used to determine severity levels.
                       
    Returns:
    list: A list of dictionaries representing individual alerts.
    """
    alerts = []
    
    for _, row in overloads_df.iterrows():
        consumption = row["consumption_kw"]
        meter_id = row["meter_id"]
        # Format the timestamp for readability (handling string or datetime objects)
        if isinstance(row["timestamp"], pd.Timestamp):
            timestamp_str = row["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
        else:
            timestamp_str = str(row["timestamp"])
            
        # Determine Severity Level based on overload intensity
        # - CRITICAL: Consumption exceeds threshold by 30% or more (e.g., >= 6.5 kW when threshold is 5.0 kW)
        # - WARNING: Consumption exceeds threshold but is less than 30% over
        if consumption >= (threshold * 1.3):
            severity = "CRITICAL"
        else:
            severity = "WARNING"
            
        alert_msg = (
            f"ALERT [{severity}]: Meter {meter_id} exceeded threshold of {threshold:.2f} kW. "
            f"Current load is {consumption:.2f} kW."
        )
        
        # Build a structured alert dictionary
        alert_data = {
            "timestamp": timestamp_str,
            "meter_id": meter_id,
            "consumption_kw": consumption,
            "threshold_kw": threshold,
            "severity": severity,
            "message": alert_msg
        }
        alerts.append(alert_data)
        
    return alerts


def log_alerts_to_file(alerts: list, log_path: str = "data/alerts.log") -> None:
    """
    Appends generated alerts to a persistent text log file.
    
    Parameters:
    alerts (list): A list of structured alert dictionaries to log.
    log_path (str): The file path where alerts will be written. Defaults to 'data/alerts.log'.
    """
    if not alerts:
        return  # Nothing to log
        
    # Ensure the parent directory exists
    dir_name = os.path.dirname(log_path)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name)
        
    # Open the log file in append mode to prevent overwriting past logs
    with open(log_path, "a") as log_file:
        for alert in alerts:
            # Create a standardized, professional log entry format:
            # [YYYY-MM-DD HH:MM:SS] [SEVERITY] [Meter ID] -> Message
            log_entry = (
                f"[{alert['timestamp']}] [{alert['severity']}] "
                f"Meter: {alert['meter_id']} | Load: {alert['consumption_kw']:.2f} kW | "
                f"Threshold: {alert['threshold_kw']:.2f} kW | Msg: {alert['message']}\n"
            )
            log_file.write(log_entry)
            
    print(f"Successfully appended {len(alerts)} alert(s) to '{log_path}'.")
