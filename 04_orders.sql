INSERT INTO orders (user_id,total_amount,status)
SELECT
floor(random()*20)+1,
floor(random()*1000)+100,
'PAID'
FROM generate_series(1,20);