import os
import json
from datasets import load_dataset
from itertools import islice

# Load the dataset in streaming mode
dataset = load_dataset("xcodemind/webcode2m", split="train", streaming=True)

# Grab just 10 examples
samples = list(islice(dataset, 200))

# Prepare output directory
output_dir = "F:/personalized-layouts/data/raw"
os.makedirs(output_dir, exist_ok=True)

# Save samples to JSONL file (no data modification)
output_path = os.path.join(output_dir, "webcode2m_samples.jsonl")
with open(output_path, 'w', encoding='utf-8') as f:
    for sample in samples:
        json.dump(sample, f, default=str)  # default=str handles non-serializable fields gracefully
        f.write('\n')

print(f"Saved 10 samples to {len(output_path)}")
# print("First sample:", samples[0])
