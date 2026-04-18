// src/controllers/UIController.js

import { BaseController } from './BaseController.js';

export class UIController extends BaseController {
  /**
   * POST /api/ui/transcript/update
   * Body: { sessionId, speaker, message, timestamp }
   */
  transcriptUpdate = this.handle(async (req, res) => {
    // stub: acknowledge receipt
    res.json({ status: 'ok' });
  });

  /**
   * POST /api/ui/voice-indicator/update
   * Body: { sessionId, state, vibrancy, timestamp }
   */
  voiceIndicatorUpdate = this.handle(async (req, res) => {
    res.json({ status: 'ok' });
  });

  /**
   * POST /api/ui/transaction-panel/update
   * Body: { sessionId, transactionId, updates }
   */
  transactionPanelUpdate = this.handle(async (req, res) => {
    res.json({ status: 'ok' });
  });
}
