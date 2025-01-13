import os
import pandas as pd
import sqlite3
from kaggle import KaggleApi

# Define directories
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Instantiate Kaggle API
api = KaggleApi()
api.authenticate()

# Download datasets
datasets = {
    "us_economic": "alfredkondoro/u-s-economic-indicators-1974-2024",
    "us_debt": "thedevastator/u-s-public-debt-vs-gdp-from-1947-2020"
}

# Download and extract datasets
for name, dataset in datasets.items():
    print(f"Downloading {name}...")
    api.dataset_download_files(dataset, path=DATA_DIR, unzip=True)

# Load datasets
cpi_data = pd.read_csv(f"{DATA_DIR}/cpi_data.csv")
gdp_data = pd.read_csv(f"{DATA_DIR}/gdp_data.csv")
unemployment_data = pd.read_csv(f"{DATA_DIR}/unemployment_data.csv")
us_gdp_debt = pd.read_csv(f"{DATA_DIR}/US GDP vs Debt.csv")

# Rename columns for consistency
cpi_data.columns = ["DATE", "CPIAUCSL"]
gdp_data.columns = ["DATE", "GDP"]
unemployment_data.columns = ["DATE", "UNRATE"]
us_gdp_debt.columns = ["index", "Quarter", "Gross Domestic Product ($mil)", "Total Public Debt ($mil)"]

# Convert date columns to datetime
cpi_data['DATE'] = pd.to_datetime(cpi_data['DATE'])
gdp_data['DATE'] = pd.to_datetime(gdp_data['DATE'])
unemployment_data['DATE'] = pd.to_datetime(unemployment_data['DATE'])
us_gdp_debt['Quarter'] = pd.to_datetime(us_gdp_debt['Quarter'])

# Convert monthly data to quarterly
cpi_data['Quarter'] = cpi_data['DATE'].dt.to_period('Q')
cpi_quarterly = cpi_data.groupby('Quarter')['CPIAUCSL'].mean().reset_index()

gdp_data['Quarter'] = gdp_data['DATE'].dt.to_period('Q')
gdp_quarterly = gdp_data.groupby('Quarter')['GDP'].mean().reset_index()

unemployment_data['Quarter'] = unemployment_data['DATE'].dt.to_period('Q')
unemployment_quarterly = unemployment_data.groupby('Quarter')['UNRATE'].mean().reset_index()

# Merge CPI, GDP, and Unemployment datasets
merged_quarterly = cpi_quarterly.merge(unemployment_quarterly, on='Quarter', how='inner')
merged_quarterly = merged_quarterly.merge(gdp_quarterly, on='Quarter', how='inner')

# Prepare Public Debt data
us_gdp_debt.rename(columns={
    'Gross Domestic Product ($mil)': 'GDP_MIL',
    'Total Public Debt ($mil)': 'DEBT_MIL'
}, inplace=True)
us_gdp_debt['Quarter'] = us_gdp_debt['Quarter'].dt.to_period('Q')

# Merge all datasets
final_data = merged_quarterly.merge(us_gdp_debt, on='Quarter', how='inner')
final_data = final_data[final_data['Quarter'] != '2020Q3']

# Normalize numerical columns
columns_to_normalize = ['CPIAUCSL', 'UNRATE', 'GDP_MIL', 'DEBT_MIL']
for col in columns_to_normalize:
    final_data[col] = (final_data[col] - final_data[col].min()) / (final_data[col].max() - final_data[col].min())

# Save merged and normalized dataset to SQLite database
conn = sqlite3.connect(f"{DATA_DIR}/final_dataset.sqlite")
final_data.to_sql("final_combined_quarterly_data", conn, if_exists="replace", index=False)
conn.close()

print("Pipeline completed successfully. Final dataset saved to SQLite.")
