import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Agent } from '../../core/agent';
import { AgentUi } from '../../components/agent-ui/agent-ui';
import { Sidebar } from '../../components/sidebar/sidebar';
import { Chat } from '../../components/chat/chat';
import { ModelSelector } from '../../components/model-selector/model-selector';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    AgentUi,
    Sidebar,
    Chat,
    ModelSelector
  ],
  templateUrl: './home.html',
  styleUrls: ['./home.css']
})
export class HomePage {
  private agent = inject(Agent);

  allModels = ['llama3', 'mistral', 'codellama'];

  get messages() {
    return this.agent.messages();
  }

  get selectedModel() {
    return this.agent.selectedModel();
  }

  get temperature() {
    return this.agent.temperature();
  }

  sendMessage(text: string) {
    this.agent.sendMessage(text);
  }

  selectModel(model: string) {
    this.agent.selectModel(model);
  }
}
