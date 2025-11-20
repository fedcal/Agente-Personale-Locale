import { Injectable, inject, WritableSignal, signal } from '@angular/core';
import { Ollama } from '../services/ollama';
import { MemoryPlus } from '../services/memory';

export interface Message {
  role: 'user' | 'assistant';
  text: string;
}

@Injectable({ providedIn: 'root' })
export class Agent {
  private ollama = inject(Ollama);
  private memory = inject(MemoryPlus);

  messages: WritableSignal<Message[]> = signal(this.memory.getHistory());
  selectedModel: WritableSignal<string> = signal('llama3');
  temperature: WritableSignal<number> = signal(0.7);

  constructor() {}

  selectModel(model: string) {
    this.selectedModel.set(model);
  }

  async sendMessage(userText: string) {
    const text = userText.trim();
    if (!text) return;

    const newUserMsg: Message = { role: 'user', text };
    this.messages.update(msgs => [...msgs, newUserMsg]);

    const model = this.selectedModel();
    const responseText = await this.ollama.ask(model, text, this.temperature());
    const assistantMsg: Message = { role: 'assistant', text: responseText };

    this.messages.update(msgs => [...msgs, assistantMsg]);
    this.memory.storeMessage(text, responseText);
  }

  clearHistory() {
    this.memory.clearHistory();
    this.messages.set([]);
  }
}
