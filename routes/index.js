// src/routes/index.js
import express from 'express';
import { UserController } from '../controllers/UserController.js';

export function loadRoutes(app) {
  const router = express.Router();
  const userCtrl = new UserController();

  router.get('/user/profile', userCtrl.getProfile);
  router.get('/account/balance', userCtrl.getBalance);

  app.use('/api', router);
}
