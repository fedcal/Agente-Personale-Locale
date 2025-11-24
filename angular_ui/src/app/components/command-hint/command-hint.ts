import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';

export interface CommandInfo {
  name: string;
  description: string;
  params: string;
}

@Component({
  selector: 'app-command-hint',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './command-hint.html',
  styleUrls: ['./command-hint.css']
})
export class CommandHint {
  @Input() commands: CommandInfo[] = [];
  @Input() visible = false;
  @Output() onSelect = new EventEmitter<string>();

  select(cmd: string) {
    this.onSelect.emit(cmd);
  }
}
