CREATE TABLE IF NOT EXISTS user (
    user_id varchar(10) NOT NULL,
    store_id varchar(10) NOT NULL,
    first_name varchar(250),
    last_name varchar(250),
    email varchar(250),
    PRIMARY KEY(user_id, store_id),
    FOREIGN KEY(store_id) REFERENCES store(store_id)
)