CREATE TABLE IF NOT EXISTS games (
    game_id varchar(10) NOT NULL,
    game_name varchar(250),
    release_date int,
    num_of_players int, 
    type_of_machine varchar(250),
    game_cost decimal(4,2),
    PRIMARY KEY(game_id)
)