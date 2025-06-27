# import torch
# import json
# from models.vae_model import VAE

# # Use the SAME dimensions as training
# input_dim = 60      # Must match training dimension
# latent_dim = 8      # Must match training dimension
# hidden_dim = 64     # Must match training dimension

# vae = VAE(input_dim=input_dim, latent_dim=latent_dim, hidden_dim=hidden_dim)
# vae.load_state_dict(torch.load('vae_trained.pth'))
# vae.eval()

# generated_layouts = []
# for i in range(10):
#     z = torch.randn(1, latent_dim)
#     features = vae.decode(z).detach().numpy().tolist()[0]
#     generated_layouts.append({"layout_id": i, "features": features})

# # Save to React public folder
# with open('../frontend/public/generatedLayouts.json', 'w') as f:
#     json.dump(generated_layouts, f, indent=2)

# print("Layouts generated and saved successfully!")
import torch
import json
import os
import sys
import pandas as pd
from models.vae_model import VAE  # Adjust import if needed

# Paths
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, "models", "vae_trained.pth")
print(f"[DEBUG] Model will be loaded from: {os.path.abspath(model_path)}")
output_path = os.path.abspath(os.path.join(script_dir, '..', 'frontend', 'public', 'generatedLayouts.json'))

# Model parameters (must match training)
input_dim = 68      # Must match the number of columns in vae_combined_features.csv
latent_dim = 8
hidden_dim = 64

# Load VAE model
vae = VAE(input_dim=input_dim, latent_dim=latent_dim, hidden_dim=hidden_dim)
vae.load_state_dict(torch.load(model_path))
vae.eval()

# Load user feature vectors
features_path = os.path.join(script_dir, '..', 'data', 'processed', 'vae_combined_features.csv')
features_df = pd.read_csv(features_path)

# Select feature vector
user_index = None
if len(sys.argv) > 1:
    try:
        user_index = int(sys.argv[1])
        feature_vector = features_df.iloc[user_index].values.tolist()
        print(f"[INFO] Using feature vector for user index {user_index}")
    except Exception as e:
        print(f"[WARN] Invalid user index argument: {e}. Picking random user.")
        feature_vector = features_df.sample(1).iloc[0].values.tolist()
        print(f"[INFO] Using feature vector for random user")
else:
    feature_vector = features_df.sample(1).iloc[0].values.tolist()
    print(f"[INFO] Using feature vector for random user")

feature_tensor = torch.tensor([feature_vector], dtype=torch.float32)
# Encode to latent space
with torch.no_grad():
    mu, logvar = vae.encode(feature_tensor)
    z = mu  # Use mean for deterministic output

# Decode to layout features
features = vae.decode(z).detach().numpy().tolist()[0]

print("[DEBUG] Decoded features:", features)

# Map features to card layout structure
card_names = ["analytics-card", "profile-card", "notifications-card"]
layout = []
for i, name in enumerate(card_names):
    layout.append({
        "component": name,
        "visible": features[i] > 0,
        "order": -features[i]  # negative for descending sort in frontend
    })
# Sort by feature value descending
layout = sorted(layout, key=lambda x: x["order"])

# Save to JSON for frontend
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w') as f:
    json.dump(layout, f, indent=2)

print(f"Layout generated and saved to {output_path}")
