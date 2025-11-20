import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

export interface ChatMessage {
  role: 'user' | 'assistant';
  text: string;
}

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chat.html',
  styleUrls: ['./chat.css']
})
export class Chat {
  @Input() messages: ChatMessage[] = [];
  @Input() userInput = '';
  @Input() onSend!: (text: string) => void;

  send() {
    if (this.userInput.trim()) {
      this.onSend(this.userInput.trim());
      this.userInput = '';
    }
  }
}
