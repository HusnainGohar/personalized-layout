import torch
import json
import os
import random
from models.vae_model import VAE

# Resolve project root and paths
project_root = os.getcwd()
data_dir = os.path.join(project_root, 'deep-learning', 'data')
data_path = os.path.join(data_dir, 'dummyUserEvents.json')

# Ensure data directory exists
os.makedirs(data_dir, exist_ok=True)

# Generate dummy events if missing
if not os.path.exists(data_path):
    print("⚠️ dummyUserEvents.json not found. Generating sample data...")
    event_types = ['click', 'scroll', 'hover', 'input']
    sections = ['card', 'main', 'button', 'sidebar', 'footer']
    actions = ['like', 'view', 'buy', 'share', 'dismiss']
    
    dummy_events = [
        {
            "event": random.choice(event_types),
            "section": random.choice(sections),
            "timestamp": 1718880000000 + i*1000,
            "action": random.choice(actions)  # Ensure action is always included
        }
        for i in range(10)
    ]
    
    with open(data_path, 'w') as f:
        json.dump(dummy_events, f, indent=2)
    print(f"✅ Generated sample data at {data_path}")

# Load dummy events
with open(data_path, 'r') as f:
    dummy_events = json.load(f)

# Map actions to latent vectors
action_to_vector = {
    "like":    [0.8, -0.2, 0.5, 0.1, -0.3, 0.4, 0.0, 0.2],
    "view":    [-0.5, 1.2, 0.1, -0.4, 0.3, -0.7, 0.5, -0.1],
    "buy":     [0.1, 0.3, -0.9, 0.7, 0.2, -0.1, 0.4, 0.0],
    "share":   [0.2, -0.1, 0.3, 0.5, -0.2, 0.1, -0.4, 0.3],
    "dismiss": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
}

# Load VAE model
vae = VAE(input_dim=60, latent_dim=8, hidden_dim=64)
model_path = os.path.join(project_root, 'deep-learning', 'models', 'vae_trained.pth')
vae.load_state_dict(torch.load(model_path))
vae.eval()

adaptive_layouts = []
for i, event in enumerate(dummy_events):
    # SAFE ACCESS: Use .get() with default 'dismiss'
    action = event.get('action', 'dismiss')
    latent_vec = action_to_vector.get(action, [0.0]*8)
    
    z = torch.tensor(latent_vec, dtype=torch.float32).unsqueeze(0)
    features = vae.decode(z).detach().numpy().flatten().tolist()
    
    # Create layout object
    layout = {
        "event": {
            "section": event.get('section', 'unknown'),
            "action": action
        },
        "features": features,
        "width": 260 + features[0] * 20,
        "height": 140 + features[1] * 10
    }
    adaptive_layouts.append(layout)

# Save to frontend/public/
output_dir = os.path.join(project_root, 'frontend', 'public')
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'adaptive_layout.json')

with open(output_path, 'w') as f:
    json.dump(adaptive_layouts, f, indent=2)

print(f"✅ Generated {len(adaptive_layouts)} adaptive layouts")
print(f"Saved to: {output_path}")
