import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';

import { UsageApiService } from './usage-api.service';
import { CustomerUsage } from '../models/usage.model';

describe('UsageApiService', () => {
  let service: UsageApiService;
  let httpMock: HttpTestingController;

  const mockUsage: CustomerUsage = {
    customerId: '1001',
    customerName: 'Ana Torres',
    balance: 18.75,
    dataUsage: {
      used: 7.2,
      total: 20,
      unit: 'GB',
      percentage: 36
    },
    minutesUsage: {
      used: 320,
      total: 1000,
      unit: 'minutes',
      percentage: 32
    },
    lastUpdated: '2026-06-19T16:30:00+00:00'
  };

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        UsageApiService,
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    });

    service = TestBed.inject(UsageApiService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should request customer usage from the backend API', () => {
    service.getCustomerUsage('1001').subscribe((usage) => {
      expect(usage).toEqual(mockUsage);
      expect(usage.customerName).toBe('Ana Torres');
      expect(usage.dataUsage.percentage).toBe(36);
      expect(usage.minutesUsage.percentage).toBe(32);
    });

    const request = httpMock.expectOne('http://localhost:5001/api/customers/1001/usage');

    expect(request.request.method).toBe('GET');

    request.flush(mockUsage);
  });
});