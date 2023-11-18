CREATE TABLE IF NOT EXISTS games (
    game_id varchar(10) NOT NULL,
    game_name varchar(250),
    release_date int,
    genre varchar(250),
    num_of_players int, 
    type_of_machine varchar(250),
    PRIMARY KEY(game_id)
)