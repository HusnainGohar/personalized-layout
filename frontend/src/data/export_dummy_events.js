import { dummyUserEvents } from './dummyUserEvents.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Define output path
const outputPath = path.resolve(__dirname, '../../../deep-learning/data/dummyUserEvents.json');

// Create directory if it doesn't exist
const outputDir = path.dirname(outputPath);
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });  // Fix: Create parent directories
}

// Write file
fs.writeFileSync(outputPath, JSON.stringify(dummyUserEvents, null, 2));
console.log(`✅ Exported to: ${outputPath}`);
