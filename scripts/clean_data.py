# scripts/clean_data.py

import os
import pandas as pd
import argparse

def main():
    """
    Example script to clean or preprocess CSV data.
    1. Reads input CSV (default: data/raw/dataset.csv).
    2. Drops rows with NaN values.
    3. Optionally rename columns, convert data types, etc.
    4. Saves cleaned data (default: data/processed/cleaned_dataset.csv).
    """
    parser = argparse.ArgumentParser(description="Clean or preprocess CSV data.")
    parser.add_argument("--input", default="data/raw/dataset.csv", help="Path to input CSV file.")
    parser.add_argument("--output", default="data/processed/cleaned_dataset.csv", help="Path to output CSV file.")
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output

    if not os.path.exists(input_path):
        print(f"Input file not found: {input_path}")
        return

    # Load data
    df = pd.read_csv(input_path)
    print(f"Loaded dataset with shape {df.shape} from {input_path}")

    # Basic data cleaning example
    initial_rows = len(df)
    df.dropna(inplace=True)
    dropped_rows = initial_rows - len(df)
    print(f"Dropped {dropped_rows} rows with NaNs.")

    # Additional transformations (examples)
    # df.columns = [col.strip().lower() for col in df.columns]  # Standardize column names
    # df['some_column'] = df['some_column'].astype(int)

    # Save cleaned data
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path} with shape {df.shape}")

if __name__ == "__main__":
    main()
