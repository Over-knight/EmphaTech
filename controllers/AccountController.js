// src/controllers/AccountController.js

import { BaseController } from './BaseController.js';

export class AccountController extends BaseController {
  /**
   * POST /api/account/verify
   * Body: { accountNumber, bankName, requestId }
   * Returns a mocked accountName for now.
   */
  verify = this.handle(async (req, res) => {
    const { accountNumber, bankName, requestId } = req.body;

    const accountName = 'Bola Okoro';

    res.json({
      accountNumber,
      bankName,
      accountName,
      requestId
    });
  });
}
