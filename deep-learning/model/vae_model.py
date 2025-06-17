import torch
import torch.nn as nn
import torch.nn.functional as F
import pandas as pd
import os

# 1. Define the VAE model
class VAE(nn.Module):
    def __init__(self, input_dim, latent_dim=8, hidden_dim=64):
        super().__init__()
        # Encoder
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc_mu = nn.Linear(hidden_dim, latent_dim)
        self.fc_logvar = nn.Linear(hidden_dim, latent_dim)
        # Decoder
        self.fc2 = nn.Linear(latent_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, input_dim)

    def encode(self, x):
        h = F.relu(self.fc1(x))
        return self.fc_mu(h), self.fc_logvar(h)

    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std

    def decode(self, z):
        h = F.relu(self.fc2(z))
        return torch.sigmoid(self.fc3(h))

    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        recon_x = self.decode(z)
        return recon_x, mu, logvar

if __name__ == "__main__":
    # 2. Load real preprocessed data if available
    csv_path = "data/processed/your_processed_file.csv"  # <-- Update this path!
    batch_size = 4
    latent_dim = 8
    hidden_dim = 64

    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        input_dim = df.shape[1]
        # For demonstration, just take the first batch_size rows
        x_np = df.iloc[:batch_size].values
        x = torch.tensor(x_np, dtype=torch.float32)
        print(f"Loaded real data from {csv_path} with shape {x.shape}")
    else:
        # Fallback: use dummy data if CSV not found
        input_dim = 10
        x = torch.randn(batch_size, input_dim)
        print("CSV not found, using random input.")

    # 3. Instantiate and run the VAE
    vae = VAE(input_dim=input_dim, latent_dim=latent_dim, hidden_dim=hidden_dim)
    recon_x, mu, logvar = vae(x)

    # 4. Print the outputs
    print("Reconstructed Output (recon_x):")
    print(recon_x)
    print("\nLatent Mean (mu):")
    print(mu)
    print("\nLatent Log-Variance (logvar):")
    print(logvar)
    print("\nShapes:")
    print("recon_x:", recon_x.shape)
    print("mu:", mu.shape)
    print("logvar:", logvar.shape)
