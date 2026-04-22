INSERT INTO products (name,price,stock_quantity,category)
SELECT
'Product'||i,
(100 + i*5),
100,
'Category'||(i%5)
FROM generate_series(1,50) i;