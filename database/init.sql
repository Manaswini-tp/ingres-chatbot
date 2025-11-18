-- Create database and tables
CREATE DATABASE groundwater_db;

\c groundwater_db;

CREATE TABLE groundwater_data (
    id SERIAL PRIMARY KEY,
    state VARCHAR(100) NOT NULL,
    district VARCHAR(100) NOT NULL,
    year INTEGER NOT NULL,
    month VARCHAR(10) NOT NULL,
    groundwater_level DECIMAL(5,2) NOT NULL,
    water_quality VARCHAR(20) NOT NULL,
    rainfall DECIMAL(6,2) NOT NULL,
    category VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_groundwater_state ON groundwater_data(state);
CREATE INDEX idx_groundwater_district ON groundwater_data(district);
CREATE INDEX idx_groundwater_year ON groundwater_data(year);
CREATE INDEX idx_groundwater_state_district ON groundwater_data(state, district);