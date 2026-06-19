import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of } from 'rxjs';

import { AppComponent } from './app.component';
import { UsageApiService } from './features/usage/services/usage-api.service';

describe('AppComponent', () => {
  let fixture: ComponentFixture<AppComponent>;

  const usageApiServiceMock = {
    getCustomerUsage: jasmine.createSpy('getCustomerUsage').and.returnValue(
      of({
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
      })
    )
  };

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AppComponent],
      providers: [
        {
          provide: UsageApiService,
          useValue: usageApiServiceMock
        }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(AppComponent);
    fixture.detectChanges();
  });

  it('should create the app shell', () => {
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });
});