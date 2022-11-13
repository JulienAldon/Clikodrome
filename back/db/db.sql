CREATE TABLE session (
    id INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (id),
    date VARCHAR(200),
    hour VARCHAR(200),
    is_approved tinyint(1)
) ENGINE=INNODB;

CREATE TABLE student (
    id INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (id),
    login VARCHAR(200),
    status VARCHAR(200),
    late VARCHAR(200),
    session_id INT,
    INDEX sess_ind(session_id),
    FOREIGN KEY (session_id) 
        REFERENCES session(id)
) ENGINE=INNODB;

CREATE TABLE remote (
    id INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (id),
    login VARCHAR(200),
    begin VARCHAR(200),
    end VARCHAR(200)
) ENGINE=INNODB;

