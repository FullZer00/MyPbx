alter table info_users
add column user_id integer not null
references users(id)