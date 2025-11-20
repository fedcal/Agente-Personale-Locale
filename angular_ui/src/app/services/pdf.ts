import { Injectable } from '@angular/core';
// @ts-ignore
import * as pdfjsLib from 'pdfjs-dist/build/pdf';
import { Logger } from '../utils/logger.util';

@Injectable({
  providedIn: 'root',
})
export class Pdf {
  constructor() {
    // Imposta worker per pdf.js
    (pdfjsLib as any).GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.338/pdf.worker.min.js';
  }

  /**
   * Estrae testo da un file PDF.
   * @param file File PDF caricato dall'utente
   * @returns Promise<string> con tutto il testo del PDF
   */
  async extractText(file: File): Promise<string> {
    try {
      const arrayBuffer = await file.arrayBuffer();
      const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
      let fullText = '';

      for (let i = 1; i <= pdf.numPages; i++) {
        const page = await pdf.getPage(i);
        const content = await page.getTextContent();
        const pageText = content.items.map((item: any) => item.str).join(' ');
        fullText += pageText + '\n';
      }

      return fullText;
    } catch (err) {
      Logger.error('Errore PdfService.extractText:', err);
      return '';
    }
  }

  /**
   * Estrae metadati base da un PDF (autore, titolo, etc.)
   * @param file File PDF
   */
  async extractMetadata(file: File): Promise<any> {
    try {
      const arrayBuffer = await file.arrayBuffer();
      const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
      const metadata = await pdf.getMetadata();
      return metadata.info;
    } catch (err) {
      Logger.error('Errore PdfService.extractMetadata:', err);
      return {};
    }
  }

}
