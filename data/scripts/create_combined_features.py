import pandas as pd

# Load each processed dataset
user_df = pd.read_csv('data/processed/uiux_user_interaction_processed.csv')
clay_df = pd.read_csv('data/processed/clay_labels_processed.csv')
ui_df = pd.read_csv('data/processed/webcode2ui_preprocessed.csv')

# Align by row index using the minimum length
min_len = min(len(user_df), len(clay_df), len(ui_df))
user_df = user_df.iloc[:min_len]
clay_df = clay_df.iloc[:min_len]
ui_df = ui_df.iloc[:min_len]

# Concatenate features column-wise
combined_df = pd.concat([user_df, clay_df, ui_df], axis=1)

# Save the combined features for VAE input
combined_df.to_csv('data/processed/vae_combined_features.csv', index=False)
print("Combined features saved to data/processed/vae_combined_features.csv")
