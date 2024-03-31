CREATE DATABASE attendance_system;

USE attendance_system;

CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
