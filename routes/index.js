// src/routes/index.js
import express from 'express';
import { UserController } from '../controllers/UserController.js';
import { BankController } from '../controllers/BankController.js';
import { TransactionController } from '../controllers/transactionController.js';

export function loadRoutes(app) {
  const router = express.Router();
  const userCtrl = new UserController();
  const bankCtrl = new BankController();
  const transactionCtrl= new TransactionController();

  // user endpoints
  router.get('/user/profile', userCtrl.getProfile);
  router.get('/account/balance', userCtrl.getBalance);
  router.post('/transaction/create', transactionCtrl.create);

  //bank list endpoint
  router.get('/banks/list', bankCtrl.list);
  app.use('/api', router);
}
