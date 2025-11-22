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

  listening = false;
  hasSpeech = 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window;
  recognition: any;

  send() {
    if (this.userInput.trim()) {
      this.onSend(this.userInput.trim());
      this.userInput = '';
    }
  }

  toggleVoice() {
    if (!this.hasSpeech) return;
    if (this.listening) {
      this.stopVoice();
    } else {
      this.startVoice();
    }
  }

  startVoice() {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) return;
    this.recognition = new SpeechRecognition();
    this.recognition.lang = 'it-IT';
    this.recognition.interimResults = false;
    this.recognition.maxAlternatives = 1;
    this.listening = true;
    this.recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      this.userInput = transcript;
      this.send();
    };
    this.recognition.onend = () => {
      this.listening = false;
    };
    this.recognition.onerror = () => {
      this.listening = false;
    };
    this.recognition.start();
  }

  stopVoice() {
    if (this.recognition) {
      this.recognition.stop();
    }
    this.listening = false;
  }
}
