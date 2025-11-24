import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AfterViewChecked, ElementRef, ViewChild } from '@angular/core';
import { MarkdownPipe } from '../../pipes/markdown.pipe';
import { CommandHint } from '../command-hint/command-hint';

export interface ChatMessage {
  role: 'user' | 'assistant';
  text: string;
}

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule, MarkdownPipe, CommandHint],
  templateUrl: './chat.html',
  styleUrls: ['./chat.css']
})
export class Chat implements AfterViewChecked, OnChanges {
  @ViewChild('messagesContainer') messagesContainer!: ElementRef<HTMLDivElement>;
  @Input() messages: ChatMessage[] = [];
  @Input() userInput = '';
  @Input() onSend!: (text: string) => void;
  @Input() commands: { name: string; description: string; params: string }[] = [];

  listening = false;
  hasSpeech = 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window;
  recognition: any;
  loading = false;
  private shouldScroll = false;
  private lastCount = 0;
  showCommands = false;

  send() {
    if (this.userInput.trim()) {
      this.loading = true;
      this.onSend(this.userInput.trim());
      this.userInput = '';
      this.shouldScroll = true;
      setTimeout(() => (this.loading = false), 500);
    }
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['messages']) {
      const current = this.messages?.length ?? 0;
      if (current > this.lastCount) {
        this.shouldScroll = true;
        const last = this.messages[current - 1];
        if (last?.role === 'assistant') {
          this.loading = false;
        }
      }
      this.lastCount = current;
    }
  }

  ngAfterViewChecked() {
    if (this.shouldScroll && this.messagesContainer) {
      const el = this.messagesContainer.nativeElement;
      el.scrollTop = el.scrollHeight;
      this.shouldScroll = false;
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

  onInputChange() {
    this.showCommands = this.userInput.startsWith('/');
  }

  pickCommand(cmd: string) {
    this.userInput = cmd;
    this.showCommands = false;
  }
}
