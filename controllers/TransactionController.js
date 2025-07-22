
import { BaseController } from './BaseController.js';
import { users } from '../models/User.js';
import { transactions } from '../models/Transaction.js';
import { v4 as uuidv4 } from 'uuid';

export class TransactionController extends BaseController {
  /**
   * POST /api/transaction/create
   * Body: { amount, currency, recipientAccount, recipientBank, sessionId }
   */
  create = this.handle(async (req, res) => {
    const { amount, currency, recipientAccount, recipientBank, sessionId } = req.body;

    // Simple funds check
    const user = users['user123'];
    if (amount > user.balance) {
      return res.status(400).json({ error: 'Insufficient funds' });
    }

    // Create transaction record
    const transactionId = uuidv4();
    transactions[transactionId] = {
      transactionId,
      from: user.accountNumber,
      to: recipientAccount,
      amount,
      currency,
      recipientBank,
      status: 'pending',
      sessionId,
      createdAt: new Date().toISOString()
    };

    // Deduct immediately (for demo)
    user.balance -= amount;

    res.json({ transactionId, status: 'pending' });
  });
}
