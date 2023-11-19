SELECT store_name FROM user
INNER JOIN store ON store.store_id = user.store_id
WHERE user_id IN (SELECT user_id FROM user 
WHERE first_name = 'John' AND last_name = 'Doe')