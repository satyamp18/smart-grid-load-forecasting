"""
Smart Grid Load Analytics Module
--------------------------------
This module provides utility functions for reading smart meter load profiles,
generating daily, weekly, and monthly aggregate consumption reports,
and detecting peak load consumption per smart meter.

Dependencies: pandas, os
"""

import os
import pandas as pd

def load_smart_meter_data(csv_path: str) -> pd.DataFrame:
    """
    Loads smart meter reading files from a CSV database.

    Parameters:
        csv_path (str): File path to the raw smart meter CSV data.

    Returns:
        pd.DataFrame: A parsed Pandas DataFrame containing standard types.

    Raises:
        FileNotFoundError: If the specified CSV path does not exist.
    """
    # Verify file existence before reading
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Database error: File '{csv_path}' not found.")
        
    df = pd.read_csv(csv_path)
    
    # Convert 'timestamp' to datetime datatype to enable datetime grouping functions
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    
    return df

def calculate_periodic_consumption(df: pd.DataFrame) -> tuple:
    """
    Calculates total energy consumption (kWh) over Day, Week, and Month periods.

    Parameters:
        df (pd.DataFrame): Dataframe containing 'timestamp' and 'consumption_kw' columns.

    Returns:
        tuple: A tuple containing daily, weekly, and monthly aggregate Series.
    """
    # Group by Daily Period ('D') and sum electricity consumption
    daily_totals = df.groupby(df["timestamp"].dt.to_period("D"))["consumption_kw"].sum()

    # Group by Weekly Period ('W') and sum electricity consumption
    weekly_totals = df.groupby(df["timestamp"].dt.to_period("W"))["consumption_kw"].sum()

    # Group by Monthly Period ('M') and sum electricity consumption
    monthly_totals = df.groupby(df["timestamp"].dt.to_period("M"))["consumption_kw"].sum()

    return daily_totals, weekly_totals, monthly_totals

def detect_meter_peak_loads(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detects the peak consumption reading and corresponding timestamp for each meter.

    Parameters:
        df (pd.DataFrame): Dataframe containing 'meter_id', 'consumption_kw', and 'timestamp'.

    Returns:
        pd.DataFrame: Filtered Dataframe representing the peak readings.
    """
    # Find the row index of max load for each individual meter group
    peak_indices = df.groupby("meter_id")["consumption_kw"].idxmax()
    
    # Locate the full row data based on peak index values
    peak_loads_df = df.loc[peak_indices]
    
    return peak_loads_df

def generate_formatted_reports(csv_path: str) -> None:
    """
    Orchestrates data loading, aggregation, calculations, and prints formatted report.

    Parameters:
        csv_path (str): Relative or absolute path to the target smart meter CSV.
    """
    print("=" * 60)
    print("          SMART GRID LOAD ANALYTICS - DAY 2 REPORT          ")
    print("=" * 60)

    try:
        # Step 1: Load and parse the CSV database
        df = load_smart_meter_data(csv_path)
        print(f"Dataset successfully loaded from: {csv_path}\n")
        
        # Step 2: Extract daily, weekly, and monthly calculations
        daily_totals, weekly_totals, monthly_totals = calculate_periodic_consumption(df)
        
        # Display Periodic Reports
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

        # Step 3: Detect and display peak load per meter
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
    # Define the local data file location
    data_file_path = os.path.join("data", "sample_meter_data.csv")
    generate_formatted_reports(data_file_path)
