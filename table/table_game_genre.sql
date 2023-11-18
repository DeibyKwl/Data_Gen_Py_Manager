CREATE TABLE IF NOT EXISTS game_genre (
    game_id varchar(10) NOT NULL,
    genre varchar(250),
    FOREIGN KEY(game_id) REFERENCES games(game_id)
)