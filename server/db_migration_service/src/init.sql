CREATE TABLE IF NOT EXISTS users (
    id serial primary key,
    login varchar(50) NOT NULL,
    PasswordHash bytea NOT NULL,
    Salt bytea NOT NULL,
    constraint login_constraint CHECK (
        length(login) BETWEEN 6 AND 50
        AND login ~ '^\w+$'
        )
);

CREATE TABLE IF NOT EXISTS info_users (
    id serial primary key,
    first_name varchar(100),
    last_name varchar(100),
    second_name varchar(100)
);

CREATE TABLE IF NOT EXISTS type_phone_numbers (
    id serial primary key,
    type varchar(50)
);

CREATE TABLE IF NOT EXISTS phone_numbers (
    id serial primary key,
    phone_number varchar(50),
    type_id int not null,
    foreign key (type_id) references type_phone_numbers(id),
    user_id int not null,
    foreign key (user_id) references info_users(id)
);
