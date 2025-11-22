import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Agent } from '../../core/agent';
import { AgentUi } from '../../components/agent-ui/agent-ui';
import { Sidebar } from '../../components/sidebar/sidebar';
import { Chat } from '../../components/chat/chat';
import { ModelSelector } from '../../components/model-selector/model-selector';
import { ChatSessions } from '../../components/chat-sessions/chat-sessions';
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
    ModelSelector,
    ChatSessions
  ],
  templateUrl: './home.html',
  styleUrls: ['./home.css']
})
export class HomePage {
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
