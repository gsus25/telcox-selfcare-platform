import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { CustomerUsage } from '../models/usage.model';

@Injectable({
  providedIn: 'root'
})
export class UsageApiService {
  private readonly apiUrl = 'http://localhost:5001/api';

  constructor(private readonly http: HttpClient) {}

  getCustomerUsage(customerId: string): Observable<CustomerUsage> {
    return this.http.get<CustomerUsage>(`${this.apiUrl}/customers/${customerId}/usage`);
  }
}