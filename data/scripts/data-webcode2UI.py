import json
from datasets import load_dataset
from itertools import islice
import os

dataset = load_dataset("xcodemind/webcode2m", split="train", streaming=True)
samples = list(islice(dataset, 200))

def make_json_serializable(obj):
    # Remove or convert any non-serializable fields (like PIL images)
    if isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items() if not str(type(v)).startswith("<class 'PIL.")}
    elif isinstance(obj, list):
        return [make_json_serializable(i) for i in obj]
    else:
        return obj

clean_samples = [make_json_serializable(sample) for sample in samples]

os.makedirs("data/raw", exist_ok=True)
with open("data/raw/webcode2m_samples.json", "w", encoding="utf-8") as f:
    json.dump(clean_samples, f, ensure_ascii=False, indent=2)
