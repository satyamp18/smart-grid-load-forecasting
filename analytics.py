import os
import pandas as pd

def run_grid_analytics(csv_path: str):
    """
    Reads smart meter consumption data from a CSV file and calculates
    essential metrics for smart grid load monitoring.
    """
    print("=" * 60)
    print("          SMART GRID LOAD ANALYTICS - DAY 1 REPORT          ")
    print("=" * 60)

    # Step 1: Check if the CSV file exists
    if not os.path.exists(csv_path):
        print(f"Error: The file '{csv_path}' was not found.")
        return

    # Step 2: Load the dataset using Pandas
    # pd.read_csv reads a comma-separated values file into a Pandas DataFrame.
    # A DataFrame is a two-dimensional, size-mutable, tabular data structure.
    df = pd.read_csv(csv_path)
    print(f"Successfully loaded dataset from: {csv_path}\n")
    print("First 5 rows of the dataset:")
    print(df.head(), "\n")

    # Step 3: Perform calculations
    
    # Calculate total consumption (summing all raw kW readings)
    # Since readings are hourly, the sum of kW matches total kWh for these hours.
    total_consumption = df["consumption_kw"].sum()

    # Calculate average consumption (mean of the consumption_kw column)
    average_consumption = df["consumption_kw"].mean()

    # Find the maximum load record
    # idxmax() returns the index of the maximum value in the column.
    max_load_idx = df["consumption_kw"].idxmax()
    max_load_row = df.loc[max_load_idx]
    
    max_load_value = max_load_row["consumption_kw"]
    max_load_time = max_load_row["timestamp"]
    max_load_meter = max_load_row["meter_id"]

    # Step 4: Overload Detection
    # Filter the DataFrame to keep only rows where consumption is greater than 5.0 kW.
    overload_threshold = 5.0
    overloads_df = df[df["consumption_kw"] > overload_threshold]

    # Step 5: Display metrics
    print("-" * 60)
    print("KEY METRICS:")
    print("-" * 60)
    print(f"Total Consumption: {total_consumption:.2f} kWh")
    print(f"Average Load:      {average_consumption:.2f} kW")
    print(f"Maximum Load:      {max_load_value:.2f} kW (Meter: {max_load_meter} at {max_load_time})")
    print("-" * 60)
    print(f"OVERLOAD DETECTION (Threshold > {overload_threshold} kW):")
    print("-" * 60)

    if not overloads_df.empty:
        print(f"Alert! Found {len(overloads_df)} overload events:")
        # We iterate over the rows of the filtered DataFrame and print each event.
        for index, row in overloads_df.iterrows():
            print(f"⚠️  Time: {row['timestamp']} | Meter: {row['meter_id']} | Load: {row['consumption_kw']} kW")
    else:
        print("✅ No overload events detected. Grid is operating normally.")
    print("=" * 60)

if __name__ == "__main__":
    # Define the path to the CSV file relative to the root directory
    data_file_path = os.path.join("data", "sample_meter_data.csv")
    run_grid_analytics(data_file_path)
