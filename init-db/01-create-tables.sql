CREATE TABLE IF NOT EXISTS "users" (
    "id" uuid NOT NULL UNIQUE,
    "email" varchar(255) NOT NULL UNIQUE,
    "password_hash" varchar(255) NOT NULL,
    PRIMARY KEY("id")
);