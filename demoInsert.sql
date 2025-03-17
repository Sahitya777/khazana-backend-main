-- Insert into mutual_funds
INSERT INTO mutual_funds (id, name, isin, nav) VALUES
(1, 'ICICI Prudential Bluechip Fund', 'INF109K016L0', 100),
(2, 'HDFC Top 100 Fund', 'INF179K01YV8', 100),
(3, 'SBI Bluechip Fund', 'INF200K01QX4', 100),
(4, 'Axis Bluechip Fund', 'INF846K01DP8', 100),
(5, 'Mirae Asset Large Cap Fund', 'INF769K01AX2', 100);

-- Insert into investments
INSERT INTO investments (mutual_fund_id, investment_date, amount_invested, nav_at_investment, returns_percentage) VALUES
(1, '2023-01-10', 1000000, 100, 12.5),
(2, '2022-12-05', 800000, 100, 10.2),
(3, '2023-02-15', 1200000, 100, 11.0),
(4, '2022-11-20', 950000, 100, 9.8),
(5, '2023-03-01', 1100000, 100, 13.0);

-- Insert into allocations
INSERT INTO allocations (mutual_fund_id, mutualfund_name, sector_allocation, stock_allocation, market_cap_allocation) VALUES
(1, 'ICICI Prudential Bluechip Fund', '{"IT": 38, "Financials": 37, "Energy/Conglomerate": 25}', '{"Reliance Industries": 25, "HDFC Bank": 22, "TCS": 20, "Infosys": 18, "ICICI Bank": 15}', '{"Large Cap": 98, "Mid Cap": 2, "Small Cap": 0}'),
(2, 'HDFC Top 100 Fund', '{"Financials": 80, "Energy/Conglomerate": 20}', '{"HDFC Bank": 28, "ICICI Bank": 24, "Reliance Industries": 20, "Kotak Mahindra Bank": 18, "Bajaj Finance": 10}', '{"Large Cap": 85, "Mid Cap": 13, "Small Cap": 2}'),
(3, 'SBI Bluechip Fund', '{"Energy/Conglomerate": 27, "IT": 40, "Financials": 21, "Industrials": 12}', '{"Reliance Industries": 27, "TCS": 23, "HDFC Bank": 21, "Infosys": 17, "Larsen & Toubro": 12}', '{"Large Cap": 97, "Mid Cap": 3, "Small Cap": 0}'),
(4, 'Axis Bluechip Fund', '{"IT": 50, "Financials": 32, "Energy/Conglomerate": 18}', '{"TCS": 26, "Infosys": 24, "HDFC Bank": 22, "Reliance Industries": 18, "State Bank of India (SBI)": 10}', '{"Large Cap": 98, "Mid Cap": 2, "Small Cap": 0}'),
(5, 'Mirae Asset Large Cap Fund', '{"IT": 42, "Financials": 34, "Energy/Conglomerate": 24}', '{"Reliance Industries": 24, "HDFC Bank": 23, "TCS": 22, "Infosys": 20, "ICICI Bank": 11}', '{"Large Cap": 96, "Mid Cap": 4, "Small Cap": 0}');

-- Insert into overlaps
-- Insert into overlaps
INSERT INTO "overlaps" (id, fund_1_id, fund_2_id, overlap_percentage) VALUES
(1, 1, 2, 67.0),
(2, 1, 3, 87.0),
(3, 1, 4, 88.0),
(4, 1, 5, 100.0),
(5, 2, 3, 48.0),
(6, 2, 4, 44.0),
(7, 2, 5, 65.0),
(8, 3, 4, 89.0),
(9, 3, 5, 89.0),
(10, 4, 5, 90.0);


