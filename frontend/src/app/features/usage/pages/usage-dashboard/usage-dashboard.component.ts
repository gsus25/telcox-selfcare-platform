import { CommonModule, DatePipe, DecimalPipe } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { finalize } from 'rxjs';

import { CustomerUsage, UsageBucket } from '../../models/usage.model';
import { UsageApiService } from '../../services/usage-api.service';

@Component({
  selector: 'app-usage-dashboard',
  standalone: true,
  imports: [CommonModule, DatePipe, DecimalPipe],
  templateUrl: './usage-dashboard.component.html',
  styleUrl: './usage-dashboard.component.css'
})
export class UsageDashboardComponent implements OnInit {
  private readonly customerId = '1001';

  usage: CustomerUsage | null = null;
  isLoading = false;
  errorMessage = '';

  constructor(private readonly usageApiService: UsageApiService) {}

  ngOnInit(): void {
    this.loadUsage();
  }

  loadUsage(): void {
    this.isLoading = true;
    this.errorMessage = '';

    this.usageApiService
      .getCustomerUsage(this.customerId)
      .pipe(finalize(() => {
        this.isLoading = false;
      }))
      .subscribe({
        next: (usage) => {
          this.usage = usage;
        },
        error: (error: HttpErrorResponse) => {
          this.usage = null;
          this.errorMessage = this.getFriendlyErrorMessage(error);
        }
      });
  }


  getRemaining(bucket: UsageBucket): number {
    return Math.max(bucket.total - bucket.used, 0);
  }

  getProgressBarClass(percentage: number): string {
    if (percentage >= 90) {
      return 'bg-danger';
    }

    if (percentage >= 75) {
      return 'bg-warning';
    }

    return 'bg-success';
  }

  private getFriendlyErrorMessage(error: HttpErrorResponse): string {
    if (error.status === 0) {
      return 'No pudimos conectar con el backend. Verifica que el servicio esté encendido e intenta nuevamente.';
    }

    if (error.status === 404) {
      return 'No encontramos información de consumo para el cliente seleccionado.';
    }

    if (error.status >= 500) {
      return 'El sistema de consulta de consumo no está disponible temporalmente. Intenta nuevamente en unos minutos.';
    }

    return 'Ocurrió un problema inesperado al consultar tu consumo.';
  }
}