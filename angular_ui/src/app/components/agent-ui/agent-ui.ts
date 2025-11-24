import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IconModule } from '../icon/icon.module';

@Component({
  selector: 'app-agent-ui',
  standalone: true,
  imports: [CommonModule, IconModule],
  templateUrl: './agent-ui.html',
  styleUrls: ['./agent-ui.css']
})
export class AgentUi {
  @Input() title = 'Ares Agent';
  @Output() openConfig = new EventEmitter<void>();
  @Output() goHome = new EventEmitter<void>();
}
