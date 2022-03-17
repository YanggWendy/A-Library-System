DROP database ALS;

CREATE database ALS;
USE ALS;

CREATE TABLE Faculty(
     FacultyID INT AUTO_INCREMENT,
     FacultyName VARCHAR(20) UNIQUE,
	 PRIMARY KEY(FacultyID)); 
     
CREATE TABLE Author(
     AuthorID INT AUTO_INCREMENT,
     FirstName VARCHAR(20),
     LastName VARCHAR(20),
	 PRIMARY KEY(AuthorID)); 

CREATE TABLE Member(
     MemberID CHAR(10),
     FirstName VARCHAR(25),
     LastName VARCHAR(25),
     FacultyID INT,
     PhoneNo VARCHAR(10),
	 Email VARCHAR(25),
     FineAmount SMALLINT NOT NULL DEFAULT 0,
	 PRIMARY KEY(MemberID),
     FOREIGN KEY(FacultyID) REFERENCES Faculty(FacultyID)); 
     
CREATE TABLE Book(
     AccessionNumber CHAR(5),
     Title VARCHAR(100),
	 ISBN CHAR(13),
     Publisher VARCHAR(50),
     PublicationYear CHAR(4),
	 PRIMARY KEY(AccessionNumber)); 
     

CREATE TABLE Borrow(
     AccessionNumber CHAR(5),
     MemberID CHAR(10),
     BorrowDate DATE,
	 PRIMARY KEY(AccessionNumber, MemberID),
	 FOREIGN KEY(AccessionNumber) REFERENCES Book(AccessionNumber) ON UPDATE CASCADE,
	 FOREIGN KEY(MemberID) REFERENCES Member(MemberID)); 

CREATE TABLE Reserve(
     AccessionNumber CHAR(5),
     MemberID CHAR(10),
     ReserveDate DATE,
	 PRIMARY KEY (AccessionNumber, MemberID),
	 FOREIGN KEY (AccessionNumber) REFERENCES Book(AccessionNumber) ON UPDATE CASCADE,
	 FOREIGN KEY (MemberID) REFERENCES Member(MemberID) ON DELETE CASCADE); 

CREATE TABLE Writes (
    AuthorID INT,
    AccessionNumber CHAR(5),
    PRIMARY KEY(AuthorID, AccessionNumber),
    FOREIGN KEY(AccessionNumber) REFERENCES Book(AccessionNumber) ON UPDATE CASCADE,
    FOREIGN KEY(AuthorID) REFERENCES Author(AuthorID) ON UPDATE CASCADE);