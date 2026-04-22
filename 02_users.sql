INSERT INTO users (name,email,password_hash)
SELECT 
'User'||i,
'user'||i||'@mail.com',
'hash'
FROM generate_series(1,20) i;