# Fire Analysis Project

This project analyzes California fire perimeter data to derive insights into fire trends, containment effectiveness, and spatial patterns. The dataset contains historical data from 1878 to 2023 and includes fire attributes like containment methods, causes, geographic extent, and durations.

## Features

### Data Cleaning
- Drops rows with missing essential values (`YEAR_`, `GIS_ACRES`).
- Converts date columns (`ALARM_DATE`, `CONT_DATE`) to a standard datetime format.
- Fills missing categorical data (`AGENCY`, `UNIT_ID`, `FIRE_NAME`) with placeholders.
- Removes columns with excessive missing data or limited analytical utility.

### Key Analyses
1. **Containment Effectiveness**:
   - Calculates fire containment effectiveness using the formula:
     
     \[ \text{Effectiveness} = \frac{\text{GIS_ACRES}}{\text{Containment Duration (hours)}} \]
   - Ranks containment methods based on average effectiveness.

2. **Temporal Trends**:
   - Visualizes fire counts over time.
   - Highlights peak years for fire occurrences.
   - Examines trends by decade.

3. **Spatial Analysis**:
   - Generates a heatmap of total fire area burned by decade.
   - Plots fire locations on a map of California (requires latitude and longitude data).

4. **Cause Analysis**:
   - Analyzes and summarizes fire causes (if present in the dataset).

## Visualizations
- **Number of Fires Over Time**: Line plot showing trends in fire counts.
- **Peak Years for Fires**: Bar chart highlighting top fire years.
- **Fires by Decade**: Bar chart of fire occurrences grouped by historical decades.
- **Total Fire Area by Decade**: Heatmap depicting the acreage burned per decade.

## Requirements
- Python 3.8+
- Libraries:
  - `pandas`
  - `matplotlib`
  - `seaborn`
  - `folium`

## Usage
1. Place the dataset in the `Resources` folder with the filename `California_Fire_Perimeters_(all).csv`.
2. Run the script to:
   - Clean the dataset.
   - Perform analyses.
   - Generate visualizations and geographic heatmaps.


## How to Run
```bash
# Install required libraries
pip install pandas matplotlib seaborn folium

# Run the script
python FireStarter.py
```

## Output
- **Console**: Displays key metrics and analysis results (e.g., containment effectiveness, cause data).
- **Visualizations**: Automatically generated and displayed.
- **Interactive Map**: Saved as `California_Fire_Heatmap.html`.

## Notes
- Effectiveness is calculated as how quickly acreage was contained relative to fire size.
- Latitude and longitude columns are required for spatial heatmaps.

---

### Future Improvements
- Add metadata for `CAUSE` and `C_METHOD` codes.
- Integrate additional datasets (e.g., weather or vegetation).
- Enhance visualizations with advanced GIS tools.

---

**Author**: Nathaniel Trief  
**Year**: 2025
