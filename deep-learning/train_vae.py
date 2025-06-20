import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import pandas as pd
from torch.utils.data import DataLoader, TensorDataset
import os
import json

from models.vae_model import VAE

# Get current script directory (robust method)
script_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()

# CORRECTED DATA PATH: Go up one level to project root
project_root = os.path.dirname(script_dir)
data_path = os.path.join(project_root, 'data', 'processed', 'vae_combined_features.csv')
print(f"Looking for data at: {data_path}")

# Data loading with error handling
try:
    df = pd.read_csv(data_path)
    print("✅ CSV file loaded successfully!")
except FileNotFoundError:
    print(f"❌ Error: File not found at {data_path}")
    # Add fallback or exit logic here
    exit(1)

x = torch.tensor(df.values, dtype=torch.float32)
batch_size = 32
dataset = TensorDataset(x)
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
input_dim = x.shape[1]  # Use [1] to get feature dimension

# Model setup
vae = VAE(input_dim=input_dim, latent_dim=8, hidden_dim=64)
optimizer = optim.Adam(vae.parameters(), lr=1e-3)
epochs = 50

# Loss function
def vae_loss(recon_x, x, mu, logvar):
    recon_loss = F.mse_loss(recon_x, x, reduction='sum')
    kl_div = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
    return recon_loss + kl_div

# Training loop with loss tracking
training_losses = []  # Store average loss per epoch

vae.train()
for epoch in range(epochs):
    total_loss = 0
    for batch in dataloader:
        x_batch = batch[0]  # Correct batch unpacking
        optimizer.zero_grad()
        recon_x, mu, logvar = vae(x_batch)
        loss = vae_loss(recon_x, x_batch, mu, logvar)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    
    avg_loss = total_loss / len(dataset)
    training_losses.append(avg_loss)
    print(f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.4f}")

# Save the trained model with robust path handling
model_save_path = os.path.join(script_dir, 'models', 'vae_trained.pth')  # Simplified path
os.makedirs(os.path.dirname(model_save_path), exist_ok=True)  # Create directories if missing
torch.save(vae.state_dict(), model_save_path)

print(f'Model saved at: {model_save_path}')

# Save training losses for analysis
losses_save_path = os.path.join(script_dir, 'training_losses.json')
with open(losses_save_path, 'w') as f:
    json.dump(training_losses, f)
print(f'Training losses saved at: {losses_save_path}')

# Verify model file exists
if os.path.exists(model_save_path):
    print("✅ Model file created successfully!")
else:
    print("❌ Error: Model file not created!")
