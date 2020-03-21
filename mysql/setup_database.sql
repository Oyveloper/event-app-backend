CREATE DATABASE event_app;
USE event_app;

CREATE TABLE events (
       id INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
       name VARCHAR(100) NOT NULL,
       description VARCHAR(1000) NOT NULL,
       start TIMESTAMP,
       end TIMESTAMP,
       host VARCHAR(100) NOT NULL,
       location VARCHAR(200),
       url VARCHAR(200),
       study_program VARCHAR(200) NOT NULL,
       class_year INTEGER
);