CREATE TABLE IF NOT EXISTS store_hours (
    store_id varchar(10) NOT NULL,
    weekday varchar(250),
    open_time time,
    close_time time,
    FOREIGN KEY(store_id) REFERENCES store(store_id)
)