import { Routes } from '@angular/router';
import { HomePage } from './pages/home/home';
import { AgentPage } from './pages/agent/agent';

export const routes: Routes = [
  { path: '', component: HomePage },
  { path: 'agent', component: AgentPage }
];
