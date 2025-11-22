import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-model-selector',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './model-selector.html',
  styleUrls: ['./model-selector.css']
})
export class ModelSelector {
  @Input({ required: true }) models: string[] | null = null;
  @Input() selectedModel = '';
  @Input() onSelectModel!: (model: string) => void;

  select(model: string) {
    this.onSelectModel(model);
  }
}
