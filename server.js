// src/server.js
import express from 'express';
import bodyParser from 'body-parser';
import { loadRoutes } from './routes/index.js';
import dotenv from 'dotenv';
import cors from 'cors'

dotenv.config();  // load .env into process.env

const app = express();

// Middleware
app.use(bodyParser.json());

app.use(cors({
  origin: ['http://localhost:5173', 'http://localhost:5174' ],
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

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
export default app; 