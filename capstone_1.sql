DROP DATABASE IF EXISTS capstone_1;

CREATE DATABASE capstone_1;

\c capstone_1

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    user_password TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE drinks (
    drink_id SERIAL PRIMARY KEY,
    drink_ingredients_id INT   NOT NULL,
    drink_image TEXT,
    drink_instructions TEXT
);

CREATE TABLE drink_ingredient (
    drink_ingredient_id SERIAL PRIMARY KEY,
    drink_id INT REFERENCES drinks ON DELETE CASCADE,
    quantity FLOAT,
    measurement_unit TEXT
);

CREATE TABLE comment (
    comment_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users ON DELETE CASCADE,
    drink_id INT REFERENCES drinks ON DELETE CASCADE,
    created_at TIMESTAMP   NOT NULL
);

CREATE TABLE ingredient (
    ingredient_id SERIAL PRIMARY KEY, 
    drink_ingredient_id INT REFERENCES drink_ingredient ON DELETE CASCADE,
    ingredient_name TEXT
);

CREATE TABLE favorites (
    favorite_id SERIAL PRIMARY KEY,
    drink_id INT REFERENCES drinks ON DELETE CASCADE,
    user_id INT REFERENCES users ON DELETE CASCADE
);