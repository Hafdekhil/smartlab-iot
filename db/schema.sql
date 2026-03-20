CREATE DATABASE IF NOT EXISTS smartlab;
USE smartlab;

CREATE TABLE IF NOT EXISTS telemetry (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device VARCHAR(50),
    topic VARCHAR(255),
    value FLOAT,
    unit VARCHAR(10),
    ts_utc VARCHAR(40),
    INDEX idx_telemetry_device_ts (device, ts_utc)
);

CREATE TABLE IF NOT EXISTS events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device VARCHAR(50),
    topic VARCHAR(255),
    payload TEXT,
    ts_utc VARCHAR(40),
    INDEX idx_events_device_ts (device, ts_utc)
);
