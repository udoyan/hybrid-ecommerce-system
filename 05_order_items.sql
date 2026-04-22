INSERT INTO order_items (order_id,product_id,quantity,price_at_purchase)
SELECT
floor(random()*20)+1,
floor(random()*50)+1,
floor(random()*5)+1,
floor(random()*500)+50
FROM generate_series(1,40);