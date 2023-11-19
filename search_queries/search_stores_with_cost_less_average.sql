WITH cost_total (store_name, value) AS
	(SELECT store_name, SUM(game_cost) FROM store
	INNER JOIN store_game ON store_game.store_id = store.store_id
	INNER JOIN games ON games.game_id = store_game.game_id
	GROUP BY store_name),
cost_total_avg (value) AS 
	(SELECT AVG(value) FROM cost_total)

SELECT store_name FROM cost_total, cost_total_avg
WHERE cost_total.value < cost_total_avg.value;