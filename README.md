#  Hybrid E-Commerce System

A mini backend system demonstrating **Hybrid Database Architecture** using:

*  PostgreSQL (ACID - transactional data)
*  MongoDB (BASE - flexible data)
*  Python Flask (Application layer)
*  Docker (MongoDB deployment)

---

##  Features

✔ Add Product (SQL + MongoDB)
✔ Place Order (ACID transaction with stock check)
✔ View Product Details (Hybrid query)
✔ Add Review (MongoDB)
✔ Purchase History (SQL JOIN)

---

##  Architecture

```
Flask App
   │
   ├── PostgreSQL → users, products, orders
   └── MongoDB   → product_details, activity_log
```

---

##  Project Workflow

1. User adds product → stored in PostgreSQL + MongoDB
2. User places order → SQL transaction updates stock
3. Activity is logged → MongoDB
4. User views product → data fetched from both databases

---
##  System Design
---
User → Flask App
    │
    ├── PostgreSQL (products, orders)
    └── MongoDB (reviews, activity logs)

---

##  Setup Instructions

### 1. Start MongoDB (Docker)

```
docker run -d -p 27017:27017 --name mongodb mongo
```

### 2. Install dependencies

```
pip install flask psycopg2-binary pymongo
```

### 3. Run app

```
python app.py
```

### 4. Open browser

```
http://127.0.0.1:5000
```

---

##  Screenshots

### Add Product

![Add Product](screenshots/01_users_table.png)

### Orders Table

![Orders](screenshots/06_orders_table.png)

### Purchase History (JOIN Query)

![Query](screenshots/03_purchase_history_query.png)

---

##  Key Concepts

* Hybrid Database Systems
* ACID vs BASE
* SQL JOIN operations
* MongoDB document model
* Transaction handling

---

##  Conclusion

This project demonstrates how real-world systems combine **relational + NoSQL databases** for performance and flexibility.

---

##  Author

Udoyan Ojah
