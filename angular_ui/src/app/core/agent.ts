import { Injectable, inject } from '@angular/core';
import { Ollama } from '../services/ollama';
import { Memory } from '../services/memory';

export interface Message {
  role: 'user' | 'assistant';
  text: string;
}

@Injectable({
  providedIn: 'root',
})
export class Agent {
  private ollama = inject(Ollama);
  private memory = inject(Memory);

  messages: Message[] = [];
  selectedModel: string = 'llama3';
  temperature: number = 0.7;

  constructor() {
    // eventualmente inizializza la memoria con conversazioni precedenti
    this.messages = this.memory.getHistory();
  }

  selectModel(model: string) {
    this.selectedModel = model;
  }

  async sendMessage(userText: Message): Promise<Message> {
    if (!userText.text.trim()) throw new Error('Messaggio vuoto');

    this.messages.push(userText);

    const responseText = await this.ollama.ask(this.selectedModel, userText.text);
    const assistantMsg: Message = { role: 'assistant', text: responseText };
    this.messages.push(assistantMsg);

    // salva nella memoria
    this.memory.storeMessage(userText, assistantMsg);

    return assistantMsg;
  }

  getHistory(): Message[] {
    return this.messages;
  }

  clearHistory() {
    this.messages = [];
    this.memory.clearHistory();
  }
}
