-- ============================================================================
-- Phase 4: Reference Data (Synthetic)
-- Project: Customs Revenue and Trade Volume Prediction Analytics Platform
-- Status: SYNTHETIC DATA ONLY - Privacy Clean
-- ============================================================================

-- ============================================================================
-- Port Reference Data (Generic Codes)
-- ============================================================================

INSERT INTO port_reference (port_code, port_name, port_type, region_code, country_code) VALUES
('PORT001', 'Customs Port Alpha', 'SEA', 'REGION01', 'XX'),
('PORT002', 'Customs Port Beta', 'SEA', 'REGION01', 'XX'),
('PORT003', 'Customs Port Gamma', 'AIR', 'REGION02', 'XX'),
('PORT004', 'Customs Port Delta', 'LAND', 'REGION02', 'XX'),
('PORT005', 'Customs Port Epsilon', 'SEA', 'REGION03', 'XX'),
('PORT006', 'Customs Port Zeta', 'AIR', 'REGION03', 'XX'),
('PORT007', 'Customs Port Eta', 'LAND', 'REGION04', 'XX'),
('PORT008', 'Customs Port Theta', 'RAIL', 'REGION04', 'XX'),
('PORT009', 'Customs Port Iota', 'SEA', 'REGION05', 'XX'),
('PORT010', 'Customs Port Kappa', 'AIR', 'REGION05', 'XX');

-- ============================================================================
-- Country Reference Data (ISO Codes)
-- ============================================================================

INSERT INTO country_reference (country_code, country_name, iso_alpha_3, region, wto_member, preferential_codes) VALUES
('AU', 'Australia', 'AUS', 'Asia-Pacific', TRUE, 'AUSFTA'),
('BD', 'Bangladesh', 'BGD', 'South Asia', TRUE, 'LDC'),
('BR', 'Brazil', 'BRA', 'South America', TRUE, 'MERCOSUR'),
('CA', 'Canada', 'CAN', 'North America', TRUE, 'CUSMA'),
('CN', 'China', 'CHN', 'East Asia', TRUE, 'RCEP'),
('DE', 'Germany', 'DEU', 'Europe', TRUE, 'EU'),
('FR', 'France', 'FRA', 'Europe', TRUE, 'EU'),
('GB', 'United Kingdom', 'GBR', 'Europe', TRUE, 'UKFTA'),
('ID', 'Indonesia', 'IDN', 'Southeast Asia', TRUE, 'ASEAN'),
('IN', 'India', 'IND', 'South Asia', TRUE, 'RCEP'),
('IT', 'Italy', 'ITA', 'Europe', TRUE, 'EU'),
('JP', 'Japan', 'JPN', 'East Asia', TRUE, 'RCEP'),
('KR', 'South Korea', 'KOR', 'East Asia', TRUE, 'RCEP'),
('MY', 'Malaysia', 'MYS', 'Southeast Asia', TRUE, 'ASEAN'),
('NL', 'Netherlands', 'NLD', 'Europe', TRUE, 'EU'),
('PH', 'Philippines', 'PHL', 'Southeast Asia', TRUE, 'ASEAN'),
('SG', 'Singapore', 'SGP', 'Southeast Asia', TRUE, 'ASEAN'),
('TH', 'Thailand', 'THA', 'Southeast Asia', TRUE, 'ASEAN'),
('TW', 'Taiwan', 'TWN', 'East Asia', FALSE, 'ATIGA'),
('US', 'United States', 'USA', 'North America', TRUE, 'CUSMA'),
('VN', 'Vietnam', 'VNM', 'Southeast Asia', TRUE, 'ASEAN');

-- ============================================================================
-- Currency Reference Data (ISO 4217)
-- ============================================================================

INSERT INTO currency_reference (currency_code, currency_name, currency_symbol, decimal_places) VALUES
('USD', 'United States Dollar', '

-- ============================================================================
-- HS Code Reference Data (Selected Common Codes)
-- ============================================================================

INSERT INTO hs_code_reference (hs_code, chapter, heading, subheading, description, mfn_duty_rate, preferential_rate, excise_applicable, excise_type, vat_category, vat_rate, unit_of_quantity) VALUES
-- Chapter 84 - Machinery
('8471300000', '84', '8471', '847130', 'Portable digital automatic data processing machines', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8517120000', '85', '8517', '851712', 'Telephones for cellular networks', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8471410000', '84', '8471', '847141', 'Data processing machines comprising in same housing', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8443320000', '84', '8443', '844332', 'Printing machinery; printers, printing by transfer', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8415100000', '84', '8415', '841510', 'Air conditioning machines, window or wall types', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),

-- Chapter 85 - Electrical Equipment
('8541400000', '85', '8541', '854140', 'Photosensitive semiconductor devices', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8517620000', '85', '8517', '851762', 'Machines for the reception of voice/images data', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8536500000', '85', '8536', '853650', 'Electrical switches for voltage not exceeding 1000V', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8528720000', '85', '8528', '852872', 'Reception apparatus for television', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),

-- Chapter 87 - Vehicles
('8703235010', '87', '8703', '870323', 'Motor cars with engine >1500cc but <=3000cc', 0.2500, 0.1500, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8704310000', '87', '8704', '870431', 'Motor vehicles for goods transport, diesel', 0.1000, 0.0500, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8711200000', '87', '8711', '871120', 'Motorcycles with engine >50cc but <=250cc', 0.3000, 0.2000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),

-- Chapter 62 - Textiles
('6204620000', '62', '6204', '620462', 'Womens trousers of cotton', 0.1675, 0.0000, FALSE, NULL, 'REDUCED', 0.0700, 'PCE'),
('6203420000', '62', '6203', '620342', 'Mens trousers of cotton', 0.1675, 0.0000, FALSE, NULL, 'REDUCED', 0.0700, 'PCE'),
('6110200000', '61', '6110', '611020', 'Pullovers of cotton', 0.1650, 0.0000, FALSE, NULL, 'REDUCED', 0.0700, 'PCE'),

-- Chapter 90 - Precision Instruments
('9021210000', '90', '9021', '902121', 'Artificial teeth', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('9018900000', '90', '9018', '901890', 'Instruments and appliances used in medical sciences', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('9031800000', '90', '9031', '903180', 'Measuring or checking instruments nesoi', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),

-- Chapter 94 - Furniture
('9403610000', '94', '9403', '940361', 'Wooden furniture for dining rooms', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('9401400000', '94', '9401', '940140', 'Seats, convertible into beds (not garden seats)', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),

-- Chapter 30 - Pharmaceutical
('3002150000', '30', '3002', '300215', 'Immunological products, unmixed', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.0000, 'PCE'),
('3004900000', '30', '3004', '300490', 'Medicaments nesoi, measured doses', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.0000, 'PCE'),

-- Chapter 39 - Plastics
('3926900000', '39', '3926', '392690', 'Articles of plastics nesoi', 0.0650, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('3923210000', '39', '3923', '392321', 'Sacks and bags of polymers of ethylene', 0.0650, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),

-- Chapter 48 - Paper
('4801000000', '48', '4801', '480100', 'Newsprint, in rolls or sheets', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'KGM'),
('4819100000', '48', '4819', '481910', 'Cartons and boxes of corrugated paper', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'KGM');

-- ============================================================================
-- Trader Reference Data (Synthetic Entities)
-- ============================================================================

-- Generate 100 synthetic traders
INSERT INTO trader_reference (trader_id, trader_type, region_code, entity_code, registration_number, registration_country, risk_category)
SELECT 
    'IMP-' || 
    LPAD((10000 + (gs.id % 90000))::VARCHAR, 5, '0') || '-' ||
    LPAD((1000000 + (gs.id * 7)::INTEGER % 9000000)::VARCHAR, 7, '0') AS trader_id,
    'IMPORTER' AS trader_type,
    'REGION' || LPAD((1 + (gs.id % 5))::VARCHAR, 2, '0') AS region_code,
    'ENT' || LPAD((gs.id % 1000)::VARCHAR, 3, '0') AS entity_code,
    'REG' || LPAD((100000 + gs.id)::VARCHAR, 6, '0') AS registration_number,
    'XX' AS registration_country,
    CASE 
        WHEN gs.id % 20 = 0 THEN 'HIGH'
        WHEN gs.id % 10 = 0 THEN 'ELEVATED'
        WHEN gs.id % 5 = 0 THEN 'LOW'
        ELSE 'STANDARD'
    END AS risk_category
FROM generate_series(1, 100) AS gs(id);

-- ============================================================================
-- Exchange Rate Seed Data (Synthetic - base rates)
-- ============================================================================

INSERT INTO exchange_rates (rate_date, from_currency, to_currency, rate_value)
SELECT 
    '2024-01-01'::DATE + (gs.id - 1) AS rate_date,
    'USD' AS from_currency,
    'USD' AS to_currency,
    1.000000 AS rate_value
FROM generate_series(1, 730) AS gs(id);

-- Update with synthetic exchange rates for other currencies
UPDATE exchange_rates SET rate_value = 0.670000 WHERE from_currency = 'EUR';
UPDATE exchange_rates SET rate_value = 0.006700 WHERE from_currency = 'JPY';
UPDATE exchange_rates SET rate_value = 0.138000 WHERE from_currency = 'CNY';
UPDATE exchange_rates SET rate_value = 1.270000 WHERE from_currency = 'GBP';
UPDATE exchange_rates SET rate_value = 0.028500 WHERE from_currency = 'THB';
UPDATE exchange_rates SET rate_value = 0.000740 WHERE from_currency = 'KRW';
UPDATE exchange_rates SET rate_value = 0.740000 WHERE from_currency = 'SGD';
UPDATE exchange_rates SET rate_value = 0.210000 WHERE from_currency = 'MYR';
UPDATE exchange_rates SET rate_value = 0.000063 WHERE from_currency = 'IDR';

-- Add some variation to exchange rates over time
UPDATE exchange_rates SET rate_value = rate_value * (1 + (random() - 0.5) * 0.02) 
WHERE from_currency != 'USD';

-- ============================================================================
-- End of Seed Data
-- ============================================================================, 2),
('EUR', 'Euro', '€', 2),
('JPY', 'Japanese Yen', '¥', 0),
('CNY', 'Chinese Yuan', '¥', 2),
('GBP', 'British Pound', '£', 2),
('THB', 'Thai Baht', '฿', 2),
('KRW', 'South Korean Won', '₩', 0),
('SGD', 'Singapore Dollar', '

-- ============================================================================
-- HS Code Reference Data (Selected Common Codes)
-- ============================================================================

INSERT INTO hs_code_reference (hs_code, chapter, heading, subheading, description, mfn_duty_rate, preferential_rate, excise_applicable, excise_type, vat_category, vat_rate, unit_of_quantity) VALUES
-- Chapter 84 - Machinery
('8471300000', '84', '8471', '847130', 'Portable digital automatic data processing machines', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8517120000', '85', '8517', '851712', 'Telephones for cellular networks', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8471410000', '84', '8471', '847141', 'Data processing machines comprising in same housing', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8443320000', '84', '8443', '844332', 'Printing machinery; printers, printing by transfer', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8415100000', '84', '8415', '841510', 'Air conditioning machines, window or wall types', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),

-- Chapter 85 - Electrical Equipment
('8541400000', '85', '8541', '854140', 'Photosensitive semiconductor devices', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8517620000', '85', '8517', '851762', 'Machines for the reception of voice/images data', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8536500000', '85', '8536', '853650', 'Electrical switches for voltage not exceeding 1000V', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8528720000', '85', '8528', '852872', 'Reception apparatus for television', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),

-- Chapter 87 - Vehicles
('8703235010', '87', '8703', '870323', 'Motor cars with engine >1500cc but <=3000cc', 0.2500, 0.1500, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8704310000', '87', '8704', '870431', 'Motor vehicles for goods transport, diesel', 0.1000, 0.0500, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8711200000', '87', '8711', '871120', 'Motorcycles with engine >50cc but <=250cc', 0.3000, 0.2000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),

-- Chapter 62 - Textiles
('6204620000', '62', '6204', '620462', 'Womens trousers of cotton', 0.1675, 0.0000, FALSE, NULL, 'REDUCED', 0.0700, 'PCE'),
('6203420000', '62', '6203', '620342', 'Mens trousers of cotton', 0.1675, 0.0000, FALSE, NULL, 'REDUCED', 0.0700, 'PCE'),
('6110200000', '61', '6110', '611020', 'Pullovers of cotton', 0.1650, 0.0000, FALSE, NULL, 'REDUCED', 0.0700, 'PCE'),

-- Chapter 90 - Precision Instruments
('9021210000', '90', '9021', '902121', 'Artificial teeth', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('9018900000', '90', '9018', '901890', 'Instruments and appliances used in medical sciences', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('9031800000', '90', '9031', '903180', 'Measuring or checking instruments nesoi', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),

-- Chapter 94 - Furniture
('9403610000', '94', '9403', '940361', 'Wooden furniture for dining rooms', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('9401400000', '94', '9401', '940140', 'Seats, convertible into beds (not garden seats)', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),

-- Chapter 30 - Pharmaceutical
('3002150000', '30', '3002', '300215', 'Immunological products, unmixed', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.0000, 'PCE'),
('3004900000', '30', '3004', '300490', 'Medicaments nesoi, measured doses', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.0000, 'PCE'),

-- Chapter 39 - Plastics
('3926900000', '39', '3926', '392690', 'Articles of plastics nesoi', 0.0650, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('3923210000', '39', '3923', '392321', 'Sacks and bags of polymers of ethylene', 0.0650, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),

-- Chapter 48 - Paper
('4801000000', '48', '4801', '480100', 'Newsprint, in rolls or sheets', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'KGM'),
('4819100000', '48', '4819', '481910', 'Cartons and boxes of corrugated paper', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'KGM');

-- ============================================================================
-- Trader Reference Data (Synthetic Entities)
-- ============================================================================

-- Generate 100 synthetic traders
INSERT INTO trader_reference (trader_id, trader_type, region_code, entity_code, registration_number, registration_country, risk_category)
SELECT 
    'IMP-' || 
    LPAD((10000 + (gs.id % 90000))::VARCHAR, 5, '0') || '-' ||
    LPAD((1000000 + (gs.id * 7)::INTEGER % 9000000)::VARCHAR, 7, '0') AS trader_id,
    'IMPORTER' AS trader_type,
    'REGION' || LPAD((1 + (gs.id % 5))::VARCHAR, 2, '0') AS region_code,
    'ENT' || LPAD((gs.id % 1000)::VARCHAR, 3, '0') AS entity_code,
    'REG' || LPAD((100000 + gs.id)::VARCHAR, 6, '0') AS registration_number,
    'XX' AS registration_country,
    CASE 
        WHEN gs.id % 20 = 0 THEN 'HIGH'
        WHEN gs.id % 10 = 0 THEN 'ELEVATED'
        WHEN gs.id % 5 = 0 THEN 'LOW'
        ELSE 'STANDARD'
    END AS risk_category
FROM generate_series(1, 100) AS gs(id);

-- ============================================================================
-- Exchange Rate Seed Data (Synthetic - base rates)
-- ============================================================================

INSERT INTO exchange_rates (rate_date, from_currency, to_currency, rate_value)
SELECT 
    '2024-01-01'::DATE + (gs.id - 1) AS rate_date,
    'USD' AS from_currency,
    'USD' AS to_currency,
    1.000000 AS rate_value
FROM generate_series(1, 730) AS gs(id);

-- Update with synthetic exchange rates for other currencies
UPDATE exchange_rates SET rate_value = 0.670000 WHERE from_currency = 'EUR';
UPDATE exchange_rates SET rate_value = 0.006700 WHERE from_currency = 'JPY';
UPDATE exchange_rates SET rate_value = 0.138000 WHERE from_currency = 'CNY';
UPDATE exchange_rates SET rate_value = 1.270000 WHERE from_currency = 'GBP';
UPDATE exchange_rates SET rate_value = 0.028500 WHERE from_currency = 'THB';
UPDATE exchange_rates SET rate_value = 0.000740 WHERE from_currency = 'KRW';
UPDATE exchange_rates SET rate_value = 0.740000 WHERE from_currency = 'SGD';
UPDATE exchange_rates SET rate_value = 0.210000 WHERE from_currency = 'MYR';
UPDATE exchange_rates SET rate_value = 0.000063 WHERE from_currency = 'IDR';

-- Add some variation to exchange rates over time
UPDATE exchange_rates SET rate_value = rate_value * (1 + (random() - 0.5) * 0.02) 
WHERE from_currency != 'USD';

-- ============================================================================
-- End of Seed Data
-- ============================================================================, 2),
('MYR', 'Malaysian Ringgit', 'RM', 2),
('IDR', 'Indonesian Rupiah', 'Rp', 0),
('AUD', 'Australian Dollar', '

-- ============================================================================
-- HS Code Reference Data (Selected Common Codes)
-- ============================================================================

INSERT INTO hs_code_reference (hs_code, chapter, heading, subheading, description, mfn_duty_rate, preferential_rate, excise_applicable, excise_type, vat_category, vat_rate, unit_of_quantity) VALUES
-- Chapter 84 - Machinery
('8471300000', '84', '8471', '847130', 'Portable digital automatic data processing machines', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8517120000', '85', '8517', '851712', 'Telephones for cellular networks', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8471410000', '84', '8471', '847141', 'Data processing machines comprising in same housing', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8443320000', '84', '8443', '844332', 'Printing machinery; printers, printing by transfer', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8415100000', '84', '8415', '841510', 'Air conditioning machines, window or wall types', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),

-- Chapter 85 - Electrical Equipment
('8541400000', '85', '8541', '854140', 'Photosensitive semiconductor devices', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8517620000', '85', '8517', '851762', 'Machines for the reception of voice/images data', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8536500000', '85', '8536', '853650', 'Electrical switches for voltage not exceeding 1000V', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8528720000', '85', '8528', '852872', 'Reception apparatus for television', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),

-- Chapter 87 - Vehicles
('8703235010', '87', '8703', '870323', 'Motor cars with engine >1500cc but <=3000cc', 0.2500, 0.1500, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8704310000', '87', '8704', '870431', 'Motor vehicles for goods transport, diesel', 0.1000, 0.0500, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8711200000', '87', '8711', '871120', 'Motorcycles with engine >50cc but <=250cc', 0.3000, 0.2000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),

-- Chapter 62 - Textiles
('6204620000', '62', '6204', '620462', 'Womens trousers of cotton', 0.1675, 0.0000, FALSE, NULL, 'REDUCED', 0.0700, 'PCE'),
('6203420000', '62', '6203', '620342', 'Mens trousers of cotton', 0.1675, 0.0000, FALSE, NULL, 'REDUCED', 0.0700, 'PCE'),
('6110200000', '61', '6110', '611020', 'Pullovers of cotton', 0.1650, 0.0000, FALSE, NULL, 'REDUCED', 0.0700, 'PCE'),

-- Chapter 90 - Precision Instruments
('9021210000', '90', '9021', '902121', 'Artificial teeth', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('9018900000', '90', '9018', '901890', 'Instruments and appliances used in medical sciences', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('9031800000', '90', '9031', '903180', 'Measuring or checking instruments nesoi', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),

-- Chapter 94 - Furniture
('9403610000', '94', '9403', '940361', 'Wooden furniture for dining rooms', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('9401400000', '94', '9401', '940140', 'Seats, convertible into beds (not garden seats)', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),

-- Chapter 30 - Pharmaceutical
('3002150000', '30', '3002', '300215', 'Immunological products, unmixed', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.0000, 'PCE'),
('3004900000', '30', '3004', '300490', 'Medicaments nesoi, measured doses', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.0000, 'PCE'),

-- Chapter 39 - Plastics
('3926900000', '39', '3926', '392690', 'Articles of plastics nesoi', 0.0650, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('3923210000', '39', '3923', '392321', 'Sacks and bags of polymers of ethylene', 0.0650, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),

-- Chapter 48 - Paper
('4801000000', '48', '4801', '480100', 'Newsprint, in rolls or sheets', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'KGM'),
('4819100000', '48', '4819', '481910', 'Cartons and boxes of corrugated paper', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'KGM');

-- ============================================================================
-- Trader Reference Data (Synthetic Entities)
-- ============================================================================

-- Generate 100 synthetic traders
INSERT INTO trader_reference (trader_id, trader_type, region_code, entity_code, registration_number, registration_country, risk_category)
SELECT 
    'IMP-' || 
    LPAD((10000 + (gs.id % 90000))::VARCHAR, 5, '0') || '-' ||
    LPAD((1000000 + (gs.id * 7)::INTEGER % 9000000)::VARCHAR, 7, '0') AS trader_id,
    'IMPORTER' AS trader_type,
    'REGION' || LPAD((1 + (gs.id % 5))::VARCHAR, 2, '0') AS region_code,
    'ENT' || LPAD((gs.id % 1000)::VARCHAR, 3, '0') AS entity_code,
    'REG' || LPAD((100000 + gs.id)::VARCHAR, 6, '0') AS registration_number,
    'XX' AS registration_country,
    CASE 
        WHEN gs.id % 20 = 0 THEN 'HIGH'
        WHEN gs.id % 10 = 0 THEN 'ELEVATED'
        WHEN gs.id % 5 = 0 THEN 'LOW'
        ELSE 'STANDARD'
    END AS risk_category
FROM generate_series(1, 100) AS gs(id);

-- ============================================================================
-- Exchange Rate Seed Data (Synthetic - base rates)
-- ============================================================================

INSERT INTO exchange_rates (rate_date, from_currency, to_currency, rate_value)
SELECT 
    '2024-01-01'::DATE + (gs.id - 1) AS rate_date,
    'USD' AS from_currency,
    'USD' AS to_currency,
    1.000000 AS rate_value
FROM generate_series(1, 730) AS gs(id);

-- Update with synthetic exchange rates for other currencies
UPDATE exchange_rates SET rate_value = 0.670000 WHERE from_currency = 'EUR';
UPDATE exchange_rates SET rate_value = 0.006700 WHERE from_currency = 'JPY';
UPDATE exchange_rates SET rate_value = 0.138000 WHERE from_currency = 'CNY';
UPDATE exchange_rates SET rate_value = 1.270000 WHERE from_currency = 'GBP';
UPDATE exchange_rates SET rate_value = 0.028500 WHERE from_currency = 'THB';
UPDATE exchange_rates SET rate_value = 0.000740 WHERE from_currency = 'KRW';
UPDATE exchange_rates SET rate_value = 0.740000 WHERE from_currency = 'SGD';
UPDATE exchange_rates SET rate_value = 0.210000 WHERE from_currency = 'MYR';
UPDATE exchange_rates SET rate_value = 0.000063 WHERE from_currency = 'IDR';

-- Add some variation to exchange rates over time
UPDATE exchange_rates SET rate_value = rate_value * (1 + (random() - 0.5) * 0.02) 
WHERE from_currency != 'USD';

-- ============================================================================
-- End of Seed Data
-- ============================================================================, 2),
('INR', 'Indian Rupee', '₹', 2),
('PHP', 'Philippine Peso', '₱', 2),
('VND', 'Vietnamese Dong', '₫', 0),
('KHR', 'Cambodian Riel', '៛', 0);

-- ============================================================================
-- HS Code Reference Data (Selected Common Codes)
-- ============================================================================

INSERT INTO hs_code_reference (hs_code, chapter, heading, subheading, description, mfn_duty_rate, preferential_rate, excise_applicable, excise_type, vat_category, vat_rate, unit_of_quantity) VALUES
-- Chapter 84 - Machinery
('8471300000', '84', '8471', '847130', 'Portable digital automatic data processing machines', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8517120000', '85', '8517', '851712', 'Telephones for cellular networks', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8471410000', '84', '8471', '847141', 'Data processing machines comprising in same housing', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8443320000', '84', '8443', '844332', 'Printing machinery; printers, printing by transfer', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8415100000', '84', '8415', '841510', 'Air conditioning machines, window or wall types', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),

-- Chapter 85 - Electrical Equipment
('8541400000', '85', '8541', '854140', 'Photosensitive semiconductor devices', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8517620000', '85', '8517', '851762', 'Machines for the reception of voice/images data', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8536500000', '85', '8536', '853650', 'Electrical switches for voltage not exceeding 1000V', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8528720000', '85', '8528', '852872', 'Reception apparatus for television', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),

-- Chapter 87 - Vehicles
('8703235010', '87', '8703', '870323', 'Motor cars with engine >1500cc but <=3000cc', 0.2500, 0.1500, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8704310000', '87', '8704', '870431', 'Motor vehicles for goods transport, diesel', 0.1000, 0.0500, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('8711200000', '87', '8711', '871120', 'Motorcycles with engine >50cc but <=250cc', 0.3000, 0.2000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),

-- Chapter 62 - Textiles
('6204620000', '62', '6204', '620462', 'Womens trousers of cotton', 0.1675, 0.0000, FALSE, NULL, 'REDUCED', 0.0700, 'PCE'),
('6203420000', '62', '6203', '620342', 'Mens trousers of cotton', 0.1675, 0.0000, FALSE, NULL, 'REDUCED', 0.0700, 'PCE'),
('6110200000', '61', '6110', '611020', 'Pullovers of cotton', 0.1650, 0.0000, FALSE, NULL, 'REDUCED', 0.0700, 'PCE'),

-- Chapter 90 - Precision Instruments
('9021210000', '90', '9021', '902121', 'Artificial teeth', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('9018900000', '90', '9018', '901890', 'Instruments and appliances used in medical sciences', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('9031800000', '90', '9031', '903180', 'Measuring or checking instruments nesoi', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),

-- Chapter 94 - Furniture
('9403610000', '94', '9403', '940361', 'Wooden furniture for dining rooms', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('9401400000', '94', '9401', '940140', 'Seats, convertible into beds (not garden seats)', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),

-- Chapter 30 - Pharmaceutical
('3002150000', '30', '3002', '300215', 'Immunological products, unmixed', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.0000, 'PCE'),
('3004900000', '30', '3004', '300490', 'Medicaments nesoi, measured doses', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.0000, 'PCE'),

-- Chapter 39 - Plastics
('3926900000', '39', '3926', '392690', 'Articles of plastics nesoi', 0.0650, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),
('3923210000', '39', '3923', '392321', 'Sacks and bags of polymers of ethylene', 0.0650, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'PCE'),

-- Chapter 48 - Paper
('4801000000', '48', '4801', '480100', 'Newsprint, in rolls or sheets', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'KGM'),
('4819100000', '48', '4819', '481910', 'Cartons and boxes of corrugated paper', 0.0000, 0.0000, FALSE, NULL, 'STANDARD', 0.1700, 'KGM');

-- ============================================================================
-- Trader Reference Data (Synthetic Entities)
-- ============================================================================

-- Generate 100 synthetic traders
INSERT INTO trader_reference (trader_id, trader_type, region_code, entity_code, registration_number, registration_country, risk_category)
SELECT 
    'IMP-' || 
    LPAD((10000 + (gs.id % 90000))::VARCHAR, 5, '0') || '-' ||
    LPAD((1000000 + (gs.id * 7)::INTEGER % 9000000)::VARCHAR, 7, '0') AS trader_id,
    'IMPORTER' AS trader_type,
    'REGION' || LPAD((1 + (gs.id % 5))::VARCHAR, 2, '0') AS region_code,
    'ENT' || LPAD((gs.id % 1000)::VARCHAR, 3, '0') AS entity_code,
    'REG' || LPAD((100000 + gs.id)::VARCHAR, 6, '0') AS registration_number,
    'XX' AS registration_country,
    CASE 
        WHEN gs.id % 20 = 0 THEN 'HIGH'
        WHEN gs.id % 10 = 0 THEN 'ELEVATED'
        WHEN gs.id % 5 = 0 THEN 'LOW'
        ELSE 'STANDARD'
    END AS risk_category
FROM generate_series(1, 100) AS gs(id);

-- ============================================================================
-- Exchange Rate Seed Data (Synthetic - base rates)
-- ============================================================================

INSERT INTO exchange_rates (rate_date, from_currency, to_currency, rate_value)
SELECT 
    '2024-01-01'::DATE + (gs.id - 1) AS rate_date,
    'USD' AS from_currency,
    'USD' AS to_currency,
    1.000000 AS rate_value
FROM generate_series(1, 730) AS gs(id);

-- Update with synthetic exchange rates for other currencies
UPDATE exchange_rates SET rate_value = 0.670000 WHERE from_currency = 'EUR';
UPDATE exchange_rates SET rate_value = 0.006700 WHERE from_currency = 'JPY';
UPDATE exchange_rates SET rate_value = 0.138000 WHERE from_currency = 'CNY';
UPDATE exchange_rates SET rate_value = 1.270000 WHERE from_currency = 'GBP';
UPDATE exchange_rates SET rate_value = 0.028500 WHERE from_currency = 'THB';
UPDATE exchange_rates SET rate_value = 0.000740 WHERE from_currency = 'KRW';
UPDATE exchange_rates SET rate_value = 0.740000 WHERE from_currency = 'SGD';
UPDATE exchange_rates SET rate_value = 0.210000 WHERE from_currency = 'MYR';
UPDATE exchange_rates SET rate_value = 0.000063 WHERE from_currency = 'IDR';

-- Add some variation to exchange rates over time
UPDATE exchange_rates SET rate_value = rate_value * (1 + (random() - 0.5) * 0.02) 
WHERE from_currency != 'USD';

-- ============================================================================
-- End of Seed Data
-- ============================================================================