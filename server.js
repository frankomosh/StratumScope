const express = require('express');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Start Python backend
console.log('Starting Python backend...');
const python = spawn('python', ['run.py'], {
    env: { ...process.env, PYTHONUNBUFFERED: '1' }
});

python.stdout.on('data', (data) => {
    console.log(`Python: ${data.toString()}`);
});

python.stderr.on('data', (data) => {
    console.error(`Python Error: ${data.toString()}`);
});

python.on('error', (error) => {
    console.error('Failed to start Python process:', error);
});

// Serve frontend
app.use(express.static('./frontend'));

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ status: 'ok', backend: python.pid ? 'running' : 'stopped' });
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});