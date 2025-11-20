import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-agent-ui',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './agent-ui.html',
  styleUrls: ['./agent-ui.css']
})
export class AgentUi {
  @Input() title = 'Agente Personale';
}
