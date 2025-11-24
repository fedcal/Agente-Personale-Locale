import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SiteItem } from '../../services/sites';

@Component({
  selector: 'app-sites-config',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './sites-config.html',
  styleUrls: ['./sites-config.css']
})
export class SitesConfig {
  @Input() sites: SiteItem[] = [];
  @Input() loading = false;
  @Input() error = '';
  @Input() apiBase = '';
  @Output() onAdd = new EventEmitter<{ url: string; note: string }>();
  @Output() onDelete = new EventEmitter<number>();
  @Output() onReload = new EventEmitter<void>();
  @Output() onUpdate = new EventEmitter<{ id: number; url: string; note: string }>();

  url = '';
  note = '';
  editId: number | null = null;
  editUrl = '';
  editNote = '';

  add() {
    const u = this.url.trim();
    if (!u) return;
    this.onAdd.emit({ url: u, note: this.note.trim() });
    this.url = '';
    this.note = '';
  }

  remove(id: number) {
    this.onDelete.emit(id);
  }

  reload() {
    this.onReload.emit();
  }

  startEdit(site: SiteItem) {
    this.editId = site.id;
    this.editUrl = site.url;
    this.editNote = site.note || '';
  }

  cancelEdit() {
    this.editId = null;
    this.editUrl = '';
    this.editNote = '';
  }

  saveEdit() {
    if (this.editId == null) return;
    const url = this.editUrl.trim();
    if (!url) return;
    this.onUpdate.emit({ id: this.editId, url, note: this.editNote.trim() });
    this.cancelEdit();
  }
}
