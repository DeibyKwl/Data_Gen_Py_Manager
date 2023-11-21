(SELECT store_name, city FROM store WHERE city = 'portland')
UNION
(SELECT store_name, city FROM store WHERE city = 'saco')