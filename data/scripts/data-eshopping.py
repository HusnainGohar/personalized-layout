import requests
import os

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
output_dir = "data/raw"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "e-shop-clothing-2008.xlsx")

response = requests.get(url)
with open(output_path, "wb") as f:
    f.write(response.content)

print("Downloaded E-Shop Clothing 2008 dataset to", output_path)
