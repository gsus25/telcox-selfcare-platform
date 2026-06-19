import { HttpErrorResponse } from '@angular/common/http';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { throwError } from 'rxjs';

import { UsageApiService } from '../../services/usage-api.service';
import { UsageDashboardComponent } from './usage-dashboard.component';

describe('UsageDashboardComponent', () => {
  let fixture: ComponentFixture<UsageDashboardComponent>;

  const usageApiServiceMock = {
    getCustomerUsage: jasmine.createSpy('getCustomerUsage')
  };

  beforeEach(async () => {
    usageApiServiceMock.getCustomerUsage.calls.reset();

    await TestBed.configureTestingModule({
      imports: [UsageDashboardComponent],
      providers: [
        {
          provide: UsageApiService,
          useValue: usageApiServiceMock
        }
      ]
    }).compileComponents();
  });

  it('should show a friendly message when the backend is unavailable', () => {
    usageApiServiceMock.getCustomerUsage.and.returnValue(
      throwError(() => new HttpErrorResponse({ status: 0 }))
    );

    fixture = TestBed.createComponent(UsageDashboardComponent);
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;

    expect(compiled.textContent).toContain('No pudimos cargar la información.');
    expect(compiled.textContent).toContain('No pudimos conectar con el backend');
  });
});