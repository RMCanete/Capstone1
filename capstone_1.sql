DROP DATABASE IF EXISTS capstone_1;

CREATE DATABASE capstone_1;

\c capstone_1

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE drinks (
    id SERIAL PRIMARY KEY,
    name TEXT,
    image TEXT,
    instructions TEXT,
    ingredients TEXT
);


CREATE TABLE ingredient (
    id SERIAL PRIMARY KEY, 
    name TEXT
);

CREATE TABLE drink_ingredient (
    id SERIAL PRIMARY KEY,
    drink_id INT REFERENCES drinks ON DELETE CASCADE,
    ingredient_id INT REFERENCES ingredient ON DELETE CASCADE,
    quantity TEXT,
    measurement_unit TEXT
);

CREATE TABLE comment (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users ON DELETE CASCADE,
    drink_id INT REFERENCES drinks ON DELETE CASCADE,
    created_at TIMESTAMP   NOT NULL
);

CREATE TABLE favorites (
    id SERIAL PRIMARY KEY,
    drink_id INT REFERENCES drinks ON DELETE CASCADE,
    user_id INT REFERENCES users ON DELETE CASCADE
);