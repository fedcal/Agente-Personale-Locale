import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Agent } from '../../core/agent';
import { Chat } from '../../components/chat/chat';
import { ModelSelector } from '../../components/model-selector/model-selector';
import { Sidebar } from '../../components/sidebar/sidebar';
import { AgentUi } from '../../components/agent-ui/agent-ui';
import { FormsModule } from '@angular/forms';
import { ChatSessions } from '../../components/chat-sessions/chat-sessions';

@Component({
  selector: 'app-agent',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    AgentUi,
    Sidebar,
    Chat,
    ModelSelector,
    ChatSessions
  ],
  templateUrl: './agent.html',
  styleUrls: ['./agent.css']
})
export class AgentPage {
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

  sendMessage(text: string) {
    this.agent.sendMessage(text);
  }

  selectModel(model: string) {
    this.agent.selectModel(model);
  }

  clearHistory() {
    this.agent.clearHistory();
  }

  get sessionItems() {
    return this.agent.getSessions();
  }

  newSession() {
    this.agent.newSession();
  }

  selectSession(id: string) {
    this.agent.selectSession(id);
  }
}
