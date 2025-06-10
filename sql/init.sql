-- Initialize database
CREATE DATABASE IF NOT EXISTS usha_database;

USE usha_database;

-- Create table
CREATE TABLE
    IF NOT EXISTS user_info (
        email VARCHAR(50) PRIMARY KEY,
        first_name VARCHAR(30) NOT NULL,
        last_name VARCHAR(30) NOT NULL,
        phone_number CHAR(10) NOT NULL,
        zipcode CHAR(5) NOT NULL,
        state CHAR(2) NOT NULL,
        accessed CHAR(1) NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

SELECT
    *
FROM
    user_info
LIMIT
    1;