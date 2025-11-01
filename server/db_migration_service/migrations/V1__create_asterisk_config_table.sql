CREATE TABLE IF NOT EXISTS asterisk_config (
    id serial primary key,
    sip_port integer not null default 5060,
    tcp_port integer not null,
    username varchar(100) not null,
    password_hash bytea,
    date_creation timestamp default CURRENT_TIMESTAMP
)