const express = require('express');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// will calls the python backend
console.log('Starting Python backend...');
const python = spawn('python', ['run.py']);

python.stdout.on('data', (data) => {
  console.log(`Python: ${data}`);
});

app.use(express.static('./frontend'));

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});