export class File {
  /**
   * Legge un file come testo
   * @param file File da leggere
   * @returns Promise<string> contenente il testo del file
   */
  static async readAsText(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result as string);
      reader.onerror = (err) => reject(err);
      reader.readAsText(file);
    });
  }

  /**
   * Converte un file in ArrayBuffer
   * @param file File da convertire
   */
  static async readAsArrayBuffer(file: File): Promise<ArrayBuffer> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result as ArrayBuffer);
      reader.onerror = (err) => reject(err);
      reader.readAsArrayBuffer(file);
    });
  }

  /**
   * Scarica un testo come file .txt
   * @param filename Nome del file da salvare
   * @param content Contenuto testuale
   */
  static saveTextFile(filename: string, content: string) {
    const blob = new Blob([content], { type: 'text/plain' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
    URL.revokeObjectURL(link.href);
  }

  /**
   * Scarica un ArrayBuffer come file
   * @param filename Nome del file
   * @param buffer Contenuto come ArrayBuffer
   * @param type MIME type (default octet-stream)
   */
  static saveArrayBufferFile(filename: string, buffer: ArrayBuffer, type = 'application/octet-stream') {
    const blob = new Blob([buffer], { type });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
    URL.revokeObjectURL(link.href);
  }
}
