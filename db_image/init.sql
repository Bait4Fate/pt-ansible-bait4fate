CREATE ROLE replication WITH REPLICATION PASSWORD 'deb' LOGIN;
SELECT * FROM pg_create_physical_replication_slot('replication_slot');
\c db
CREATE TABLE email(
    ID SERIAL PRIMARY KEY,
    address VARCHAR (50) NOT NULL
);
CREATE TABLE phone(
    ID SERIAL PRIMARY KEY,
    number VARCHAR (50) NOT NULL
);
INSERT INTO email (address)
VALUES ('amogus@sus.am'),
       ('sussy@sus.am');
INSERT INTO phone (number)
VALUES ('8(800)555-35-35'),
       ('8(000)000-00-00');