
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

CREATE TABLE filters (
    id SERIAL NOT NULL PRIMARY KEY,
    filter TEXT NOT NUll,
    property TEXT
);

CREATE TABLE website (
    id SERIAL NOT NULL PRIMARY KEY,
    "url" TEXT NOT NULL,
    filter_id INTEGER REFERENCES filters(id)
);

CREATE TABLE saved_houses (
    id SERIAL NOT NULL PRIMARY KEY,
    url TEXT NOT NULL,
    is_contacted boolean
);

