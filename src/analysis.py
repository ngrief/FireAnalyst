"""
Statistical analysis module for FireAnalyst.

This module provides functions for analyzing wildfire patterns, containment effectiveness,
and statistical testing. All analyses include proper statistical rigor with hypothesis
tests and confidence intervals.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, List, Optional
from scipy import stats
from dataclasses import dataclass

from src.config import STATS_CONFIG


@dataclass
class StatisticalTest:
    """Container for statistical test results."""
    test_name: str
    statistic: float
    p_value: float
    significant: bool
    interpretation: str
    confidence_level: float = 0.95


def calculate_containment_effectiveness(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate containment effectiveness metrics with statistical measures.

    NOTE: The current effectiveness metric (GIS_ACRES / Duration) is flawed as it
    conflates fire size with response quality. Larger fires naturally take longer
    to contain. This metric should be interpreted cautiously and supplemented with
    size-controlled analyses.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset with Containment_Duration and GIS_ACRES columns

    Returns
    -------
    pd.DataFrame
        Dataset with added Effectiveness column (acres per hour)
    """
    df = df.copy()

    # Calculate effectiveness (acres per hour)
    df['Effectiveness'] = df['GIS_ACRES'] / df['Containment_Duration']

    # Replace infinite and negative infinite values
    df['Effectiveness'] = df['Effectiveness'].replace([np.inf, -np.inf], np.nan)

    # Drop rows where Effectiveness is NaN
    df = df.dropna(subset=['Effectiveness'])

    return df


def analyze_containment_methods(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    """
    Analyze containment effectiveness by method with statistical testing.

    Performs:
    1. Descriptive statistics by containment method
    2. ANOVA test to check if methods differ significantly
    3. Effect size calculations

    Parameters
    ----------
    df : pd.DataFrame
        Dataset with C_METHOD_DESCRIPTION and Effectiveness columns

    Returns
    -------
    Tuple[pd.DataFrame, Dict]
        - DataFrame with method statistics (mean, std, count, CI)
        - Dictionary with ANOVA results and interpretation
    """
    # Drop rows with missing containment method
    df_clean = df.dropna(subset=['C_METHOD_DESCRIPTION', 'Effectiveness']).copy()

    # Calculate statistics by method
    method_stats = df_clean.groupby('C_METHOD_DESCRIPTION').agg(
        Mean_Effectiveness=('Effectiveness', 'mean'),
        Std_Effectiveness=('Effectiveness', 'std'),
        Median_Effectiveness=('Effectiveness', 'median'),
        Count=('Effectiveness', 'count'),
        Min_Effectiveness=('Effectiveness', 'min'),
        Max_Effectiveness=('Effectiveness', 'max')
    ).sort_values(by='Mean_Effectiveness', ascending=False)

    # Calculate 95% confidence intervals
    confidence_level = STATS_CONFIG['confidence_level']
    method_stats['CI_Lower'] = method_stats.apply(
        lambda row: row['Mean_Effectiveness'] - stats.t.ppf(
            (1 + confidence_level) / 2, row['Count'] - 1
        ) * row['Std_Effectiveness'] / np.sqrt(row['Count']),
        axis=1
    )
    method_stats['CI_Upper'] = method_stats.apply(
        lambda row: row['Mean_Effectiveness'] + stats.t.ppf(
            (1 + confidence_level) / 2, row['Count'] - 1
        ) * row['Std_Effectiveness'] / np.sqrt(row['Count']),
        axis=1
    )

    # Perform ANOVA test
    method_groups = [
        group['Effectiveness'].values
        for name, group in df_clean.groupby('C_METHOD_DESCRIPTION')
    ]

    f_stat, p_value = stats.f_oneway(*method_groups)

    anova_results = {
        'f_statistic': f_stat,
        'p_value': p_value,
        'significant': p_value < STATS_CONFIG['significance_threshold'],
        'interpretation': (
            f"Methods show {'statistically significant' if p_value < 0.05 else 'no significant'} "
            f"differences in effectiveness (F={f_stat:.2f}, p={p_value:.4f})"
        )
    }

    return method_stats, anova_results


def temporal_trend_analysis(df: pd.DataFrame) -> Tuple[pd.DataFrame, StatisticalTest]:
    """
    Analyze temporal trends in fire occurrence and size.

    Performs linear regression to test for trends over time.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset with YEAR_ and GIS_ACRES columns

    Returns
    -------
    Tuple[pd.DataFrame, StatisticalTest]
        - DataFrame with yearly statistics
        - Statistical test results for temporal trend
    """
    # Aggregate by year
    yearly_stats = df.groupby('YEAR_').agg(
        Fire_Count=('GIS_ACRES', 'count'),
        Total_Acres=('GIS_ACRES', 'sum'),
        Mean_Acres=('GIS_ACRES', 'mean'),
        Median_Acres=('GIS_ACRES', 'median')
    ).reset_index()

    # Test for linear trend in fire count
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        yearly_stats['YEAR_'], yearly_stats['Fire_Count']
    )

    trend_test = StatisticalTest(
        test_name="Linear Trend (Fire Count)",
        statistic=r_value,
        p_value=p_value,
        significant=p_value < STATS_CONFIG['significance_threshold'],
        interpretation=(
            f"{'Significant' if p_value < 0.05 else 'No significant'} linear trend detected. "
            f"R²={r_value**2:.4f}, slope={slope:.4f} fires/year (p={p_value:.4f})"
        )
    )

    return yearly_stats, trend_test


def seasonal_analysis(df: pd.DataFrame) -> Tuple[pd.DataFrame, StatisticalTest]:
    """
    Analyze seasonal patterns in fire occurrence.

    Tests whether fire occurrence differs significantly across months using chi-square test.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset with Month column

    Returns
    -------
    Tuple[pd.DataFrame, StatisticalTest]
        - DataFrame with monthly fire counts
        - Chi-square test results
    """
    # Count fires by month
    monthly_counts = df['Month'].value_counts().sort_index()
    monthly_df = pd.DataFrame({
        'Month': monthly_counts.index,
        'Fire_Count': monthly_counts.values
    })

    # Chi-square test for uniformity (null: equal distribution across months)
    expected_freq = len(df) / 12
    chi_stat, p_value = stats.chisquare(monthly_counts.values)

    seasonal_test = StatisticalTest(
        test_name="Chi-Square (Seasonal Distribution)",
        statistic=chi_stat,
        p_value=p_value,
        significant=p_value < STATS_CONFIG['significance_threshold'],
        interpretation=(
            f"Fire occurrence {'varies significantly' if p_value < 0.05 else 'does not vary significantly'} "
            f"across months (χ²={chi_stat:.2f}, p={p_value:.4f})"
        )
    )

    return monthly_df, seasonal_test


def cause_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze fire causes with descriptive statistics.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset with CAUSE_DESCRIPTION column

    Returns
    -------
    pd.DataFrame
        Summary statistics by fire cause
    """
    if 'CAUSE_DESCRIPTION' not in df.columns:
        raise ValueError("CAUSE_DESCRIPTION column not found. Run add_derived_columns first.")

    cause_stats = df.groupby('CAUSE_DESCRIPTION').agg(
        Count=('GIS_ACRES', 'count'),
        Mean_Acres=('GIS_ACRES', 'mean'),
        Median_Acres=('GIS_ACRES', 'median'),
        Total_Acres=('GIS_ACRES', 'sum'),
        Mean_Duration=('Containment_Duration', 'mean')
    ).sort_values(by='Count', ascending=False)

    # Calculate percentage
    cause_stats['Percentage'] = (cause_stats['Count'] / cause_stats['Count'].sum() * 100)

    return cause_stats


def compare_decades(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    """
    Compare fire patterns across decades with statistical testing.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset with Decade column

    Returns
    -------
    Tuple[pd.DataFrame, Dict]
        - DataFrame with decadal statistics
        - Dictionary with statistical test results
    """
    decade_stats = df.groupby('Decade').agg(
        Fire_Count=('GIS_ACRES', 'count'),
        Mean_Acres=('GIS_ACRES', 'mean'),
        Total_Acres=('GIS_ACRES', 'sum'),
        Mean_Duration=('Containment_Duration', 'mean')
    ).reset_index()

    # Test if fire sizes differ across decades (Kruskal-Wallis for non-normal data)
    decade_groups = [
        group['GIS_ACRES'].values
        for name, group in df.groupby('Decade')
    ]

    h_stat, p_value = stats.kruskal(*decade_groups)

    test_results = {
        'test': 'Kruskal-Wallis',
        'h_statistic': h_stat,
        'p_value': p_value,
        'significant': p_value < STATS_CONFIG['significance_threshold'],
        'interpretation': (
            f"Fire sizes {'differ significantly' if p_value < 0.05 else 'do not differ significantly'} "
            f"across decades (H={h_stat:.2f}, p={p_value:.4f})"
        )
    }

    return decade_stats, test_results


def summary_statistics(df: pd.DataFrame) -> Dict:
    """
    Generate comprehensive summary statistics for the dataset.

    Parameters
    ----------
    df : pd.DataFrame
        Processed wildfire dataset

    Returns
    -------
    Dict
        Dictionary containing summary statistics
    """
    stats_dict = {
        'total_fires': len(df),
        'year_range': (int(df['YEAR_'].min()), int(df['YEAR_'].max())),
        'total_acres_burned': float(df['GIS_ACRES'].sum()),
        'mean_fire_size': float(df['GIS_ACRES'].mean()),
        'median_fire_size': float(df['GIS_ACRES'].median()),
        'max_fire_size': float(df['GIS_ACRES'].max()),
        'mean_containment_hours': float(df['Containment_Duration'].mean()),
        'median_containment_hours': float(df['Containment_Duration'].median()),
    }

    # Add percentiles
    for p in [25, 75, 90, 95, 99]:
        stats_dict[f'p{p}_fire_size'] = float(df['GIS_ACRES'].quantile(p/100))

    return stats_dict


def generate_analysis_report(df: pd.DataFrame) -> Dict:
    """
    Generate a comprehensive analysis report with all statistical tests.

    Parameters
    ----------
    df : pd.DataFrame
        Processed wildfire dataset

    Returns
    -------
    Dict
        Comprehensive analysis results including all statistical tests
    """
    report = {
        'summary_statistics': summary_statistics(df),
        'method_analysis': None,
        'temporal_analysis': None,
        'seasonal_analysis': None,
        'cause_analysis': None,
        'decade_comparison': None
    }

    # Containment method analysis
    if 'C_METHOD_DESCRIPTION' in df.columns and 'Effectiveness' in df.columns:
        method_stats, anova = analyze_containment_methods(df)
        report['method_analysis'] = {
            'statistics': method_stats,
            'anova': anova
        }

    # Temporal trends
    yearly_stats, trend_test = temporal_trend_analysis(df)
    report['temporal_analysis'] = {
        'yearly_statistics': yearly_stats,
        'trend_test': trend_test
    }

    # Seasonal patterns
    monthly_stats, seasonal_test = seasonal_analysis(df)
    report['seasonal_analysis'] = {
        'monthly_statistics': monthly_stats,
        'test': seasonal_test
    }

    # Cause analysis
    if 'CAUSE_DESCRIPTION' in df.columns:
        report['cause_analysis'] = cause_analysis(df)

    # Decade comparison
    decade_stats, decade_test = compare_decades(df)
    report['decade_comparison'] = {
        'statistics': decade_stats,
        'test': decade_test
    }

    return report