DROP DATABASE flask_contacts;
CREATE DATABASE flask_contacts;
DROP USER 'flaskuser'@'localhost';
CREATE USER 'flaskuser'@'localhost' IDENTIFIED BY 'flaskuser';
GRANT ALL PRIVILEGES ON flask_contacts.* TO 'flaskuser'@'localhost';
FLUSH PRIVILEGES;
