(SELECT store_name, city,address FROM store WHERE city = 'portland')
UNION
(SELECT store_name, city,address FROM store WHERE city = 'saco')