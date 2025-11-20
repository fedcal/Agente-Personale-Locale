import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-model-selector',
  imports: [CommonModule],
  templateUrl: './model-selector.html',
  styleUrl: './model-selector.css',
})
export class ModelSelector {
  @Input() models: string[] = [];
  @Input() selectedModel: string = '';
  @Input() onSelect!: (model: string) => void;

  selectModel(model: string) {
    this.onSelect?.(model);
  }

}
