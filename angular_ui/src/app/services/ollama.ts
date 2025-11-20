import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class Ollama {
  private http = inject(HttpClient);
  private baseUrl = 'http://localhost:11434/api';

  async ask(model: string, prompt: string): Promise<string> {
    try {
      const response = await this.http.post(
        `${this.baseUrl}/generate`,
        { model, prompt },
        { responseType: 'text' }
      ).toPromise();

      return response ?? 'Nessuna risposta dal modello';
    } catch (err) {
      console.error('Errore OllamaService:', err);
      return 'Errore di connessione a Ollama';
    }
  }
}
