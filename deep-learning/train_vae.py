import pandas as pd
import torch
from torch.utils.data import DataLoader, TensorDataset

# Load the combined features CSV
df = pd.read_csv('data/processed/vae_combined_features.csv')
x = torch.tensor(df.values, dtype=torch.float32)
batch_size = 32
dataset = TensorDataset(x)
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
input_dim = x.shape[1]
