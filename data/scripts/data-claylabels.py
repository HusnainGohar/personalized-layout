import requests
import os

url = "https://raw.githubusercontent.com/clay-ui/clay-dataset/main/clay_labels.csv"  # Replace with actual URL
output_dir = "data/raw"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "clay_labels.csv")

response = requests.get(url)
with open(output_path, "wb") as f:
    f.write(response.content)

print("Downloaded clay_labels.csv to", output_path)
