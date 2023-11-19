CREATE TABLE IF NOT EXISTS games (
    game_id varchar(10) NOT NULL,
    game_name varchar(250),
    release_date int,
    num_of_players varchar(250), 
    type_of_machine varchar(250),
    PRIMARY KEY(game_id)
)