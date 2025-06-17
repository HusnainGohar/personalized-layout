import requests
import os
import pandas as pd

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
output_dir = "data/raw"
os.makedirs(output_dir, exist_ok=True)
excel_path = os.path.join(output_dir, "e-shop-clothing-2008.xlsx")
csv_path = os.path.join(output_dir, "e-shop-clothing-2008.csv")
df = pd.read_csv(csv_path)
print(df.head())
# Download the Excel file if it doesn't exist
if not os.path.exists(excel_path):
    response = requests.get(url)
    with open(excel_path, "wb") as f:
        f.write(response.content)
    print("Downloaded Excel file to", excel_path)
else:
    print("Excel file already exists at", excel_path)

# Convert Excel to CSV
try:
    df = pd.read_excel(excel_path)
    df.to_csv(csv_path, index=False)
    print("Converted Excel to CSV at", csv_path)
except Exception as e:
    print("Error during conversion:", e)

# Remove the Excel file after conversion
if os.path.exists(excel_path):
    os.remove(excel_path)
    print("Removed Excel file from raw directory.")
 