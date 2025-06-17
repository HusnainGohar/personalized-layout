import pandas as pd
import os
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler

def preprocess_uiux_user_interaction(input_path, output_path):
    # Step 1: Load the data
    df = pd.read_csv(input_path)
    print("Loaded data. Columns found:")
    print(df.columns.tolist())
    print(df.head())

    # Step 2: Drop rows with missing values (or use fillna if preferred)
    df = df.dropna()
    print("After dropping missing values:", df.shape)

    # Step 3: Encode categorical features
    cat_cols = ['Gender', 'Platform', 'User_experience']
    cat_cols = [col for col in cat_cols if col in df.columns]  # Only keep columns that exist

    if cat_cols:
        encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        encoded = encoder.fit_transform(df[cat_cols])
        encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(cat_cols))
    else:
        encoded_df = pd.DataFrame()
        print("No categorical columns found for encoding.")

    # Step 4: Normalize numerical features
    # List the expected numerical columns, but only use those that exist in the DataFrame
    num_cols = [
        'Age', 'Color Scheme', 'Visual Hierarchy', 'Typography', 'Images and Multimedia',
        'Layout', 'Mobile Responsiveness', 'CTA (Call to Action) Buttons',
        'Forms and Input Fields', 'Feedback/Error Messages', 'Loading Speed',
        'Personalization', 'Accessibility'
    ]
    num_cols = [col for col in num_cols if col in df.columns]

    if num_cols:
        scaler = MinMaxScaler()
        normalized = scaler.fit_transform(df[num_cols])
        normalized_df = pd.DataFrame(normalized, columns=num_cols)
    else:
        normalized_df = pd.DataFrame()
        print("No numerical columns found for normalization.")

    # Step 5: Combine all features
    if not encoded_df.empty and not normalized_df.empty:
        processed = pd.concat([encoded_df, normalized_df], axis=1)
    elif not encoded_df.empty:
        processed = encoded_df
    elif not normalized_df.empty:
        processed = normalized_df
    else:
        raise ValueError("No features to process!")

    print("Processed data sample:")
    print(processed.head())

    # Step 6: Save the processed data
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    processed.to_csv(output_path, index=False)
    print(f"Preprocessed data saved to {output_path}")

if __name__ == "__main__":
    input_path = "data/raw/uiux_user_interaction.csv"
    output_path = "data/processed/uiux_user_interaction_processed.csv"
    if not os.path.exists(input_path):
        print(f"ERROR: Input file not found at {input_path}")
    else:
        preprocess_uiux_user_interaction(input_path, output_path)
