import { Component } from '@angular/core';

import { UsageDashboardComponent } from './features/usage/pages/usage-dashboard/usage-dashboard.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [UsageDashboardComponent],
  template: '<app-usage-dashboard />'
})
export class AppComponent {}