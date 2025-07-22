// src/controllers/BankController.js

import { BaseController } from './BaseController.js';
import { banks } from '../models/Bank.js';

export class BankController extends BaseController {
  /**
   * GET /api/banks/list
   */
  list = this.handle(async (req, res) => {
    res.json({ banks });
  });
}
