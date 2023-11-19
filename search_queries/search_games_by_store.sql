SELECT game_name FROM games
INNER JOIN store_game ON store_game.game_id = games.game_id
INNER JOIN store ON store.store_id = store_game.store_id
WHERE store.store_name = 'Arcadia';