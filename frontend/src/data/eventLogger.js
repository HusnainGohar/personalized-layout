export async function logUserEvent(eventType, eventData) {
  try {
    await fetch('http://localhost:5000/api/user-event', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ eventType, eventData, timestamp: Date.now() })
    });
  } catch (err) {
    // Optionally handle error
    console.error('Failed to log user event:', err);
  }
} 