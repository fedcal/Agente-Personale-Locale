import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

export interface SessionItem {
  id: string;
  title: string;
  active: boolean;
  editing?: boolean;
}

@Component({
  selector: 'app-chat-sessions',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chat-sessions.html',
  styleUrls: ['./chat-sessions.css']
})
export class ChatSessions {
  @Input() sessions: SessionItem[] = [];
  @Input() onSelect!: (id: string) => void;
  @Input() onNew!: () => void;
  @Input() onRename!: (id: string, title: string) => void;

  select(id: string) {
    this.onSelect(id);
  }

  add() {
    this.onNew();
  }

  rename(id: string, title: string) {
    const value = title.trim();
    if (!value) return;
    this.onRename(id, value);
  }
}
