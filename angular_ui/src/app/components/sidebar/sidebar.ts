import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './sidebar.html',
  styleUrls: ['./sidebar.css']
})
export class Sidebar {
  @Input() models: string[] = [];
  @Input() selectedModel = '';
  @Input() onModelSelect!: (model: string) => void;

  select(model: string) {
    this.onModelSelect(model);
  }
}
