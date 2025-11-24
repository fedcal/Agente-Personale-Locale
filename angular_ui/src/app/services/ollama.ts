import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';
import { Message } from '../core/agent';

interface ChatResponse {
  response: string;
  model: string;
}

@Injectable({ providedIn: 'root' })
export class Ollama {
  private http = inject(HttpClient);
  private baseUrl = 'http://localhost:8000';

  async ask(model: string, prompt: string, temperature: number): Promise<string> {
    try {
      const body = { model, message: prompt, temperature };
      const response = await firstValueFrom(this.http.post<ChatResponse>(`${this.baseUrl}/chat`, body));
      return response.response;
    } catch (err) {
      console.error('Errore in Ollama:', err);
      return 'Errore di connessione all\'agente';
    }
  }

  async models(): Promise<string[]> {
    try {
      return await firstValueFrom(this.http.get<string[]>(`${this.baseUrl}/models`));
    } catch {
      return [];
    }
  }

  async history(): Promise<Message[]> {
    try {
      const res = await firstValueFrom(this.http.get<{ history: Message[] }>(`${this.baseUrl}/memory`));
      return res.history ?? [];
    } catch {
      return [];
    }
  }

  async clearHistory(): Promise<void> {
    await firstValueFrom(this.http.delete(`${this.baseUrl}/memory`));
  }

  async commands(): Promise<{ name: string; description: string; params: string }[]> {
    try {
      return await firstValueFrom(this.http.get<{ name: string; description: string; params: string }[]>(`${this.baseUrl}/commands`));
    } catch {
      return [];
    }
  }
}
