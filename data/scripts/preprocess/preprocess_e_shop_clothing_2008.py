import pandas as pd
import os
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler

def preprocess_e_shop_clothing_2008(input_path, output_path):
    # Step 1: Load the data
    df = pd.read_csv(input_path)
    print("Loaded data. Columns found:")
    print(df.columns.tolist())
    print(df.head())

    # Step 2: Define possible columns (case and spacing may vary)
    possible_cat_cols = [
        'country',
        'page 1 (main category)', 'Page 1 (main category)',
        'page 2 (clothing model)', 'Page 2 (clothing model)',
        'colour', 'color',
        'location'
    ]
    possible_num_cols = ['price', 'Price']

    # Step 3: Find columns that actually exist in the DataFrame
    cat_cols = [col for col in possible_cat_cols if col in df.columns]
    num_cols = [col for col in possible_num_cols if col in df.columns]

    print("Categorical columns used:", cat_cols)
    print("Numerical columns used:", num_cols)

    # Step 4: Drop rows with missing values in selected columns
    if cat_cols or num_cols:
        df = df.dropna(subset=cat_cols + num_cols)
        print("After dropping missing values:", df.shape)
    else:
        print("No valid columns found for processing. Please check your CSV headers.")
        return

    # Step 5: Encode categorical features
    if cat_cols:
        encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        encoded = encoder.fit_transform(df[cat_cols])
        encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(cat_cols))
    else:
        encoded_df = pd.DataFrame()
        print("No categorical columns found for encoding.")

    # Step 6: Normalize numerical features
    if num_cols:
        scaler = MinMaxScaler()
        normalized = scaler.fit_transform(df[num_cols])
        normalized_df = pd.DataFrame(normalized, columns=num_cols)
    else:
        normalized_df = pd.DataFrame()
        print("No numerical columns found for normalization.")

    # Step 7: Combine all features
    if not encoded_df.empty and not normalized_df.empty:
        processed = pd.concat([encoded_df, normalized_df], axis=1)
    elif not encoded_df.empty:
        processed = encoded_df
    elif not normalized_df.empty:
        processed = normalized_df
    else:
        raise ValueError("No features to process! Please check your column selections.")

    print("Processed data sample:")
    print(processed.head())

    # Step 8: Save the processed data
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    processed.to_csv(output_path, index=False)
    print(f"Preprocessed data saved to {output_path}")

if __name__ == "__main__":
    input_path = "data/raw/e-shop-clothing-2008.csv"
    output_path = "data/processed/e-shop-clothing-2008-processed.csv"
    if not os.path.exists(input_path):
        print(f"ERROR: Input file not found at {input_path}")
    else:
        preprocess_e_shop_clothing_2008(input_path, output_path)
