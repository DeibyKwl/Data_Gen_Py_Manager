SELECT store_name FROM store
INNER JOIN store_game ON store_game.store_id = store.store_id
INNER JOIN games ON games.game_id = store_game.game_id
WHERE game_name = 'Donkey Kong'