-- Metro Route Planner MySQL Schema & Seed Data
CREATE DATABASE IF NOT EXISTS metro_db;
USE metro_db;

-- Table 1: Stations
DROP TABLE IF EXISTS connections;
DROP TABLE IF EXISTS search_history;
DROP TABLE IF EXISTS stations;

CREATE TABLE stations (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    line VARCHAR(50) NOT NULL,
    x_pos INT DEFAULT 0,
    y_pos INT DEFAULT 0
);

-- Table 2: Connections (Graph Edges)
CREATE TABLE connections (
    id INT AUTO_INCREMENT PRIMARY KEY,
    station_a VARCHAR(100) NOT NULL,
    station_b VARCHAR(100) NOT NULL,
    distance DECIMAL(5,2) NOT NULL,
    line VARCHAR(50) NOT NULL,
    FOREIGN KEY (station_a) REFERENCES stations(name) ON DELETE CASCADE,
    FOREIGN KEY (station_b) REFERENCES stations(name) ON DELETE CASCADE
);

-- Table 3: Search History
CREATE TABLE search_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    algorithm VARCHAR(50) NOT NULL,
    distance DECIMAL(5,2) NOT NULL,
    stops INT NOT NULL,
    searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Seed Data: Stations (Purple, Green, Yellow lines)
INSERT INTO stations (id, name, line, x_pos, y_pos) VALUES
(101, 'Kengeri', 'Purple', 100, 400),
(102, 'Vijayanagar', 'Purple', 250, 400),
(103, 'City Railway Stn', 'Purple', 380, 400),
(104, 'Majestic', 'Interchange', 500, 400),
(105, 'Cubbon Park', 'Purple', 620, 400),
(106, 'MG Road', 'Purple', 740, 400),
(107, 'Trinity', 'Purple', 860, 400),
(108, 'Indiranagar', 'Purple', 980, 400),
(109, 'Baiyappanahalli', 'Purple', 1100, 400),

(201, 'Yeshwanthpur', 'Green', 500, 100),
(202, 'Rajajinagar', 'Green', 500, 200),
(203, 'Sampige Road', 'Green', 500, 300),
(204, 'Chikpet', 'Green', 500, 500),
(205, 'National College', 'Green', 500, 600),
(206, 'Jayanagar', 'Green', 500, 700),
(207, 'Silk Institute', 'Green', 500, 800),

(301, 'Electronic City', 'Yellow', 860, 700),
(302, 'BTM Layout', 'Yellow', 700, 600);

-- Seed Data: Connections
INSERT INTO connections (station_a, station_b, distance, line) VALUES
('Kengeri', 'Vijayanagar', 6.5, 'Purple'),
('Vijayanagar', 'City Railway Stn', 4.2, 'Purple'),
('City Railway Stn', 'Majestic', 1.2, 'Purple'),
('Majestic', 'Cubbon Park', 2.0, 'Purple'),
('Cubbon Park', 'MG Road', 1.0, 'Purple'),
('MG Road', 'Trinity', 1.5, 'Purple'),
('Trinity', 'Indiranagar', 1.7, 'Purple'),
('Indiranagar', 'Baiyappanahalli', 2.3, 'Purple'),

('Yeshwanthpur', 'Rajajinagar', 3.8, 'Green'),
('Rajajinagar', 'Sampige Road', 2.4, 'Green'),
('Sampige Road', 'Majestic', 1.5, 'Green'),
('Majestic', 'Chikpet', 1.8, 'Green'),
('Chikpet', 'National College', 2.1, 'Green'),
('National College', 'Jayanagar', 3.0, 'Green'),
('Jayanagar', 'Silk Institute', 5.4, 'Green'),

('Trinity', 'BTM Layout', 5.2, 'Yellow'),
('BTM Layout', 'Electronic City', 8.5, 'Yellow'),
('National College', 'BTM Layout', 4.1, 'Yellow');
