import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { Agent } from './core/agent';
import { Sidebar } from './components/sidebar/sidebar';
import { Chat } from './components/chat/chat';
import { ModelSelector } from './components/model-selector/model-selector';
import { AgentUi} from './components/agent-ui/agent-ui';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    Sidebar,
    Chat,
    ModelSelector,
    AgentUi
  ],
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class App {
  private agent = inject(Agent);

  get models() {
    return this.agent.models();
  }

  get messages() {
    return this.agent.messages();
  }

  get selectedModel() {
    return this.agent.selectedModel();
  }

  get temperature() {
    return this.agent.temperature();
  }

  sendMessage(userInput: string) {
    this.agent.sendMessage(userInput);
  }

  selectModel(model: string) {
    this.agent.selectModel(model);
  }
}
