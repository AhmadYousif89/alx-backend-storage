-- SQL script that creates a table users

-- id, integer, never null, auto increment and primary key
-- email, string (255 characters), never null and unique
-- name, string (255 characters)
-- country, enumeration of countries: US, CO and TN, never null (= default will be the first element of the enumeration, here US)
-- If the table already exists, script should not fail
-- Script can be executed on any database

Drop table if exists users;
Create table if not exists users (
    id int not null auto_increment primary key,
    email varchar(255) not null unique,
    name varchar(255),
    country ENUM ('US', 'CO', 'TN') NOT NULL DEFAULT 'US'
);
