import { Component, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { Ollama } from './services/ollama';
import { Memory } from './services/memory';
import { Sidebar } from './components/sidebar/sidebar';
import { Chat } from './components/chat/chat';
import { ModelSelector } from './components/model-selector/model-selector';
import { AgentUi } from './components/agent-ui/agent-ui';
import {RouterOutlet} from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  private ollama = inject(Ollama);
  private memory = inject(Memory);

  models = ['llama3', 'mistral', 'codellama'];
  selectedModel = 'llama3';
  userInput = '';
  messages: { role: string; text: string }[] = [];
  temperature = 0.7;

  selectModel(model: string) {
    this.selectedModel = model;
  }

  async send() {
    if (!this.userInput.trim()) return;

    this.messages.push({ role: 'user', text: this.userInput });

    const response = await this.ollama.ask(this.selectedModel, this.userInput);
    this.memory.storeMessage(this.userInput, response);

    this.messages.push({ role: 'assistant', text: response });
    this.userInput = '';
  }
}
