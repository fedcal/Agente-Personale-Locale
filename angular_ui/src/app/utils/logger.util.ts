export class Logger {

  /**
   * Log informativo
   * @param message Messaggio da stampare
   * @param data Dati opzionali da loggare
   */
  static info(message: string, data?: any) {
    console.info(`[INFO] ${message}`, data ?? '');
  }

  /**
   * Log di warning
   * @param message Messaggio da stampare
   * @param data Dati opzionali da loggare
   */
  static warn(message: string, data?: any) {
    console.warn(`[WARN] ${message}`, data ?? '');
  }

  /**
   * Log di errore
   * @param message Messaggio da stampare
   * @param data Dati opzionali da loggare
   */
  static error(message: string, data?: any) {
    console.error(`[ERROR] ${message}`, data ?? '');
  }

  /**
   * Log generico
   * @param message Messaggio da stampare
   * @param data Dati opzionali da loggare
   */
  static log(message: string, data?: any) {
    console.log(`[LOG] ${message}`, data ?? '');
  }
}
