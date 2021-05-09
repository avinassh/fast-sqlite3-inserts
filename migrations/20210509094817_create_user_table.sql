-- Add migration script here
create table IF NOT EXISTS user
(
    id INTEGER not null primary key,
    area CHAR(6),
    age INTEGER not null,
    active INTEGER not null
);
