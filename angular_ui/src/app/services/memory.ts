import { Injectable, inject } from '@angular/core';

export interface Message {
  role: 'user' | 'assistant';
  text: string;
}


@Injectable({
  providedIn: 'root',
})
export class Memory {
  private history: Message[] = [];

  storeMessage(userMessage: Message, agentResponse: Message) {
    this.history.push(userMessage);
    this.history.push(agentResponse);
  }

  getHistory(): Message[] {
    return this.history;
  }

  clearHistory() {
    this.history = [];
  }
}
