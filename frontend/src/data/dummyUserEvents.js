// dummyUserEvents.js
export const dummyUserEvents = [
  { event: "click", section: "card", timestamp: Date.now(), action: "like" },
  { event: "scroll", section: "main", timestamp: Date.now() + 1000, action: "view" },
  { event: "click", section: "button", timestamp: Date.now() + 2000, action: "buy" }
];
