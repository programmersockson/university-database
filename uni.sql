CREATE DATABASE university;
# DROP DATABASE university; 

USE university;

CREATE TABLE Students (
  student_id INT PRIMARY KEY AUTO_INCREMENT,
  full_name VARCHAR(255) NOT NULL,
  course INT NOT NULL CHECK (course BETWEEN 1 AND 6),
  group_num INT NOT NULL CHECK (group_num BETWEEN 1 AND 10),
  test_retakes INT DEFAULT 0,
  access BOOL DEFAULT TRUE,
  exam_retakes INT DEFAULT 0,
  expulsion BOOL DEFAULT FALSE,
  date_of_admission DATE NOT NULL
);

CREATE TABLE Teachers (
  teacher_id INT PRIMARY KEY AUTO_INCREMENT,
  full_name VARCHAR(255) NOT NULL,
  degree VARCHAR(255) NOT NULL		
);

CREATE TABLE Subjects (
  subject_id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  has_test BOOL NOT NULL,
  has_exam BOOL NOT NULL
);

CREATE TABLE Lectures (
  lecture_id INT PRIMARY KEY AUTO_INCREMENT,
  date DATE NOT NULL,
  teacher_id INT NOT NULL,
  subject_id INT NOT NULL,
  group_num INT NOT NULL CHECK (group_num BETWEEN 1 AND 10),
  course INT NOT NULL CHECK (course BETWEEN 1 AND 6),
  FOREIGN KEY (teacher_id) REFERENCES Teachers(teacher_id),
  FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id)
);

CREATE TABLE Attendance (
  attendance_id INT PRIMARY KEY AUTO_INCREMENT,
  student_id INT NOT NULL,
  lecture_id INT NOT NULL,
  present BOOL NOT NULL DEFAULT TRUE,
  FOREIGN KEY (student_id) REFERENCES Students(student_id),
  FOREIGN KEY (lecture_id) REFERENCES Lectures(lecture_id)
);

CREATE TABLE Performance (
  performance_id INT PRIMARY KEY AUTO_INCREMENT,
  student_id INT NOT NULL,
  lecture_id INT NOT NULL,
  grade INT CHECK (grade BETWEEN 1 AND 10) DEFAULT NULL,
  FOREIGN KEY (student_id) REFERENCES Students(student_id),
  FOREIGN KEY (lecture_id) REFERENCES Lectures(lecture_id)
);

CREATE TABLE Overall_Performance (
  overall_performance_id INT PRIMARY KEY AUTO_INCREMENT,
  student_id INT NOT NULL,
  subject_id INT NOT NULL,
  rating FLOAT DEFAULT NULL CHECK (rating BETWEEN 1 AND 10),	
  test BOOL DEFAULT NULL,																
  exam INT DEFAULT NULL CHECK (exam BETWEEN 1 AND 10),											
  FOREIGN KEY (student_id) REFERENCES Students(student_id),
  FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id)
);

# Rating calculation in Overall_Performance table
DELIMITER //
CREATE TRIGGER update_rating AFTER UPDATE ON Performance
FOR EACH ROW
BEGIN
    DECLARE average_rating FLOAT;
    SELECT Overall_Performance.rating INTO average_rating 
    FROM Overall_Performance 
    WHERE Overall_Performance.student_id = NEW.student_id 
    AND Overall_Performance.subject_id = (SELECT subject_id FROM Lectures WHERE lecture_id = NEW.lecture_id);
    
    IF average_rating IS NULL THEN 
        SET average_rating = NEW.grade;
    ELSE
        SET average_rating = (average_rating + NEW.grade) / 2;
    END IF;

    UPDATE Overall_Performance SET rating = average_rating WHERE student_id = NEW.student_id AND subject_id = (SELECT subject_id FROM Lectures WHERE lecture_id = NEW.lecture_id);
END;
//
DELIMITER ;

# Update test_retakes, expulsion value in Students table
DELIMITER //
CREATE TRIGGER update_test_retakes
AFTER UPDATE ON Overall_Performance
FOR EACH ROW
BEGIN
  DECLARE retakes INT;
  SET retakes = (SELECT test_retakes FROM Students WHERE student_id = NEW.student_id);
  IF NEW.test = 0 THEN
    SET retakes = retakes + 1;
    UPDATE Students SET test_retakes = retakes WHERE student_id = NEW.student_id;
    IF retakes >= 3 THEN
	  UPDATE Students SET expulsion = TRUE WHERE student_id = NEW.student_id;
    END IF;
  END IF;
END//
DELIMITER ;

# Checking access to the Overall_Performance table
DELIMITER //
CREATE TRIGGER check_exam_access
BEFORE INSERT ON Overall_Performance.exam
FOR EACH ROW
BEGIN
  DECLARE retakes INT;
  SET retakes = (SELECT test_retakes FROM Students WHERE student_id = NEW.student_id);
  IF retakes >= 1 AND retakes < 3 THEN
    UPDATE Students SET access = FALSE WHERE student_id = NEW.student_id;
  END IF;
END//
DELIMITER ;

# Update the value of exam_retakes, expulsion in the Students table
DELIMITER //
CREATE TRIGGER update_exam_retakes
AFTER UPDATE ON Overall_Performance
FOR EACH ROW
BEGIN
  DECLARE retakes INT;
  SET retakes = (SELECT exam_retakes FROM Students WHERE student_id = NEW.student_id);
  IF NEW.exam < 4 THEN
    SET retakes = retakes + 1;
    UPDATE Students SET test_retakes = retakes WHERE student_id = NEW.student_id;
    IF retakes >= 3 THEN
	  UPDATE Students SET expulsion = TRUE WHERE student_id = NEW.student_id;
    END IF;
  END IF;
END//
DELIMITER ;

select * from Students;
select * from Teachers;
select * from Attendance;
select * from Subjects;
select * from Performance;
select * from Lectures;
select * from Overall_Performance;
