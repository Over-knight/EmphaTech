import express from 'express';
import { UserController } from '../controllers/UserController.js';
import { BankController } from '../controllers/BankController.js';
import { TransactionController } from '../controllers/transactionController.js';
import { AccountController } from '../controllers/AccountController.js';
import { RechargeController } from '../controllers/RechargeController.js';
import { SendController } from '../controllers/sendController.js';
import { UIController } from '../controllers/UIController.js';

export function loadRoutes(app) {
  const router = express.Router();
  const userCtrl = new UserController();
  const bankCtrl = new BankController();
  const transactionCtrl= new TransactionController();
  const acctCtrl = new AccountController(); 
  const rechargeCtrl = new RechargeController();
  const sendCtrl = new SendController();
  const uiCtrl = new UIController();
  

  // user endpoints
  router.get('/user/profile', userCtrl.getProfile);
  router.get('/account/balance', userCtrl.getBalance);
  router.post('/transaction/create', transactionCtrl.create);
  router.post('/account/verify', acctCtrl.verify);
  router.post('/transaction/execute', transactionCtrl.execute);
  router.get('/transaction/status/:transactionId', transactionCtrl.status);
  router.post('/recharge-card', rechargeCtrl.buy);
  router.post('/transaction/send-money', sendCtrl.sendMoney);
  // UI endpoints
  router.post('/ui/transcript/update', uiCtrl.transcriptUpdate);
  router.post('/ui/voice-indicator/update', uiCtrl.voiceIndicatorUpdate);
  router.post('/ui/transaction-panel/update', uiCtrl.transactionPanelUpdate);

  //bank list endpoint
  router.get('/banks/list', bankCtrl.list);
  app.use('/api', router);
}
