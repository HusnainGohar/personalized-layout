import json
import os
from datetime import datetime
import random

event_types = ['click', 'scroll', 'hover', 'input']
sections = ['card', 'main', 'button', 'sidebar', 'footer']
actions = ['like', 'view', 'buy', 'share', 'dismiss']

N = 10
now = int(datetime.now().timestamp() * 1000)  # milliseconds

output_dir = os.path.join(os.getcwd(), 'deep-learning', 'data')
output_file = 'dummyUserEvents.json'
os.makedirs(output_dir, exist_ok=True)

dummyUserEvents = [
    {
        'event': random.choice(event_types),
        'section': random.choice(sections),
        'timestamp': now + i * 1000,
        'action': random.choice(actions)
    }
    for i in range(N)
]

output_path = os.path.join(output_dir, output_file)
with open(output_path, 'w') as f:
    json.dump(dummyUserEvents, f, indent=2)

print(f"Generated {N} dummy user events and saved to {output_path}")
