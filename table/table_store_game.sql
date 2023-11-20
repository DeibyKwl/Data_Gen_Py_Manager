CREATE TABLE IF NOT EXISTS store_game (
    store_id varchar(10) NOT NULL,
    game_id varchar(10) NOT NULL,
    FOREIGN KEY(store_id) REFERENCES store(store_id),
    FOREIGN KEY(game_id) REFERENCES games(game_id)
)