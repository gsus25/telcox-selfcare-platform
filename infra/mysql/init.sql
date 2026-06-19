CREATE TABLE IF NOT EXISTS customer_usage (
  customer_id VARCHAR(20) PRIMARY KEY,
  customer_name VARCHAR(120) NOT NULL,
  balance DECIMAL(10, 2) NOT NULL,
  data_used DECIMAL(10, 2) NOT NULL,
  data_total DECIMAL(10, 2) NOT NULL,
  minutes_used INT NOT NULL,
  minutes_total INT NOT NULL,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO customer_usage (
  customer_id,
  customer_name,
  balance,
  data_used,
  data_total,
  minutes_used,
  minutes_total
) VALUES
  ('1001', 'Ana Torres', 18.75, 7.20, 20.00, 320, 1000),
  ('1002', 'Carlos Mejia', 5.40, 18.60, 20.00, 870, 1000)
ON DUPLICATE KEY UPDATE
  customer_name = VALUES(customer_name),
  balance = VALUES(balance),
  data_used = VALUES(data_used),
  data_total = VALUES(data_total),
  minutes_used = VALUES(minutes_used),
  minutes_total = VALUES(minutes_total);