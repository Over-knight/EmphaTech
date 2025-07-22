export class BaseController {
  constructor() {}

  /**
   * Wrapper to handle async controller methods and errors
   */
  handle(fn) {
    return async (req, res, next) => {
      try {
        await fn(req, res);
      } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Internal Server Error' });
      }
    };
  }
}