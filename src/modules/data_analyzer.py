# src/modules/data_analyzer.py

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List, Union

# If you want optional scikit-learn usage
from sklearn.preprocessing import StandardScaler, MinMaxScaler


def analyze_data(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Performs a comprehensive analysis on the given pandas DataFrame.
    This may include:
      - Basic info (row count, columns)
      - Missing data checks
      - Statistical summaries
      - Correlation matrix or other relationships

    :param df: A pandas DataFrame containing your dataset.
    :return: A dictionary summarizing the analysis.
    """
    analysis_results = {}

    # Basic shape
    row_count, col_count = df.shape
    analysis_results["row_count"] = row_count
    analysis_results["column_count"] = col_count
    analysis_results["columns"] = list(df.columns)

    # Missing data count
    missing_counts = df.isnull().sum()
    analysis_results["missing_values"] = missing_counts.to_dict()

    # Basic stats (describe numerical columns)
    describe_numeric = df.describe(include=[np.number]).to_dict()
    analysis_results["numeric_summary"] = describe_numeric

    # Basic stats (describe categorical columns, if any)
    # Only if you want to handle object columns as well
    # describe_categorical = df.describe(include=["object", "category"]).to_dict()
    # analysis_results["categorical_summary"] = describe_categorical

    # Correlation matrix (for numeric columns), stored as nested dict
    # If row_count is large or you have many columns, you may consider skipping or limiting columns
    corr_matrix = df.select_dtypes(include=[np.number]).corr()
    analysis_results["correlation_matrix"] = corr_matrix.to_dict()

    return analysis_results


def detect_outliers_iqr(df: pd.DataFrame, columns: Optional[List[str]] = None, factor: float = 1.5) -> Dict[str, List[int]]:
    """
    Detects outliers in specified columns of a DataFrame using the IQR (Interquartile Range) method.

    :param df: A pandas DataFrame.
    :param columns: List of column names to check for outliers. If None, checks all numeric columns.
    :param factor: The IQR multiplier; 1.5 is common (3.0 for more stringent).
    :return: A dictionary where keys are column names and values are lists of row indices containing outliers.
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()

    outlier_indices = {}
    for col in columns:
        if col not in df.columns:
            continue
        series = df[col].dropna()
        if series.empty:
            continue

        q1 = np.percentile(series, 25)
        q3 = np.percentile(series, 75)
        iqr = q3 - q1
        lower_bound = q1 - (factor * iqr)
        upper_bound = q3 + (factor * iqr)

        col_outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)].index.tolist()
        if col_outliers:
            outlier_indices[col] = col_outliers

    return outlier_indices


def transform_data(
    df: pd.DataFrame,
    drop_duplicates: bool = True,
    dropna_threshold: Optional[float] = None,
    fillna_method: Optional[str] = None,
    numeric_scaling: Optional[str] = None,
    columns_to_scale: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Applies a series of transformations to prepare data for ML or other steps.
    This might include:
      - Dropping duplicates
      - Dropping rows/columns with excessive missing values
      - Filling missing values
      - Scaling numeric features (Standard or MinMax)

    :param df: A pandas DataFrame to transform.
    :param drop_duplicates: Whether to drop duplicate rows.
    :param dropna_threshold: If set, drops rows with missing values above a certain threshold (0-1).
        e.g., 0.5 => drop rows if >50% of the columns are NaN.
    :param fillna_method: How to fill missing values. e.g., 'mean', 'median', 'mode', or a constant.
        If None, missing values remain as is (unless dropped).
    :param numeric_scaling: If 'standard', applies StandardScaler; if 'minmax', applies MinMaxScaler; else None.
    :param columns_to_scale: A list of numeric columns to scale. If None, scales all numeric columns.
    :return: A transformed DataFrame.
    """

    df_transformed = df.copy()

    # 1. Drop duplicates
    if drop_duplicates:
        initial_rows = len(df_transformed)
        df_transformed.drop_duplicates(inplace=True)
        print(f"Dropped {initial_rows - len(df_transformed)} duplicate rows.")

    # 2. Drop rows based on missing value threshold
    if dropna_threshold is not None:
        # For each row, calculate fraction of missing
        thresh_count = int((1 - dropna_threshold) * df_transformed.shape[1])
        initial_rows = len(df_transformed)
        df_transformed.dropna(thresh=thresh_count, inplace=True)
        print(f"Dropped {initial_rows - len(df_transformed)} rows with > {int(dropna_threshold*100)}% missing values.")

    # 3. Fill missing values
    if fillna_method is not None:
        if fillna_method.lower() in ["mean", "median", "mode"]:
            numeric_cols = df_transformed.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if fillna_method.lower() == "mean":
                    fill_value = df_transformed[col].mean()
                elif fillna_method.lower() == "median":
                    fill_value = df_transformed[col].median()
                elif fillna_method.lower() == "mode":
                    fill_value = df_transformed[col].mode()[0] if not df_transformed[col].mode().empty else None
                df_transformed[col].fillna(fill_value, inplace=True)
        else:
            # Assume fillna_method is a constant or custom string
            df_transformed.fillna(fillna_method, inplace=True)
        print(f"Filled missing values using method: {fillna_method}")

    # 4. Numeric Scaling (Standard or MinMax)
    if numeric_scaling in ["standard", "minmax"]:
        numeric_cols = columns_to_scale
        if not numeric_cols:
            numeric_cols = df_transformed.select_dtypes(include=[np.number]).columns.tolist()

        if numeric_scaling == "standard":
            scaler = StandardScaler()
        else:  # 'minmax'
            scaler = MinMaxScaler()

        # Fit and transform
        df_transformed[numeric_cols] = scaler.fit_transform(df_transformed[numeric_cols])
        print(f"Scaled numeric columns ({numeric_scaling}): {numeric_cols}")

    print("Data transformation complete.")
    return df_transformed
