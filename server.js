// src/server.js
import express from 'express';
import bodyParser from 'body-parser';
import { loadRoutes } from './routes/index.js';
import dotenv from 'dotenv';

dotenv.config();  // load .env into process.env

const app = express();

// Middleware
app.use(bodyParser.json());

// Mount all API routes under /api
loadRoutes(app);

// Health‑check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok' });
});

// Start the server
const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});