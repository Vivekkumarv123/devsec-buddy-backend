import express from 'express';
import { execFile } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const app = express();
app.use(express.json());

const __dirname = path.dirname(fileURLToPath(import.meta.url));

app.post('/api/scan', (req, res) => {
  const { url } = req.body;

  console.log(`📡 Scan request received for URL: ${url}`); // ✅ Add this
  const pythonScript = path.join(__dirname, '/scanner/main.py');

  execFile('python', [pythonScript, url], (error, stdout, stderr) => {
    console.log('🚀 Starting Python script...'); // ✅ Add this

    if (error) {
      console.error('❌ Scanner error:', error);
      return res.status(500).json({ error: 'Scanner failed to execute' });
    }

    try {
      console.log('📦 Python stdout:', stdout); // ✅ Output from scanner
      const result = JSON.parse(stdout);
      res.json(result);
    } catch (parseError) {
      console.error('⚠️ Invalid scanner output:', parseError);
      res.status(500).json({ error: 'Failed to parse scanner output' });
    }
  });
});


const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
  console.log(`🔐 DevSec Buddy backend running on http://localhost:${PORT}`);
});
