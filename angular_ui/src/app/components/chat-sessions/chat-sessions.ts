import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

export interface SessionItem {
  id: string;
  title: string;
  active: boolean;
}

@Component({
  selector: 'app-chat-sessions',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './chat-sessions.html',
  styleUrls: ['./chat-sessions.css']
})
export class ChatSessions {
  @Input() sessions: SessionItem[] = [];
  @Input() onSelect!: (id: string) => void;
  @Input() onNew!: () => void;

  select(id: string) {
    this.onSelect(id);
  }

  add() {
    this.onNew();
  }
}
