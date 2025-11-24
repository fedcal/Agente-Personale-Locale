import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterOutlet } from '@angular/router';

import { Agent } from './core/agent';
import { AgentUi} from './components/agent-ui/agent-ui';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    AgentUi,
    RouterOutlet
  ],
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class App {
  private agent = inject(Agent);
  private router = inject(Router);

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

  get commands() {
    return this.agent.getCommands();
  }

  toggleConfig() {
    this.router.navigate(['/sites']);
  }

  goHome() {
    this.router.navigate(['/']);
  }

  sendMessage(userInput: string) {
    this.agent.sendMessage(userInput);
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

  renameSession(id: string, title: string) {
    this.agent.renameSession(id, title);
  }
}
