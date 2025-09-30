"""
Data processing module for FireAnalyst.

This module handles data loading, cleaning, and validation of California wildfire data.
All functions are designed to be reproducible and include comprehensive error handling.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Dict, Optional
import warnings

from src.config import (
    RAW_DATA_PATH,
    CLEANED_DATA_PATH,
    COLUMNS_TO_DROP,
    ESSENTIAL_COLUMNS,
    VALIDATION_CONFIG,
    CONTAINMENT_METHOD_MAPPING,
    FIRE_CAUSE_MAPPING
)


def load_data(file_path: Optional[Path] = None) -> pd.DataFrame:
    """
    Load wildfire data from CSV file.

    Parameters
    ----------
    file_path : Path, optional
        Path to the CSV file. If None, uses default RAW_DATA_PATH from config.

    Returns
    -------
    pd.DataFrame
        Raw wildfire dataset

    Raises
    ------
    FileNotFoundError
        If the specified file does not exist
    """
    if file_path is None:
        file_path = RAW_DATA_PATH

    if not Path(file_path).exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")

    df = pd.read_csv(file_path)
    print(f"[OK] Loaded {len(df):,} records from {Path(file_path).name}")
    return df


def clean_fire_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the wildfire dataset by handling missing values and formatting columns.

    This function performs the following operations:
    1. Removes rows with missing essential columns
    2. Converts data types to appropriate formats
    3. Drops columns with limited analytical utility
    4. Fills missing categorical values with placeholders
    5. Standardizes formatting

    Parameters
    ----------
    df : pd.DataFrame
        Raw wildfire dataset

    Returns
    -------
    pd.DataFrame
        Cleaned wildfire dataset

    Notes
    -----
    This function creates a copy of the input dataframe to avoid
    unintended side effects on the original data.
    """
    df = df.copy()
    initial_rows = len(df)

    # Drop rows where essential columns are missing
    df = df.dropna(subset=ESSENTIAL_COLUMNS[:2])  # YEAR_ and GIS_ACRES

    # Convert YEAR_ to integer
    df['YEAR_'] = df['YEAR_'].astype(int)

    # Convert date columns to datetime
    for date_col in ['ALARM_DATE', 'CONT_DATE']:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

    # Drop columns with excessive missing data or limited utility
    df = df.drop(columns=[col for col in COLUMNS_TO_DROP if col in df.columns])

    # Fill missing categorical data with placeholders
    df['AGENCY'] = df['AGENCY'].fillna('Unknown')
    df['UNIT_ID'] = df['UNIT_ID'].fillna('Unknown')
    df['FIRE_NAME'] = df['FIRE_NAME'].fillna('Unnamed Fire')
    df['STATE'] = df['STATE'].astype(str)

    rows_dropped = initial_rows - len(df)
    print(f"[OK] Cleaned data: {rows_dropped:,} rows removed, {len(df):,} rows retained")

    return df


def validate_fire_data(df: pd.DataFrame, verbose: bool = True) -> Tuple[pd.DataFrame, Dict]:
    """
    Validate wildfire dataset for data quality issues.

    Performs comprehensive validation checks:
    1. Date logic consistency (containment after alarm)
    2. Future date detection
    3. Outlier detection using IQR method
    4. Extreme duration detection
    5. Invalid acre values
    6. Year range validation

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned wildfire dataset
    verbose : bool, default True
        If True, prints detailed validation report

    Returns
    -------
    Tuple[pd.DataFrame, Dict]
        - Validated dataframe with problematic rows removed
        - Dictionary containing validation statistics and issues

    Notes
    -----
    This function removes rows that fail critical validation checks.
    The validation statistics dictionary contains keys:
    - 'initial_rows': Number of rows before validation
    - 'final_rows': Number of rows after validation
    - 'rows_removed': Number of rows removed
    - 'issues': List of validation issues found
    - 'outlier_count': Number of outlier fires detected
    """
    df = df.copy()
    validation_stats = {
        'initial_rows': len(df),
        'issues': [],
        'outlier_count': 0
    }

    if verbose:
        print("=" * 60)
        print("DATA VALIDATION REPORT")
        print("=" * 60)

    # 1. Check date logic: CONT_DATE should be after ALARM_DATE
    df['ALARM_DATE'] = pd.to_datetime(df['ALARM_DATE'], errors='coerce')
    df['CONT_DATE'] = pd.to_datetime(df['CONT_DATE'], errors='coerce')

    invalid_dates = df[df['CONT_DATE'] < df['ALARM_DATE']]
    if len(invalid_dates) > 0:
        if verbose:
            print(f"[WARN]  {len(invalid_dates)} rows have containment date before alarm date")
        validation_stats['issues'].append(f"Invalid date logic: {len(invalid_dates)} rows")
        df = df[df['CONT_DATE'] >= df['ALARM_DATE']]
    else:
        if verbose:
            print("[PASS] All dates follow correct logic (containment after alarm)")

    # 2. Check for future dates (handle timezone-aware datetimes)
    today = pd.Timestamp.now(tz='UTC')
    future_alarms = df[df['ALARM_DATE'] > today]
    future_cont = df[df['CONT_DATE'] > today]
    if len(future_alarms) > 0 or len(future_cont) > 0:
        if verbose:
            print(f"[WARN]  {len(future_alarms)} alarm dates and {len(future_cont)} containment dates are in the future")
        validation_stats['issues'].append(f"Future dates detected")
    else:
        if verbose:
            print("[PASS] No future dates detected")

    # 3. Check for outliers in GIS_ACRES using IQR method
    Q1 = df['GIS_ACRES'].quantile(0.25)
    Q3 = df['GIS_ACRES'].quantile(0.75)
    IQR = Q3 - Q1
    multiplier = VALIDATION_CONFIG['outlier_iqr_multiplier']
    lower_bound = Q1 - multiplier * IQR
    upper_bound = Q3 + multiplier * IQR

    acres_outliers = df[(df['GIS_ACRES'] < lower_bound) | (df['GIS_ACRES'] > upper_bound)]
    validation_stats['outlier_count'] = len(acres_outliers)

    if verbose:
        print(f"📊 Acres outliers ({multiplier}×IQR): {len(acres_outliers)} fires ({len(acres_outliers)/len(df)*100:.1f}%)")
        print(f"   Range: {df['GIS_ACRES'].min():.1f} to {df['GIS_ACRES'].max():.1f} acres")
        print(f"   Median: {df['GIS_ACRES'].median():.1f} acres")

    # 4. Check containment duration outliers
    df['Containment_Duration'] = (df['CONT_DATE'] - df['ALARM_DATE']).dt.total_seconds() / 3600
    max_hours = VALIDATION_CONFIG['max_containment_hours']
    duration_outliers = df[df['Containment_Duration'] > max_hours]

    if len(duration_outliers) > 0:
        if verbose:
            print(f"[WARN]  {len(duration_outliers)} fires took longer than 1 year to contain")
        validation_stats['issues'].append(f"Extreme durations: {len(duration_outliers)} rows")
    else:
        if verbose:
            print("[PASS] All containment durations are reasonable (<1 year)")

    # 5. Check for negative or zero acres
    invalid_acres = df[df['GIS_ACRES'] <= 0]
    if len(invalid_acres) > 0:
        if verbose:
            print(f"[WARN]  {len(invalid_acres)} fires have zero or negative acres")
        validation_stats['issues'].append(f"Invalid acres: {len(invalid_acres)} rows")
        df = df[df['GIS_ACRES'] > 0]
    else:
        if verbose:
            print("[PASS] All fire acres are positive")

    # 6. Check year range
    year_min = df['YEAR_'].min()
    year_max = df['YEAR_'].max()
    if verbose:
        print(f"📅 Year range: {int(year_min)} to {int(year_max)}")

    # Summary
    validation_stats['final_rows'] = len(df)
    validation_stats['rows_removed'] = validation_stats['initial_rows'] - validation_stats['final_rows']

    if verbose:
        print("=" * 60)
        print(f"Rows removed: {validation_stats['rows_removed']:,} ({validation_stats['rows_removed']/validation_stats['initial_rows']*100:.1f}%)")
        print(f"Rows retained: {validation_stats['final_rows']:,} ({validation_stats['final_rows']/validation_stats['initial_rows']*100:.1f}%)")

        if len(validation_stats['issues']) == 0:
            print("[PASS] No critical validation issues found")
        else:
            print(f"[WARN]  {len(validation_stats['issues'])} validation issue(s) found")

        print("=" * 60)

    return df, validation_stats


def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add derived columns for analysis.

    Adds the following computed columns:
    - Containment_Duration: Time in hours from alarm to containment
    - Month: Month of alarm date (1-12)
    - Decade: Decade of fire occurrence
    - C_METHOD_DESCRIPTION: Human-readable containment method
    - CAUSE_DESCRIPTION: Human-readable fire cause

    Parameters
    ----------
    df : pd.DataFrame
        Validated wildfire dataset

    Returns
    -------
    pd.DataFrame
        Dataset with additional derived columns
    """
    df = df.copy()

    # Calculate containment duration in hours
    df['Containment_Duration'] = (
        (df['CONT_DATE'] - df['ALARM_DATE']).dt.total_seconds() / 3600
    )

    # Remove invalid durations (zero or negative)
    df = df[df['Containment_Duration'] > 0]

    # Extract month from alarm date
    df['Month'] = df['ALARM_DATE'].dt.month

    # Calculate decade
    df['Decade'] = (df['YEAR_'] // 10) * 10

    # Map containment method codes to descriptions
    if 'C_METHOD' in df.columns:
        df['C_METHOD_DESCRIPTION'] = df['C_METHOD'].map(CONTAINMENT_METHOD_MAPPING)

    # Map cause codes to descriptions
    if 'CAUSE' in df.columns:
        df['CAUSE_DESCRIPTION'] = df['CAUSE'].map(FIRE_CAUSE_MAPPING)

    print(f"[OK] Added {5} derived columns for analysis")

    return df


def save_cleaned_data(df: pd.DataFrame, output_path: Optional[Path] = None) -> None:
    """
    Save cleaned and validated data to CSV file.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned and validated dataset
    output_path : Path, optional
        Output file path. If None, uses default CLEANED_DATA_PATH from config.
    """
    if output_path is None:
        output_path = CLEANED_DATA_PATH

    df.to_csv(output_path, index=False)
    print(f"[OK] Saved cleaned data to {Path(output_path).name}")


def full_pipeline(input_path: Optional[Path] = None,
                 output_path: Optional[Path] = None,
                 verbose: bool = True) -> Tuple[pd.DataFrame, Dict]:
    """
    Execute complete data processing pipeline.

    This is a convenience function that runs the entire data processing workflow:
    1. Load raw data
    2. Clean data
    3. Validate data
    4. Add derived columns
    5. Save cleaned data

    Parameters
    ----------
    input_path : Path, optional
        Path to raw data file
    output_path : Path, optional
        Path to save cleaned data
    verbose : bool, default True
        If True, prints progress messages

    Returns
    -------
    Tuple[pd.DataFrame, Dict]
        - Processed dataframe ready for analysis
        - Validation statistics dictionary

    Examples
    --------
    >>> from src.data_processing import full_pipeline
    >>> df, stats = full_pipeline()
    >>> print(f"Processed {len(df)} fire records")
    """
    if verbose:
        print("\n" + "="*60)
        print("FIRE DATA PROCESSING PIPELINE")
        print("="*60 + "\n")

    # Load data
    df = load_data(input_path)

    # Clean data
    df = clean_fire_data(df)

    # Validate data
    df, validation_stats = validate_fire_data(df, verbose=verbose)

    # Add derived columns
    df = add_derived_columns(df)

    # Save cleaned data
    save_cleaned_data(df, output_path)

    if verbose:
        print(f"\n[PASS] Pipeline complete! Final dataset: {len(df):,} records")

    return df, validation_stats