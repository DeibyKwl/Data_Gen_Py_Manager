SELECT game_name, game_cost from games
INNER JOIN store_game ON store_game.game_id = games.game_id
WHERE game_cost <= 0.50;