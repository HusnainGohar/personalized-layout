import json
import csv
from collections import Counter, defaultdict

# Path to the user events log
USER_EVENTS_PATH = 'backend/utils/user_events.json'
OUTPUT_CSV_PATH = 'data/processed/aggregated_user_events.csv'

# List of known components to track (extend as needed)
COMPONENTS = [
    'analytics-card',
    'profile-card',
    'notifications-card',
    'dashboard-menu',
    'profile-menu',
    'settings-menu',
    'adaptive-action-btn',
]

def aggregate_events():
    # Counter for each component
    component_counts = Counter()
    total_clicks = 0

    with open(USER_EVENTS_PATH, 'r') as f:
        for line in f:
            try:
                event = json.loads(line)
                if event.get('eventType') == 'click':
                    comp = event.get('eventData', {}).get('component')
                    if comp in COMPONENTS:
                        component_counts[comp] += 1
                        total_clicks += 1
            except Exception as e:
                continue  # skip malformed lines

    # Prepare CSV header and row
    header = [f'{c}_clicks' for c in COMPONENTS] + ['total_clicks']
    row = [component_counts[c] for c in COMPONENTS] + [total_clicks]

    # Write to CSV
    with open(OUTPUT_CSV_PATH, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerow(row)
    print(f'Aggregated user event features saved to {OUTPUT_CSV_PATH}')

if __name__ == '__main__':
    aggregate_events() 