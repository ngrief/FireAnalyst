# 🔥 FireAnalyst - California Wildfire Analysis

**Professional research toolkit for analyzing 145 years of California wildfire data (1878-2023)**

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 📊 Project Overview

FireAnalyst is a comprehensive statistical analysis platform for California wildfire data, featuring:

- ✅ **Rigorous data validation** with automated quality checks
- 📈 **Statistical analysis** with hypothesis testing and confidence intervals
- 📊 **Publication-quality visualizations**
- 🔬 **Reproducible research** with full documentation
- 📝 **LaTeX methodology** for academic rigor

### Key Features

- **145+ years** of historical fire data analysis
- **9,610+ validated** fire records
- **8 containment methods** analyzed with ANOVA testing
- **19 fire causes** categorized and examined
- **Temporal, seasonal, and spatial** pattern analysis

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone git@github.com:ngrief/FireAnalyst.git
cd FireAnalyst

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

#### Option 1: Use the Analysis Notebook (Recommended)

```bash
jupyter notebook analysis.ipynb
```

The notebook provides a complete, interactive analysis workflow.

#### Option 2: Use Python Scripts

```python
from src.data_processing import full_pipeline
from src.analysis import generate_analysis_report
from src.visualization import generate_all_visualizations

# Run complete pipeline
df, validation_stats = full_pipeline()

# Generate analysis report
report = generate_analysis_report(df)

# Create all visualizations
generate_all_visualizations(df)
```

---

## 📁 Project Structure

```
FireAnalyst/
├── src/                          # Source code modules
│   ├── __init__.py              # Package initialization
│   ├── config.py                # Configuration & parameters
│   ├── data_processing.py       # Data cleaning & validation
│   ├── analysis.py              # Statistical methods
│   └── visualization.py         # Plotting functions
│
├── docs/                         # Documentation
│   └── latex/
│       └── methodology.tex      # Academic methodology (LaTeX)
│
├── Resources/                    # Data directory
│   ├── California_Fire_Perimeters_(all).csv  # Raw data
│   └── cleaned_fire_data.csv    # Processed data (generated)
│
├── output/                       # Analysis outputs (generated)
│   ├── figures/                 # PNG visualizations
│   └── tables/                  # CSV summary tables
│
├── analysis.ipynb               # Main analysis notebook ⭐
├── FirePerimeter.ipynb          # Original exploratory notebook
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

---

## 📈 Analysis Workflow

### 1. Data Processing Pipeline

```python
from src.data_processing import full_pipeline

# Automated pipeline with validation
df, stats = full_pipeline(verbose=True)
```

**Pipeline stages:**
1. Load raw data
2. Clean missing values
3. Validate data quality (6 validation checks)
4. Add derived features
5. Save cleaned data

### 2. Statistical Analysis

```python
from src.analysis import (
    temporal_trend_analysis,
    seasonal_analysis,
    cause_analysis,
    analyze_containment_methods
)

# Temporal trends with linear regression
yearly_stats, trend_test = temporal_trend_analysis(df)
print(trend_test.interpretation)

# Seasonal patterns with chi-square test
monthly_stats, seasonal_test = seasonal_analysis(df)

# Containment methods with ANOVA
method_stats, anova = analyze_containment_methods(df)
```

### 3. Visualization

```python
from src.visualization import (
    plot_fires_over_time,
    plot_seasonality,
    plot_cause_distribution,
    generate_all_visualizations
)

# Generate all standard plots
generate_all_visualizations(df)

# Or create individual plots
fig = plot_fires_over_time(df, save=True)
```

---

## 📊 Key Findings

### Data Quality
- **Initial records**: 22,261
- **Validated records**: 9,610 (43.3% retention)
- **Validation issues**: Date logic errors, extreme durations

### Temporal Trends
- Year range: 1912-2023 (111 years)
- Total acres burned: 10+ million
- Median fire size: 53.1 acres
- 95th percentile: 1,032+ acres

### Seasonal Patterns
- Peak months: July-October
- Chi-square test: p < 0.001 (significant seasonality)

### Fire Causes
- Top cause: Lightning (36.7%)
- Human factors: 63.3% of all fires
- Arson: 7.3% of incidents

### Containment Methods
- 8 methods analyzed
- ANOVA: F-statistic significant (p < 0.01)
- ⚠️ **Metric limitation**: Current effectiveness measure conflates fire size with response quality

---

## ⚠️ Methodological Notes

### Current Limitations

1. **Effectiveness Metric Flaw**
   - Current: `Effectiveness = Acres / Hours`
   - Problem: Larger fires naturally take longer
   - Solution: Control for initial fire size, weather, terrain

2. **Missing Variables**
   - No weather data (wind, humidity, temperature)
   - No vegetation/fuel load information
   - No population density controls

3. **Selection Bias**
   - Historical reporting standards changed
   - Large fires may be over-represented
   - Method deployment not random

### Recommendations

See `docs/latex/methodology.tex` for:
- Proposed improved metrics
- Statistical test details
- Sensitivity analysis plans
- Future research directions

---

## 📚 Documentation

### Academic Documentation
- **Methodology**: `docs/latex/methodology.tex` (compile with `pdflatex`)
- **Data Dictionary**: Appendix A in methodology.tex
- **Statistical Tests**: Appendix B in methodology.tex

### Code Documentation
- All functions include comprehensive docstrings
- Type hints for parameters and returns
- Usage examples in docstrings

```python
from src.data_processing import validate_fire_data
help(validate_fire_data)  # View documentation
```

---

## 🔧 Configuration

Edit `src/config.py` to customize:

```python
# Validation parameters
VALIDATION_CONFIG = {
    "max_containment_hours": 8760,
    "outlier_iqr_multiplier": 3.0,
}

# Visualization settings
VIZ_CONFIG = {
    "figure_dpi": 300,
    "default_figsize": (14, 8),
}

# Statistical settings
STATS_CONFIG = {
    "confidence_level": 0.95,
    "significance_threshold": 0.05,
}
```

---

## 📊 Output Files

### Figures (saved to `output/figures/`)
- `fires_over_time.png` - Temporal trends with trend line
- `peak_years_for_fires.png` - Top 10 peak years
- `fires_by_decade.png` - Decadal comparison
- `fire_area_by_decade.png` - Heatmap of burned area
- `seasonality.png` - Monthly fire patterns
- `cause_distribution.png` - Top fire causes
- `containment_effectiveness.png` - Method comparison with CI
- `fire_size_distribution.png` - Size distribution analysis

### Tables (saved to `output/tables/`)
Generated programmatically from analysis functions.

---

## 🧪 Testing

Run basic tests:

```bash
# Test data processing
python -c "from src.data_processing import full_pipeline; full_pipeline()"

# Test analysis
python -c "from src.analysis import summary_statistics; from src.data_processing import full_pipeline; df, _ = full_pipeline(verbose=False); print(summary_statistics(df))"
```

---

## 📖 Citation

If you use this work in research, please cite:

```bibtex
@software{fireanalyst2025,
  title = {FireAnalyst: California Wildfire Analysis Toolkit},
  author = {FireAnalyst Research Team},
  year = {2025},
  url = {https://github.com/ngrief/FireAnalyst}
}
```

---

## 🤝 Contributing

Contributions welcome! Priority areas:
1. Improved effectiveness metrics (control for fire size)
2. Weather data integration
3. Spatial analysis with GIS
4. Predictive modeling
5. Sensitivity analyses

---

## 📝 License

MIT License - see LICENSE file for details

---

## 🔗 Links

- **Repository**: https://github.com/ngrief/FireAnalyst
- **Issues**: https://github.com/ngrief/FireAnalyst/issues
- **Documentation**: See `docs/` directory

---

## ✨ Acknowledgments

- Data source: California Department of Forestry and Fire Protection (CAL FIRE)
- Analysis tools: pandas, scipy, matplotlib, seaborn
- Inspiration: Need for evidence-based wildfire policy

---

**Last Updated**: 2025
**Version**: 2.0.0 (Professional Research Edition)

For questions or collaboration: Open an issue on GitHub