import express from 'express';
import { UserController } from '../controllers/UserController.js';
import { BankController } from '../controllers/BankController.js';
import { TransactionController } from '../controllers/transactionController.js';
import { AccountController } from '../controllers/AccountController.js';

export function loadRoutes(app) {
  const router = express.Router();
  const userCtrl = new UserController();
  const bankCtrl = new BankController();
  const transactionCtrl= new TransactionController();
  const acctCtrl = new AccountController(); 

  

  // user endpoints
  router.get('/user/profile', userCtrl.getProfile);
  router.get('/account/balance', userCtrl.getBalance);
  router.post('/transaction/create', transactionCtrl.create);
  router.post('/account/verify', acctCtrl.verify);
  router.post('/transaction/execute', transactionCtrl.execute);
  router.get('/transaction/status/:transactionId', transactionCtrl.status);

  //bank list endpoint
  router.get('/banks/list', bankCtrl.list);
  app.use('/api', router);
}
