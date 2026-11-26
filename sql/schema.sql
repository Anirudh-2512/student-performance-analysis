-- Schema for Student Performance Analysis (synthetic dataset)
-- Adjust types/ranges if your dataset differs.

DROP DATABASE IF EXISTS student_performance_db;
CREATE DATABASE student_performance_db;
USE student_performance_db;

DROP TABLE IF EXISTS students;
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    class_name VARCHAR(30) NOT NULL,
    gender VARCHAR(20),
    attendance_percentage DECIMAL(5,2) NOT NULL,
    mathematics_marks DECIMAL(5,2) NOT NULL,
    science_marks DECIMAL(5,2) NOT NULL,
    english_marks DECIMAL(5,2) NOT NULL,
    social_science_marks DECIMAL(5,2) NOT NULL,
    computer_marks DECIMAL(5,2) NOT NULL,
    CONSTRAINT chk_attendance CHECK (attendance_percentage BETWEEN 0 AND 100),
    CONSTRAINT chk_math CHECK (mathematics_marks BETWEEN 0 AND 100),
    CONSTRAINT chk_science CHECK (science_marks BETWEEN 0 AND 100),
    CONSTRAINT chk_english CHECK (english_marks BETWEEN 0 AND 100),
    CONSTRAINT chk_social_science CHECK (social_science_marks BETWEEN 0 AND 100),
    CONSTRAINT chk_computer CHECK (computer_marks BETWEEN 0 AND 100)
);

-- Example CSV import (adjust local path/permissions as needed):
-- LOAD DATA LOCAL INFILE 'data/raw/student_performance.csv'
-- INTO TABLE students
-- FIELDS TERMINATED BY ','
-- ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS
-- (student_id, student_name, class_name, gender, attendance_percentage,
--  mathematics_marks, science_marks, english_marks, social_science_marks, computer_marks);
