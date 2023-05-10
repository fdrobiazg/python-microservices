CREATE USER 'auth_usr'@'localhost' IDENTIFIED BY 'auth123';
CREATE USER 'auth_usr'@'%' IDENTIFIED BY 'auth123';
GRANT ALL ON *.* TO 'auth_usr'@'localhost';
GRANT ALL ON *.* TO 'auth_usr'@'%';
FLUSH PRIVILEGES;

CREATE DATABASE auth;

USE auth;

CREATE TABLE user (
id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
username VARCHAR(255) NOT NULL UNIQUE,
password VARCHAR(255) NOT NULL UNIQUE
);

INSERT INTO user (username, password) VALUES ('root', 'password123');