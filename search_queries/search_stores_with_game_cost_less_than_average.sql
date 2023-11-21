WITH cost_total (store_name, value) AS
    (SELECT store_name, AVG(game_cost) FROM store
    INNER JOIN store_game ON store_game.store_id = store.store_id
    INNER JOIN games ON games.game_id = store_game.game_id
    GROUP BY store_name)

SELECT store_name, value FROM cost_total
WHERE value < (SELECT AVG(value) FROM cost_total);