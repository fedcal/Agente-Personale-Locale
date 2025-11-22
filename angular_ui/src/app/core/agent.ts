import { Injectable, inject, WritableSignal, signal } from '@angular/core';
import { Ollama } from '../services/ollama';

export interface Message {
  role: 'user' | 'assistant';
  text: string;
}

const FALLBACK_MODELS = ['llama3.1:latest', 'qwen2.5-coder:latest', 'nomic-embed-text:latest'];

@Injectable({ providedIn: 'root' })
export class Agent {
  private ollama = inject(Ollama);

  messages: WritableSignal<Message[]> = signal([]);
  models: WritableSignal<string[]> = signal([]);
  selectedModel: WritableSignal<string> = signal('llama3');
  temperature: WritableSignal<number> = signal(0.7);

  constructor() {
    this.bootstrap();
  }

  private async bootstrap() {
    const [history, availableModels] = await Promise.all([
      this.ollama.history(),
      this.ollama.models()
    ]);
    if (history.length) {
      this.messages.set(history);
    }
    const list = availableModels.length ? availableModels : FALLBACK_MODELS;
    this.models.set(list);
    const preferred = list.find(m => !m.toLowerCase().includes('embed')) || list[0];
    this.selectedModel.set(preferred);
  }

  selectModel(model: string) {
    const m = model.trim();
    if (!m) return;
    this.selectedModel.set(m);
  }

  async sendMessage(userText: string) {
    const text = userText.trim();
    if (!text) return;

    const newUserMsg: Message = { role: 'user', text };
    this.messages.update(msgs => [...msgs, newUserMsg]);

    const model = this.selectedModel() || this.models()[0] || 'llama3.1';
    const responseText = await this.ollama.ask(model, text, this.temperature());
    const assistantMsg: Message = { role: 'assistant', text: responseText };

    this.messages.update(msgs => [...msgs, assistantMsg]);
  }

  async clearHistory() {
    await this.ollama.clearHistory();
    this.messages.set([]);
  }
}
