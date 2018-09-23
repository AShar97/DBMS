-- DROP database 09feb2018;

create database 09feb2018;
use 09feb2018;

/*
drop table Course;
drop table Department;
drop table Slot;
drop table Room;
drop table ScheduledIn;
*/

CREATE TABLE Course (course_id VARCHAR(20) NOT NULL,
	division ENUM('I', 'II', 'III', 'IV', 'NA') DEFAULT 'NA',
	PRIMARY KEY (course_id, division));

CREATE TABLE Department (department_id VARCHAR(20) NOT NULL,
	name VARCHAR(50) NOT NULL,
	PRIMARY KEY (department_id),
	UNIQUE (name));

CREATE TABLE Slot (letter ENUM('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'A1', 'B1', 'C1', 'D1', 'E1') NOT NULL,
	day ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday') NOT NULL,
	start_time TIME NOT NULL,
	end_time TIME NOT NULL,
	PRIMARY KEY (letter, day));

CREATE TABLE Room (room_number VARCHAR(20) NOT NULL,
	location ENUM('Core-I', 'Core-II', 'Core-III', 'Core-IV', 'LH', 'Local') NOT NULL,
	PRIMARY KEY (room_number));


-- ScheduledIn table Contain Attributes (course_id, division, department_id, letter, day, room_number).
-- These attributes are primary keys in their corresponding table.
-- Hence to identify a record uniquely in ScheduledIn table we must have these attributes.


CREATE TABLE ScheduledIn (
	department_id VARCHAR(20) NOT NULL,
	course_id VARCHAR(20) NOT NULL,
	division ENUM('I', 'II', 'III', 'IV', 'NA') DEFAULT 'NA',
	letter ENUM('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'A1', 'B1', 'C1', 'D1', 'E1') NOT NULL,
	room_number  VARCHAR(20) NOT NULL,
	day ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday') NOT NULL,

	PRIMARY KEY (department_id, course_id, division, letter, day, room_number),
	FOREIGN KEY (department_id) REFERENCES Department(department_id),
	FOREIGN KEY (course_id, division) REFERENCES Course(course_id, division),
	FOREIGN KEY (letter, day) REFERENCES Slot(letter, day),
	FOREIGN KEY (room_number) REFERENCES Room(room_number));

-- DROP database 09feb2018;
