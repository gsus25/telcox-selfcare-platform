export interface UsageBucket {
  used: number;
  total: number;
  unit: string;
  percentage: number;
}

export interface CustomerUsage {
  customerId: string;
  customerName: string;
  balance: number;
  dataUsage: UsageBucket;
  minutesUsage: UsageBucket;
  lastUpdated: string;
}