
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

   /**
   * POST /api/transaction/execute
   * Body: { transactionId, pinVerified, finalConfirmation }
   */
  execute = this.handle(async (req, res) => {
    const { transactionId, pinVerified, finalConfirmation } = req.body;
    const txn = transactions[transactionId];

    if (!txn) {
      return res.status(404).json({ error: 'Transaction not found' });
    }
    if (!pinVerified || !finalConfirmation) {
      txn.status = 'failed';
      return res.status(400).json({ error: 'Verification failed' });
    }

    txn.status = 'successful';
    txn.completedAt = new Date().toISOString();

    res.json({
      transactionId: txn.transactionId,
      status: txn.status
    });
  });

  /**
   * GET /api/transaction/status/:transactionId
   * Returns status, newBalance, referenceNumber, timestamp, errorMessage
   */
  status = this.handle(async (req, res) => {
    const { transactionId } = req.params;
    const txn = transactions[transactionId];

    if (!txn) {
      return res.status(404).json({ error: 'Transaction not found' });
    }

    // For demo, referenceNumber = T + first 9 chars of ID
    const referenceNumber = 'T' + transactionId.replace(/-/g, '').substring(0, 9);
    const user = users['user123'];

    res.json({
      transactionId:   txn.transactionId,
      status:          txn.status,
      newBalance:      user.balance,
      referenceNumber,
      timestamp:       txn.completedAt || txn.createdAt,
      errorMessage:    txn.status === 'failed' ? 'Verification failed or insufficient funds' : null
    });
  });
}






