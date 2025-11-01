CREATE TABLE IF NOT EXISTS roles (
    id serial primary key,
    name varchar(255),
    date_creation timestamp default CURRENT_TIMESTAMP
)