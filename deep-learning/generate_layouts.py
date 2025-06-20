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
from models.vae_model import VAE  # Adjust import if needed

# Paths
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, "models", "vae_trained.pth")
output_path = os.path.join(script_dir, "..", "..", "frontend", "public", "generatedLayouts.json")

# Model parameters (must match training)
input_dim = 60      # Set this to your actual input_dim
latent_dim = 8
hidden_dim = 64

# Load VAE model
vae = VAE(input_dim=input_dim, latent_dim=latent_dim, hidden_dim=hidden_dim)
vae.load_state_dict(torch.load(model_path))
vae.eval()

# Generate a single adaptive card layout
z = torch.randn(1, latent_dim)
features = vae.decode(z).detach().numpy().tolist()[0]

# Prepare output
layout = [{"layout_id": 0, "features": features}]

# Save to JSON for frontend
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w') as f:
    json.dump(layout, f, indent=2)

print(f"✅ Layout generated and saved to {output_path}")
