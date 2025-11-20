import { Injectable } from '@angular/core';
import { Message } from '../core/agent';

@Injectable({ providedIn: 'root' })
export class MemoryPlus {
  private history: Message[] = [];

  storeMessage(userMessage: string, assistantMessage: string) {
    this.history.push({ role: 'user', text: userMessage });
    this.history.push({ role: 'assistant', text: assistantMessage });
  }

  getHistory(): Message[] {
    return [...this.history];
  }

  clearHistory() {
    this.history = [];
  }
}
