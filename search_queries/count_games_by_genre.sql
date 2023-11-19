SELECT genre, COUNT(*) AS num_of_games FROM games
INNER JOIN game_genre ON game_genre.game_id = games.game_id
GROUP BY genre
ORDER BY COUNT(*) DESC;