// src/controllers/SendController.js

import { BaseController } from './BaseController.js';
import { users } from '../models/User.js';

export class SendController extends BaseController {
  /**
   * POST /api/transaction/send-money
   * Body: { amount }
   * Simply deducts from the demo user’s balance
   */
  sendMoney = this.handle(async (req, res) => {
    const { amount } = req.body;
    const user = users['user123'];
    if (amount > user.balance) {
      return res.status(400).json({ error: 'Insufficient funds' });
    }
    user.balance -= amount;
    res.json({
      status:     'success',
      newBalance: user.balance
    });
  });
}
