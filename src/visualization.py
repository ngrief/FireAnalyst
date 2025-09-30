"""
Visualization module for FireAnalyst.

This module provides publication-quality visualizations for wildfire analysis,
including temporal trends, spatial patterns, and comparative analyses.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Optional, Tuple, List

from src.config import VIZ_CONFIG, OUTPUT_DIR


# Set default style
sns.set_style("whitegrid")
sns.set_palette(VIZ_CONFIG['color_palette'])
plt.rcParams['figure.dpi'] = VIZ_CONFIG['figure_dpi']
plt.rcParams['savefig.dpi'] = VIZ_CONFIG['figure_dpi']
plt.rcParams['font.size'] = VIZ_CONFIG['font_size']['tick']


def save_figure(fig: plt.Figure, filename: str, subdir: str = "figures") -> None:
    """
    Save figure to output directory with consistent formatting.

    Parameters
    ----------
    fig : plt.Figure
        Matplotlib figure object
    filename : str
        Output filename (without extension)
    subdir : str, default "figures"
        Subdirectory within output folder
    """
    output_path = OUTPUT_DIR / subdir / f"{filename}.{VIZ_CONFIG['figure_format']}"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, bbox_inches='tight', dpi=VIZ_CONFIG['figure_dpi'])
    print(f"  [OK] Saved: {output_path.name}")
    plt.close(fig)


def plot_fires_over_time(df: pd.DataFrame, save: bool = True) -> plt.Figure:
    """
    Plot number of fires over time with trend line.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset with YEAR_ column
    save : bool, default True
        If True, saves figure to output directory

    Returns
    -------
    plt.Figure
        Matplotlib figure object
    """
    fires_per_year = df.groupby('YEAR_').size()

    fig, ax = plt.subplots(figsize=VIZ_CONFIG['default_figsize'])

    # Plot data
    ax.plot(fires_per_year.index, fires_per_year.values, marker='o',
            linewidth=2, markersize=4, color='#e74c3c', alpha=0.7)

    # Add trend line
    z = np.polyfit(fires_per_year.index, fires_per_year.values, 1)
    p = np.poly1d(z)
    ax.plot(fires_per_year.index, p(fires_per_year.index),
            "--", alpha=0.6, color='#2c3e50', linewidth=2,
            label=f'Trend: {z[0]:.2f} fires/year')

    ax.set_title('Wildfire Occurrence Over Time (1878-2023)',
                fontsize=VIZ_CONFIG['font_size']['title'], fontweight='bold')
    ax.set_xlabel('Year', fontsize=VIZ_CONFIG['font_size']['label'])
    ax.set_ylabel('Number of Fires', fontsize=VIZ_CONFIG['font_size']['label'])
    ax.legend(loc='best', fontsize=VIZ_CONFIG['font_size']['tick'])
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if save:
        save_figure(fig, 'fires_over_time')

    return fig


def plot_peak_years(df: pd.DataFrame, top_n: int = 10, save: bool = True) -> plt.Figure:
    """
    Plot peak years for fire occurrence.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset with YEAR_ column
    top_n : int, default 10
        Number of top years to display
    save : bool, default True
        If True, saves figure to output directory

    Returns
    -------
    plt.Figure
        Matplotlib figure object
    """
    fires_per_year = df.groupby('YEAR_').size()
    peak_years = fires_per_year.sort_values(ascending=False).head(top_n).sort_index()

    fig, ax = plt.subplots(figsize=VIZ_CONFIG['default_figsize'])

    bars = ax.bar(peak_years.index, peak_years.values, color='#e67e22',
                  edgecolor='black', linewidth=1.5, alpha=0.8)

    # Highlight the maximum
    max_idx = peak_years.values.argmax()
    bars[max_idx].set_color('#c0392b')
    bars[max_idx].set_alpha(1.0)

    ax.set_title(f'Top {top_n} Peak Years for Wildfire Occurrence',
                fontsize=VIZ_CONFIG['font_size']['title'], fontweight='bold')
    ax.set_xlabel('Year', fontsize=VIZ_CONFIG['font_size']['label'])
    ax.set_ylabel('Number of Fires', fontsize=VIZ_CONFIG['font_size']['label'])
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    # Add value labels on bars
    for i, (year, count) in enumerate(peak_years.items()):
        ax.text(year, count + 5, str(int(count)),
               ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.tight_layout()

    if save:
        save_figure(fig, 'peak_years_for_fires')

    return fig


def plot_fires_by_decade(df: pd.DataFrame, save: bool = True) -> plt.Figure:
    """
    Plot fire occurrence by decade.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset with Decade column
    save : bool, default True
        If True, saves figure to output directory

    Returns
    -------
    plt.Figure
        Matplotlib figure object
    """
    fires_by_decade = df.groupby('Decade').size()

    fig, ax = plt.subplots(figsize=VIZ_CONFIG['default_figsize'])

    ax.bar(fires_by_decade.index, fires_by_decade.values,
          color='#3498db', edgecolor='black', width=8, alpha=0.8)

    ax.set_title('Wildfire Occurrence by Decade',
                fontsize=VIZ_CONFIG['font_size']['title'], fontweight='bold')
    ax.set_xlabel('Decade', fontsize=VIZ_CONFIG['font_size']['label'])
    ax.set_ylabel('Number of Fires', fontsize=VIZ_CONFIG['font_size']['label'])
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    plt.xticks(rotation=45)
    plt.tight_layout()

    if save:
        save_figure(fig, 'fires_by_decade')

    return fig


def plot_fire_area_by_decade(df: pd.DataFrame, save: bool = True) -> plt.Figure:
    """
    Create heatmap of total fire area burned by decade.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset with Decade and GIS_ACRES columns
    save : bool, default True
        If True, saves figure to output directory

    Returns
    -------
    plt.Figure
        Matplotlib figure object
    """
    fire_area_by_decade = df.groupby('Decade')['GIS_ACRES'].sum().reset_index()

    fig, ax = plt.subplots(figsize=VIZ_CONFIG['default_figsize'])

    sns.heatmap(fire_area_by_decade.set_index('Decade').T,
               annot=True, fmt='.0f', cmap='YlOrRd',
               cbar_kws={'label': 'Total Burned Area (Acres)'},
               linewidths=2, linecolor='white', ax=ax)

    ax.set_title('Total Wildfire Area by Decade',
                fontsize=VIZ_CONFIG['font_size']['title'], fontweight='bold')
    ax.set_xlabel('Decade', fontsize=VIZ_CONFIG['font_size']['label'])
    ax.set_ylabel('', fontsize=VIZ_CONFIG['font_size']['label'])

    plt.tight_layout()

    if save:
        save_figure(fig, 'fire_area_by_decade')

    return fig


def plot_seasonality(df: pd.DataFrame, save: bool = True) -> plt.Figure:
    """
    Plot seasonal patterns in fire occurrence.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset with Month column
    save : bool, default True
        If True, saves figure to output directory

    Returns
    -------
    plt.Figure
        Matplotlib figure object
    """
    fires_by_month = df.groupby('Month').size()

    fig, ax = plt.subplots(figsize=(12, 6))

    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Color code by season
    colors = ['#5DADE2'] * 3 + ['#58D68D'] * 3 + ['#F39C12'] * 3 + ['#AF7AC5'] * 3

    ax.bar(range(1, 13), fires_by_month.values, color=colors,
          edgecolor='black', alpha=0.8)

    ax.set_title('Seasonal Patterns in Wildfire Occurrence',
                fontsize=VIZ_CONFIG['font_size']['title'], fontweight='bold')
    ax.set_xlabel('Month', fontsize=VIZ_CONFIG['font_size']['label'])
    ax.set_ylabel('Number of Fires', fontsize=VIZ_CONFIG['font_size']['label'])
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(month_names)
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    plt.tight_layout()

    if save:
        save_figure(fig, 'seasonality')

    return fig


def plot_cause_distribution(df: pd.DataFrame, top_n: int = 10, save: bool = True) -> plt.Figure:
    """
    Plot distribution of fire causes.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset with CAUSE_DESCRIPTION column
    top_n : int, default 10
        Number of top causes to display
    save : bool, default True
        If True, saves figure to output directory

    Returns
    -------
    plt.Figure
        Matplotlib figure object
    """
    cause_counts = df['CAUSE_DESCRIPTION'].value_counts().head(top_n)

    fig, ax = plt.subplots(figsize=(12, 8))

    ax.barh(range(len(cause_counts)), cause_counts.values,
           color='#16a085', edgecolor='black', alpha=0.8)

    ax.set_yticks(range(len(cause_counts)))
    ax.set_yticklabels(cause_counts.index)
    ax.invert_yaxis()

    ax.set_title(f'Top {top_n} Wildfire Causes',
                fontsize=VIZ_CONFIG['font_size']['title'], fontweight='bold')
    ax.set_xlabel('Number of Fires', fontsize=VIZ_CONFIG['font_size']['label'])
    ax.set_ylabel('Fire Cause', fontsize=VIZ_CONFIG['font_size']['label'])
    ax.grid(axis='x', linestyle='--', alpha=0.3)

    # Add percentage labels
    total = cause_counts.sum()
    for i, (cause, count) in enumerate(cause_counts.items()):
        percentage = count / total * 100
        ax.text(count + 10, i, f'{count} ({percentage:.1f}%)',
               va='center', fontsize=10)

    plt.tight_layout()

    if save:
        save_figure(fig, 'cause_distribution')

    return fig


def plot_containment_effectiveness(method_stats: pd.DataFrame, save: bool = True) -> plt.Figure:
    """
    Plot containment method effectiveness with confidence intervals.

    Parameters
    ----------
    method_stats : pd.DataFrame
        Statistics by containment method (from analyze_containment_methods)
    save : bool, default True
        If True, saves figure to output directory

    Returns
    -------
    plt.Figure
        Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=(12, 8))

    y_pos = range(len(method_stats))

    # Plot bars with error bars
    ax.barh(y_pos, method_stats['Mean_Effectiveness'],
           xerr=[method_stats['Mean_Effectiveness'] - method_stats['CI_Lower'],
                 method_stats['CI_Upper'] - method_stats['Mean_Effectiveness']],
           color='#e74c3c', edgecolor='black', alpha=0.8,
           error_kw={'linewidth': 2, 'ecolor': '#2c3e50'})

    ax.set_yticks(y_pos)
    ax.set_yticklabels(method_stats.index)
    ax.invert_yaxis()

    ax.set_title('Containment Method Effectiveness (with 95% CI)\n⚠️ Note: Metric conflates fire size with response quality',
                fontsize=VIZ_CONFIG['font_size']['title'], fontweight='bold')
    ax.set_xlabel('Effectiveness (Acres/Hour)', fontsize=VIZ_CONFIG['font_size']['label'])
    ax.set_ylabel('Containment Method', fontsize=VIZ_CONFIG['font_size']['label'])
    ax.grid(axis='x', linestyle='--', alpha=0.3)

    # Add sample size annotations
    for i, (method, row) in enumerate(method_stats.iterrows()):
        ax.text(row['Mean_Effectiveness'] + 1, i,
               f"n={int(row['Count'])}",
               va='center', fontsize=9, style='italic')

    plt.tight_layout()

    if save:
        save_figure(fig, 'containment_effectiveness')

    return fig


def plot_fire_size_distribution(df: pd.DataFrame, save: bool = True) -> plt.Figure:
    """
    Plot distribution of fire sizes (log scale).

    Parameters
    ----------
    df : pd.DataFrame
        Dataset with GIS_ACRES column
    save : bool, default True
        If True, saves figure to output directory

    Returns
    -------
    plt.Figure
        Matplotlib figure object
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Histogram on log scale
    ax1.hist(np.log10(df['GIS_ACRES'] + 1), bins=50, color='#9b59b6',
            edgecolor='black', alpha=0.7)
    ax1.set_title('Fire Size Distribution (Log Scale)',
                 fontsize=VIZ_CONFIG['font_size']['title'], fontweight='bold')
    ax1.set_xlabel('Log₁₀(Acres + 1)', fontsize=VIZ_CONFIG['font_size']['label'])
    ax1.set_ylabel('Frequency', fontsize=VIZ_CONFIG['font_size']['label'])
    ax1.grid(axis='y', linestyle='--', alpha=0.3)

    # Box plot
    ax2.boxplot(df['GIS_ACRES'], vert=True, patch_artist=True,
               boxprops=dict(facecolor='#9b59b6', alpha=0.7),
               medianprops=dict(color='red', linewidth=2))
    ax2.set_ylabel('Acres', fontsize=VIZ_CONFIG['font_size']['label'])
    ax2.set_title('Fire Size Box Plot',
                 fontsize=VIZ_CONFIG['font_size']['title'], fontweight='bold')
    ax2.grid(axis='y', linestyle='--', alpha=0.3)
    ax2.set_yscale('log')

    plt.tight_layout()

    if save:
        save_figure(fig, 'fire_size_distribution')

    return fig


def generate_all_visualizations(df: pd.DataFrame, method_stats: Optional[pd.DataFrame] = None) -> None:
    """
    Generate all standard visualizations for the analysis.

    Parameters
    ----------
    df : pd.DataFrame
        Processed wildfire dataset
    method_stats : pd.DataFrame, optional
        Containment method statistics (if available)
    """
    print("\nGenerating visualizations...")

    plot_fires_over_time(df)
    plot_peak_years(df)
    plot_fires_by_decade(df)
    plot_fire_area_by_decade(df)
    plot_seasonality(df)
    plot_fire_size_distribution(df)

    if 'CAUSE_DESCRIPTION' in df.columns:
        plot_cause_distribution(df)

    if method_stats is not None:
        plot_containment_effectiveness(method_stats)

    print(f"\n[OK] All visualizations saved to {OUTPUT_DIR / 'figures'}")