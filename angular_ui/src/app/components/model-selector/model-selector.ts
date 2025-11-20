import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-model-selector',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './model-selector.html',
  styleUrls: ['./model-selector.css']
})
export class ModelSelector {
  @Input() models: string[] = [];
  @Input() selectedModel = '';
  @Input() onSelectModel!: (model: string) => void;

  select(model: string) {
    this.onSelectModel(model);
  }
}
