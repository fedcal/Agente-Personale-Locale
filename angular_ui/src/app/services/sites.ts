import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';

export interface SiteItem {
  id: number;
  url: string;
  note: string;
}

@Injectable({ providedIn: 'root' })
export class SitesService {
  private http = inject(HttpClient);
  // Try multiple bases (override, 127.0.0.1, localhost) to avoid host mismatch issues
  private bases: string[];
  private activeBase = '';

  constructor() {
    const override = (window as any).__ARES_API__;
    if (override) {
      this.bases = [override];
    } else {
      const protocol = window.location.protocol.startsWith('http') ? window.location.protocol : 'http:';
      const candidates = [`${protocol}//127.0.0.1:8000`, `${protocol}//localhost:8000`];
      // dedup while preserving order
      this.bases = Array.from(new Set(candidates));
    }
  }

  get baseUrl() {
    return this.activeBase || this.bases[0];
  }

  private async tryBases<T>(call: (base: string) => Promise<T>): Promise<T> {
    let lastErr: any;
    for (const base of this.bases) {
      try {
        const res = await call(base);
        this.activeBase = base;
        return res;
      } catch (err) {
        lastErr = err;
        continue;
      }
    }
    throw lastErr;
  }

  async list(): Promise<SiteItem[]> {
    return this.tryBases(async (base) => {
      try {
        return await firstValueFrom(this.http.get<SiteItem[]>(`${base}/sites`));
      } catch (err) {
        console.error('Errore caricamento siti:', err);
        throw err;
      }
    });
  }

  async add(url: string, note = ''): Promise<SiteItem | null> {
    return this.tryBases(async (base) => {
      try {
        return await firstValueFrom(this.http.post<SiteItem>(`${base}/sites`, { url, note }));
      } catch (err) {
        console.error('Errore aggiunta sito:', err);
        return null;
      }
    });
  }

  async remove(id: number): Promise<boolean> {
    return this.tryBases(async (base) => {
      try {
        const res = await firstValueFrom(this.http.delete<{ ok: boolean }>(`${base}/sites/${id}`));
        return !!res.ok;
      } catch (err) {
        console.error('Errore eliminazione sito:', err);
        return false;
      }
    });
  }

  async update(id: number, url: string, note = ''): Promise<SiteItem | null> {
    return this.tryBases(async (base) => {
      try {
        return await firstValueFrom(this.http.put<SiteItem>(`${base}/sites/${id}`, { url, note }));
      } catch (err) {
        console.error('Errore modifica sito:', err);
        return null;
      }
    });
  }
}
