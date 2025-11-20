import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-sidebar',
  imports: [],
  templateUrl: './sidebar.html',
  styleUrl: './sidebar.css',
})
export class Sidebar {
  @Input() models: string[] = [];
  @Input() selectedModel: string = '';
  @Input() onSelect!: (model: string) => void;

  selectModel(model: string) {
    this.onSelect?.(model);
  }
}
