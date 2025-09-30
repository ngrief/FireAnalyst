import pandas as pd
import numpy as np
import sys

# Set UTF-8 encoding for output
sys.stdout.reconfigure(encoding='utf-8')

def validate_fire_data(df):
    """Validates fire dataset for data quality issues."""
    print("=" * 60)
    print("DATA VALIDATION REPORT")
    print("=" * 60)

    validation_issues = []
    initial_rows = len(df)

    # 1. Check date logic
    df['ALARM_DATE'] = pd.to_datetime(df['ALARM_DATE'], errors='coerce')
    df['CONT_DATE'] = pd.to_datetime(df['CONT_DATE'], errors='coerce')

    invalid_dates = df[df['CONT_DATE'] < df['ALARM_DATE']]
    if len(invalid_dates) > 0:
        print(f"WARNING: {len(invalid_dates)} rows have containment date before alarm date")
        validation_issues.append(f"Invalid date logic: {len(invalid_dates)} rows")
        df = df[df['CONT_DATE'] >= df['ALARM_DATE']]
    else:
        print("PASS: All dates follow correct logic (containment after alarm)")

    # 2. Check for future dates
    today = pd.Timestamp.now(tz='UTC')
    future_alarms = df[df['ALARM_DATE'] > today]
    future_cont = df[df['CONT_DATE'] > today]
    if len(future_alarms) > 0 or len(future_cont) > 0:
        print(f"WARNING: {len(future_alarms)} alarm dates and {len(future_cont)} containment dates are in the future")
        validation_issues.append(f"Future dates detected")
    else:
        print("PASS: No future dates detected")

    # 3. Check for outliers in GIS_ACRES
    Q1 = df['GIS_ACRES'].quantile(0.25)
    Q3 = df['GIS_ACRES'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 3 * IQR
    upper_bound = Q3 + 3 * IQR

    acres_outliers = df[(df['GIS_ACRES'] < lower_bound) | (df['GIS_ACRES'] > upper_bound)]
    print(f"INFO: Acres outliers (3×IQR): {len(acres_outliers)} fires ({len(acres_outliers)/len(df)*100:.1f}%)")
    print(f"   Range: {df['GIS_ACRES'].min():.1f} to {df['GIS_ACRES'].max():.1f} acres")
    print(f"   Median: {df['GIS_ACRES'].median():.1f} acres")

    # 4. Check containment duration outliers
    df['Duration_Hours'] = (df['CONT_DATE'] - df['ALARM_DATE']).dt.total_seconds() / 3600
    duration_outliers = df[df['Duration_Hours'] > 8760]
    if len(duration_outliers) > 0:
        print(f"WARNING: {len(duration_outliers)} fires took longer than 1 year to contain")
        validation_issues.append(f"Extreme durations: {len(duration_outliers)} rows")
    else:
        print("PASS: All containment durations are reasonable (<1 year)")

    # 5. Check for negative or zero acres
    invalid_acres = df[df['GIS_ACRES'] <= 0]
    if len(invalid_acres) > 0:
        print(f"WARNING: {len(invalid_acres)} fires have zero or negative acres")
        validation_issues.append(f"Invalid acres: {len(invalid_acres)} rows")
        df = df[df['GIS_ACRES'] > 0]
    else:
        print("PASS: All fire acres are positive")

    # 6. Check year range
    year_min = df['YEAR_'].min()
    year_max = df['YEAR_'].max()
    print(f"INFO: Year range: {int(year_min)} to {int(year_max)}")

    # Summary
    print("=" * 60)
    rows_removed = initial_rows - len(df)
    print(f"Rows removed: {rows_removed} ({rows_removed/initial_rows*100:.1f}%)")
    print(f"Rows retained: {len(df)} ({len(df)/initial_rows*100:.1f}%)")

    if len(validation_issues) == 0:
        print("PASS: No critical validation issues found")
    else:
        print(f"WARNING: {len(validation_issues)} validation issues found")

    print("=" * 60)

    return df

def clean_fire_data(df):
    """Cleans the fire dataset."""
    df = df.dropna(subset=['YEAR_', 'GIS_ACRES'])
    df.loc[:, 'YEAR_'] = df['YEAR_'].astype(int)
    for date_col in ['ALARM_DATE', 'CONT_DATE']:
        df.loc[:, date_col] = pd.to_datetime(df[date_col], errors='coerce')
    columns_to_drop = ['COMMENTS', 'COMPLEX_NAME', 'IRWINID', 'COMPLEX_ID', 'FIRE_NUM']
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])
    df.loc[:, 'AGENCY'] = df['AGENCY'].fillna('Unknown')
    df.loc[:, 'UNIT_ID'] = df['UNIT_ID'].fillna('Unknown')
    df.loc[:, 'FIRE_NAME'] = df['FIRE_NAME'].fillna('Unnamed Fire')
    df.loc[:, 'STATE'] = df['STATE'].astype(str)
    return df

# Test the functions
print("Testing Phase 1 improvements...")
print()

file_path = './Resources/California_Fire_Perimeters_(all).csv'
fire_data = pd.read_csv(file_path)
print(f"Loaded {len(fire_data)} rows from dataset\n")

cleaned_fire_data = clean_fire_data(fire_data)
cleaned_fire_data = validate_fire_data(cleaned_fire_data)

cleaned_fire_data.to_csv('Resources/cleaned_fire_data_test.csv', index=False)
print(f"\nFinal dataset: {len(cleaned_fire_data)} rows")
print("PASS: Phase 1 test completed successfully!")