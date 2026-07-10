CREATE DATABASE IF NOT EXISTS library_stats;
USE library_stats;

CREATE TABLE IF NOT EXISTS segmen_mata (
    user VARCHAR(50) PRIMARY KEY,
    points INT NOT NULL DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO segmen_mata (user, points) VALUES 
('Adeena', 0), ('Mastura', 0), ('Azra', 0),
('Aina', 0), ('Fasihah', 0), ('Irdina', 0);

SELECT * FROM segmen_mata;
