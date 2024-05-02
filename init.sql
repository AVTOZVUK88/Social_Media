CREATE TABLE "User" (
    id_user SERIAL PRIMARY KEY,
    username VARCHAR(15),
    password VARCHAR(15),
    created_at date,
    updated_at date
);

CREATE TABLE "Post" (
    id_post SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES User(id_user),
    text TEXT,
    created_at date,
    updated_at date
);