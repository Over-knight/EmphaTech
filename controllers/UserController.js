import { BaseController } from './BaseController.js';
import { users } from '../models/User.js';

export class UserController extends BaseController {
  constructor() {
    super();
  }

  getProfile = this.handle(async (req, res) => {
    // TODO: replace hard-coded userId with auth
    const user = users['user123'];
    res.json({
      userId: user.userId,
      firstName: user.firstName,
      accountNumber: user.accountNumber,
      phoneNumber: user.phoneNumber
    });
  });

  getBalance = this.handle(async (req, res) => {
    const user = users['user123'];
    res.json({
      balance: user.balance,
      currency: 'NGN',
      accountNumber: user.accountNumber,
      lastUpdated: new Date().toISOString()
    });
  });
}