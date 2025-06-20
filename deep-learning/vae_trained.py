import torch
import pandas as pd
from models.vae_model import VAE  # Adjust the import if your structure is different

# Load your combined features CSV
df = pd.read_csv('data/processed/vae_combined_features.csv')
input_dim = df.shape[1]

# Load the trained VAE model
vae = VAE(input_dim=input_dim, latent_dim=8, hidden_dim=64)
vae.load_state_dict(torch.load('model\vae_trained.pth'))
vae.eval()  # Set to evaluation mode

# Prepare a batch of data for inference
x = torch.tensor(df.values, dtype=torch.float32)

# Reconstruct the first 5 samples
with torch.no_grad():
    recon_x, mu, logvar = vae(x[:5])
    print("Original Samples:\n", x[:5])
    print("Reconstructed Samples:\n", recon_x)
    print("Latent Means:\n", mu)
    print("Latent Logvars:\n", logvar)

# Example: Generate new samples from random latent vectors
with torch.no_grad():
    z = torch.randn(5, 8)  # 5 samples, latent_dim=8
    generated = vae.decode(z)
    print("Generated Samples from Random Latent Vectors:\n", generated)
