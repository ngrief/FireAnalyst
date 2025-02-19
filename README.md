# 🔥 Fire Analysis Project

## Overview  
This project analyzes **California fire perimeter data** to derive insights into fire trends, containment effectiveness, and spatial patterns. The dataset contains historical fire data from **1878 to 2023**, including attributes such as containment methods, causes, geographic extent, and durations.

---

## 📊 Features  

### 🛠 Data Cleaning  
- Removes rows with missing essential values (**YEAR_**, **GIS_ACRES**).  
- Converts date columns (**ALARM_DATE**, **CONT_DATE**) to a standard datetime format.  
- Fills missing categorical data (**AGENCY**, **UNIT_ID**, **FIRE_NAME**) with placeholders.  
- Drops columns with excessive missing data or limited analytical utility.  

### 🔎 Key Analyses  

#### **🔥 Containment Effectiveness**  
- Measures fire containment effectiveness using the formula:

  Effectiveness = GIS_ACRES / Containment Duration(hours)
    
- Ranks containment methods based on average effectiveness.  

#### **📈 Temporal Trends**  
- Visualizes fire counts over time.  
- Highlights peak years for fire occurrences.  
- Examines trends by decade.  

#### **🌎 Spatial Analysis**  
- Generates a **heatmap** of total fire area burned by decade.  

#### **⚠️ Cause Analysis**  
- Analyzes and summarizes fire causes (if available in the dataset).  

---

## 📊 Visualizations  

- **📈 Number of Fires Over Time** – Line plot showing trends in fire counts.  
- **🔥 Peak Years for Fires** – Bar chart highlighting the most severe fire years.  
- **📊 Fires by Decade** – Bar chart of fire occurrences grouped by decade.  
- **🌎 Total Fire Area by Decade** – Heatmap depicting the acreage burned per decade.  

---

## 🛠 Requirements  

- **Python 3.8+**  
- **Libraries:**  
  - `pandas`  
  - `matplotlib`  
  - `seaborn`  

---

## 🚀 Usage  

1. Place the dataset in the `Resources` folder with the filename:  
California_Fire_Perimeters_(all).csv

markdown
Copy
Edit
2. Run the script to:  
- Clean the dataset.  
- Perform analyses.  
- Generate and save visualizations.  

### 🏃‍♂️ How to Run  

```bash
# Install required libraries
pip install pandas matplotlib seaborn

# Run the script
python FireStarter.py
📂 Output
📌 Console Output

Displays key metrics and analysis results (e.g., containment effectiveness, fire causes).
📌 Generated Visualizations (saved in the Resources folder):

fires_over_time.png
peak_years_for_fires.png
fires_by_decade.png
fire_area_by_decade.png
