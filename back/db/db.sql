USE Clikodrome;

CREATE TABLE session (
    id INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (id),
    date VARCHAR(200),
    hour VARCHAR(200),
    city VARCHAR(200),
    is_approved tinyint(1)
) ENGINE=INNODB;

CREATE TABLE promotion (
    id INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (id),
    name VARCHAR(200), -- wac1, wac2, tek1, tek2, tek3, msc1, msc2, premsc
    sign_id VARCHAR(200), -- edusign id or sign interface id (2w8jtzqdq84q6e8)
    year VARCHAR(200),
    city VARCHAR(200)
) ENGINE=INNODB;

CREATE TABLE student_session (
    id INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (id),
    login VARCHAR(200),
    card VARCHAR(200),
    status VARCHAR(200),
    session_id INT,
    INDEX sess_ind(session_id),
    FOREIGN KEY (session_id) 
        REFERENCES session(id)
) ENGINE=INNODB;


CREATE TABLE student (
    id INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (id),
    login VARCHAR(200),
    card VARCHAR(200),
    promotion_id INT,
    INDEX prom_ind(promotion_id),
    FOREIGN KEY (promotion_id) 
        REFERENCES promotion(id)
) ENGINE=INNODB;

CREATE TABLE remote (
    id INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (id),
    begin VARCHAR(200),
    end VARCHAR(200),
    student_id INT,
    FOREIGN KEY stud_ind(student_id)
        REFERENCES student(id)
) ENGINE=INNODB;

CREATE TABLE week_plan (
    id INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (id),
    day VARCHAR(200),
    city VARCHAR(200),
    promotion_id INT,
    INDEX prom_ind(promotion_id),
    FOREIGN KEY (promotion_id) 
        REFERENCES promotion(id)
) ENGINE=INNODB;