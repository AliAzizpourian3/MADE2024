# Project Plan

## **Title**
Educational Attainment and Income Correlation in the United States

---

## **Main Question**
How does the level of educational attainment influence income levels across different states and cities in the United States?

---

## **Description**
This project explores the potential relationship between education levels and income distribution across the U.S. By analyzing educational attainment data and income data, the goal is to identify patterns and trends that explain how education impacts income levels across states and cities. This analysis aims to provide insights into socioeconomic disparities and how they vary regionally.

---

## **Datasources**

### **Datasource 1**: S1501 | Educational Attainment
- **Metadata URL**: [Census S1501 Educational Attainment](https://data.census.gov/table?q=S1501)
- **Data URL**: Provided CSV file
- **Data Type**: CSV  
- **Description**: This dataset contains detailed data on educational attainment levels (e.g., bachelor's degree, graduate degree, less than high school) for cities and states in the United States.

### **Datasource 2**: S1901 | Income in the Past 12 Months (2022 Inflation-Adjusted Dollars)
- **Metadata URL**: [Census S1901 Income Data](https://data.census.gov/table?q=S1901)
- **Data URL**: Provided CSV file
- **Data Type**: CSV  
- **Description**: This dataset contains data on income levels by brackets (e.g., median household income, income distribution) for cities and states in the United States.

---

## **Work Packages**

### **Data Acquisition and Exploration**
- Load the educational attainment and income datasets from provided CSV files.
- Inspect the structure, data types, and attributes of each dataset.
- Document the format, location fields, and key variables for integration.

---

### **Data Cleaning and Preprocessing**
- Standardize the datasets for alignment (e.g., consistent city/state fields).
- Convert textual or mixed data types (e.g., income and education levels) to numeric values where necessary.
- Remove missing or invalid values.

---

### **Data Integration**
- Merge the educational attainment and income datasets by city and state.
- Ensure location identifiers align correctly for meaningful correlation analysis.

---

### **Exploratory Data Analysis (EDA)**
- Visualize the distribution of income levels across different educational attainment brackets.
- Identify trends and patterns between education levels and median income across states and cities.
- Highlight cities or states with outliers in educational attainment or income.

---

### **Statistical Analysis**
- Compute correlation coefficients between education and income metrics.
- Evaluate regional disparities in the relationship between education and income.

---

### **Report Generation**
- Create a report summarizing findings, including:
  - Correlations between education and income.
  - Regional disparities and trends.
  - Visualizations (e.g., scatter plots, bar charts).
- Provide insights into socioeconomic inequality and its relation to education.
