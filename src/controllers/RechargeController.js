// src/controllers/RechargeController.js

import { BaseController } from './BaseController.js';
import { users } from '../models/User.js';

export class RechargeController extends BaseController {
  /**
   * POST /api/recharge-card
   * Body: { amount }
   * Deducts from balance and returns a mock voucher code
   */
  buy = this.handle(async (req, res) => {
    const { amount } = req.body;
    const user = users['user123'];
    if (amount > user.balance) {
      return res.status(400).json({ error: 'Insufficient funds' });
    }
    user.balance -= amount;
    // Stub a voucher/pin code
    const voucher = Math.floor(100000 + Math.random() * 900000).toString();
    res.json({
      status:     'success',
      newBalance: user.balance,
      voucher
    });
  });
}
