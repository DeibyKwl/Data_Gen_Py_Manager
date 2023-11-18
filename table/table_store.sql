CREATE TABLE IF NOT EXISTS store (
    store_id varchar(10) NOT NULL,
    store_name varchar(250),
    website varchar(250),
    city varchar(250),
    address varchar(250), 
    PRIMARY KEY(store_id)
)