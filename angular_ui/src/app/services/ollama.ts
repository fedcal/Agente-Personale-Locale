import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class Ollama {
  private http = inject(HttpClient);
  private baseUrl = 'http://localhost:11434/api';

  async ask(model: string, prompt: string, temperature: number): Promise<string> {
    try {
      const body = { model, prompt, temperature };
      const response = await this.http
        .post(`${this.baseUrl}/generate`, body, { responseType: 'text' })
        .toPromise();
      return response ?? 'Nessuna risposta dal modello';
    } catch (err) {
      console.error('Errore in Ollama:', err);
      return 'Errore di connessione a Ollama';
    }
  }
}
