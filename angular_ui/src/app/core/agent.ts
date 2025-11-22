import { Injectable, inject, WritableSignal, signal } from '@angular/core';
import { Ollama } from '../services/ollama';

export interface Message {
  role: 'user' | 'assistant';
  text: string;
}

export interface ChatSession {
  id: string;
  title: string;
  messages: Message[];
}

const FALLBACK_MODELS = ['llama3.1:latest', 'qwen2.5-coder:latest', 'nomic-embed-text:latest'];
const STORAGE_KEY = 'ares_chat_sessions';

@Injectable({ providedIn: 'root' })
export class Agent {
  private ollama = inject(Ollama);

  messages: WritableSignal<Message[]> = signal([]);
  models: WritableSignal<string[]> = signal([]);
  selectedModel: WritableSignal<string> = signal('llama3.1:latest');
  temperature: WritableSignal<number> = signal(0.7);
  sessions: WritableSignal<ChatSession[]> = signal([]);
  currentSessionId: WritableSignal<string> = signal('');
  ready: WritableSignal<boolean> = signal(false);

  constructor() {
    this.bootstrap();
  }

  private async bootstrap() {
    const [history, availableModels] = await Promise.all([
      this.ollama.history(),
      this.ollama.models()
    ]);

    const stored = this.loadSessions();
    if (stored.sessions.length) {
      this.sessions.set(stored.sessions);
      this.currentSessionId.set(stored.currentId || stored.sessions[0].id);
      const current = stored.sessions.find(s => s.id === this.currentSessionId());
      this.messages.set(current ? [...current.messages] : []);
    } else {
      const initialSession: ChatSession = {
        id: this.uuid(),
        title: 'Chat 1',
        messages: history.length ? history : []
      };
      this.sessions.set([initialSession]);
      this.currentSessionId.set(initialSession.id);
      this.messages.set([...initialSession.messages]);
      this.saveSessions();
    }

    const list = availableModels.length ? availableModels : FALLBACK_MODELS;
    this.models.set(list);
    const preferred = list.find(m => !m.toLowerCase().includes('embed')) || list[0];
    this.selectedModel.set(preferred);
    this.ready.set(true);
  }

  private uuid() {
    return crypto.randomUUID ? crypto.randomUUID() : Math.random().toString(36).slice(2);
  }

  getSessions() {
    const current = this.currentSessionId();
    return this.sessions().map(s => ({ ...s, active: s.id === current }));
  }

  newSession() {
    const nextIndex = this.sessions().length + 1;
    const session: ChatSession = { id: this.uuid(), title: `Chat ${nextIndex}`, messages: [] };
    this.sessions.update(list => [...list, session]);
    this.currentSessionId.set(session.id);
    this.messages.set([]);
    this.saveSessions();
  }

  selectSession(id: string) {
    const found = this.sessions().find(s => s.id === id);
    if (found) {
      this.currentSessionId.set(id);
      this.messages.set([...found.messages]);
      this.saveSessions();
    }
  }

  selectModel(model: string) {
    const m = model.trim();
    if (!m) return;
    this.selectedModel.set(m);
  }

  async sendMessage(userText: string) {
    const text = userText.trim();
    if (!text) return;

    const newUserMsg: Message = { role: 'user', text };
    this.updateCurrentSession([...this.messages(), newUserMsg]);

    const model = this.selectedModel() || this.models()[0] || 'llama3.1';
    const responseText = await this.ollama.ask(model, text, this.temperature());
    const assistantMsg: Message = { role: 'assistant', text: responseText };

    this.updateCurrentSession([...this.messages(), assistantMsg]);
  }

  async clearHistory() {
    await this.ollama.clearHistory();
    this.updateCurrentSession([]);
  }

  private updateCurrentSession(msgs: Message[]) {
    const id = this.currentSessionId();
    this.messages.set(msgs);
    this.sessions.update(list =>
      list.map(s => (s.id === id ? { ...s, messages: msgs } : s))
    );
    this.saveSessions();
  }

  private saveSessions() {
    try {
      const payload = {
        sessions: this.sessions(),
        currentId: this.currentSessionId()
      };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
    } catch {
      // ignore storage errors
    }
  }

  private loadSessions(): { sessions: ChatSession[]; currentId: string } {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return { sessions: [], currentId: '' };
      const parsed = JSON.parse(raw);
      return {
        sessions: parsed.sessions || [],
        currentId: parsed.currentId || ''
      };
    } catch {
      return { sessions: [], currentId: '' };
    }
  }
}
