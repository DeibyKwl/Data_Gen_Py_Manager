SELECT store_name, weekday, open_time, close_time FROM store
INNER JOIN store_hours ON store_hours.store_id = store.store_id
WHERE '09:00:00' BETWEEN open_time AND close_time