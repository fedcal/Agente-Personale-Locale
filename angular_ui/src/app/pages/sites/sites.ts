import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SitesConfig } from '../../components/sites-config/sites-config';
import { SitesService, SiteItem } from '../../services/sites';
import { AgentUi } from '../../components/agent-ui/agent-ui';
import { Router } from '@angular/router';

@Component({
  selector: 'app-sites',
  standalone: true,
  imports: [CommonModule, SitesConfig, AgentUi],
  templateUrl: './sites.html',
  styleUrls: ['./sites.css']
})
export class SitesPage implements OnInit {
  private sitesSvc = inject(SitesService);
  protected router = inject(Router);
  sites: SiteItem[] = [];
  loading = false;
  error = '';
  apiBase = this.sitesSvc.baseUrl;

  async ngOnInit() {
    await this.load();
  }

  async load() {
    this.loading = true;
    this.error = '';
    try {
      this.sites = await this.sitesSvc.list();
      this.apiBase = this.sitesSvc.baseUrl;
    } catch {
      this.sites = [];
      this.error = 'Errore nel caricamento dei siti. Verifica che l\'API sia raggiungibile (porta 8000).';
    } finally {
      this.loading = false;
    }
  }

  async addSite(url: string, note: string) {
    const res = await this.sitesSvc.add(url, note);
    if (res) {
      this.sites = [res, ...this.sites.filter((s) => s.id !== res.id)];
    }
  }

  async updateSite(id: number, url: string, note: string) {
    const res = await this.sitesSvc.update(id, url, note);
    if (res) {
      this.sites = this.sites.map((s) => (s.id === id ? res : s));
      this.error = '';
    } else {
      this.error = 'Non è stato possibile aggiornare il sito (URL duplicato o API non raggiungibile).';
    }
  }

  async deleteSite(id: number) {
    const ok = await this.sitesSvc.remove(id);
    if (ok) {
      this.sites = this.sites.filter((s) => s.id !== id);
    }
  }
}
