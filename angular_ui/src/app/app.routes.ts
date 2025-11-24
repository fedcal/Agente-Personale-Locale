import { Routes } from '@angular/router';
import { HomePage } from './pages/home/home';
import { AgentPage } from './pages/agent/agent';
import { SitesPage } from './pages/sites/sites';

export const routes: Routes = [
  { path: '', component: HomePage },
  { path: 'agent', component: AgentPage },
  { path: 'sites', component: SitesPage }
];
