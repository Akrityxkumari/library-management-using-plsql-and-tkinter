CREATE DATABASE librarymanagement;
USE librarymanagement;
CREATE TABLE Books (
 BookID INT AUTO_INCREMENT PRIMARY KEY,
 UID VARCHAR(50) NOT NULL,
 Title VARCHAR(255) NOT NULL,
 Status ENUM('Available', 'Issued') DEFAULT 'Available',
 LenderName VARCHAR(50),
 LendDate DATETIME,
 Semester VARCHAR(20)
);