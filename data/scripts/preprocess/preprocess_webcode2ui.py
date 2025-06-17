import pandas as pd
import json
import os
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler

def flatten_ui_element(element):
    """
    Flatten a UI element dictionary into a flat record.
    Adjust the keys if your JSON schema is different.
    """
    return {
        'type': element.get('type', 'unknown'),
        'color': element.get('color', 'none'),
        'x': element.get('position', {}).get('x', 0),
        'y': element.get('position', {}).get('y', 0),
        'width': element.get('size', {}).get('width', 0),
        'height': element.get('size', {}).get('height', 0)
    }

def load_and_flatten_json(json_path):
    """
    Load a JSON file containing a list of UI layouts.
    Each layout may have an 'elements' list to flatten.
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    flat_data = []
    for record in data:
        if 'elements' in record:
            for el in record['elements']:
                flat_data.append(flatten_ui_element(el))
        else:
            flat_data.append(flatten_ui_element(record))
    return pd.DataFrame(flat_data)

def preprocess_and_save(input_path, output_path):
    """
    Preprocess the UI data: flatten, encode categoricals, normalize numericals,
    and save as a CSV for model training.
    """
    # Step 1: Load and flatten
    df = load_and_flatten_json(input_path)
    print("Loaded and flattened data. Sample:")
    print(df.head())

    # Step 2: One-hot encode categorical features
    cat_cols = ['type', 'color']
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    encoded = encoder.fit_transform(df[cat_cols])
    encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(cat_cols))

    # Step 3: Normalize numerical features
    num_cols = ['x', 'y', 'width', 'height']
    scaler = MinMaxScaler()
    normalized = scaler.fit_transform(df[num_cols])
    normalized_df = pd.DataFrame(normalized, columns=num_cols)

    # Step 4: Combine all features
    processed = pd.concat([encoded_df, normalized_df], axis=1)
    print("Processed data sample:")
    print(processed.head())

    # Step 5: Save as CSV
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    processed.to_csv(output_path, index=False)
    print(f"Preprocessed data saved to {output_path}")

if __name__ == "__main__":
    # Adjust these paths as needed
    input_path = "data/raw/webcode2m_samples.json"
    output_path = "data/processed/webcode2ui_preprocessed.csv"
    if not os.path.exists(input_path):
        print(f"ERROR: Input file not found at {input_path}")
    else:
        preprocess_and_save(input_path, output_path)
