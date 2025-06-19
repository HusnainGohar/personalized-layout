import torch
import json
from models.vae_model import VAE

# Use the SAME dimensions as training
input_dim = 60      # Must match training dimension
latent_dim = 8      # Must match training dimension
hidden_dim = 64     # Must match training dimension

vae = VAE(input_dim=input_dim, latent_dim=latent_dim, hidden_dim=hidden_dim)
vae.load_state_dict(torch.load('vae_trained.pth'))
vae.eval()

generated_layouts = []
for i in range(10):
    z = torch.randn(1, latent_dim)
    features = vae.decode(z).detach().numpy().tolist()[0]
    generated_layouts.append({"layout_id": i, "features": features})

# Save to React public folder
with open('../frontend/public/generatedLayouts.json', 'w') as f:
    json.dump(generated_layouts, f, indent=2)

print("Layouts generated and saved successfully!")
