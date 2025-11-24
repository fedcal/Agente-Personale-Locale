import { NgModule } from '@angular/core';
import { LucideAngularModule, Settings, Home } from 'lucide-angular';

export const ICONS = {
  Settings,
  Home,
};

@NgModule({
  imports: [LucideAngularModule.pick(ICONS)],
  exports: [LucideAngularModule],
})
export class IconModule {}
