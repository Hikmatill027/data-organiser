import pandas as pd
import argparse
import os


def validate_path(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    if not file_path.lower().endswith((".csv", '.xlsx', '.json')):
        raise ValueError("Unsupported file format. Use CSV, Excel, or JSON.")


def read_data(file_path):
    validate_path(file_path)
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path, chunksize=1000)
    elif file_path.endswith('.xlsx'):
        return pd.read_excel(file_path)
    elif file_path.endswith('.json'):
        return pd.read_json(file_path, lines=True)
    else:
        raise ValueError("Unsupported file format. Use CSV or Exel.")


def clean_data(df, output_path, is_duplicate=True, sort_by=None, filters=None):
    # Clean Data
    if is_duplicate:
        df = df.drop_duplicates()

    if sort_by:
        df = df.sort_values(by=sort_by)

    if filters:
        for column, value in filters.items():
            df = df[df[column] == value]

    return df


def save_data(df, output_path, append=False):
    # Saving data
    if output_path.endswith('.csv'):
        df.to_csv(output_path, mode="a" if append else "w", header=not append, index=False)
    elif output_path.endswith('.xlsx'):
        with pd.ExcelWriter(output_path, mode="a" if append else "w") as writer:
            df.to_excel(writer, index=False)
    elif output_path.endswith('.json'):
        df.to_json(output_path, orient="records", indent=4, lines=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean and process data files.")
    parser.add_argument("input", help="Path to the file")
    parser.add_argument("output", help="Path to cleaned data")
    parser.add_argument("--is_duplicate", action="store_true", help="Remove duplicate rows")
    parser.add_argument("--sort_by", help="Column to sort the data by.")
    parser.add_argument("--filters", nargs="+", help="Filters in 'column=value' format")
