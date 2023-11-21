SELECT game_name FROM games
INNER JOIN game_genre ON game_genre.game_id = games.game_id
WHERE genre IN ('platformer', 'shooter')
GROUP BY game_name
HAVING COUNT(DISTINCT(genre)) = 2;